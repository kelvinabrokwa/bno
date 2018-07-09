#!/usr/bin/env python
"""
Author: Kelvin Abrokwa
"""
import serial
from serial.tools import list_ports
import binascii
import struct

INT_SIZE = 2  # Arduino ints are shorts
VEC3_SIZE = INT_SIZE * 3
PACKET_SIZE = (VEC3_SIZE * 4) + INT_SIZE
ARDUINO_VID = 0x2341
ARDUINO_PID = 0x43

# Describes the structure of the packet
packet_structure = {
    "acceleration": {
        "offset": 0,
        "size": VEC3_SIZE,
    },
    "gyro": {
        "offset": VEC3_SIZE,
        "size": VEC3_SIZE,
    },
    "magnetic": {
        "offset": VEC3_SIZE * 2,
        "size": VEC3_SIZE,
    },
    "orientation": {
        "offset": VEC3_SIZE * 3,
        "size": VEC3_SIZE,
    },
    "temperature": {
        "offset": VEC3_SIZE * 4,
        "size": INT_SIZE,
    },
}

class Point:
    def __init__(x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def roll(self):
        return self.x

    @property
    def pitch(self):
        return self.y

    @property
    def heading(self):
        return self.z

class BNOEvent:
    acceleration = None
    gyro = None
    magnetic = None
    orientation = None
    temperature = 0

    def __str__(self):
        return "acceleration={}\ngyro={}\nmagnetic={}\norientation={}\ntemperature={}\n".format(
                self.acceleration, self.gyro, self.magnetic, self.orientation, self.temperature)

def get_float(b):
    """
    Read 2 bytes as a float
    """
    assert len(b) == INT_SIZE
    return struct.unpack("h", bytes(b))[0] / 100.

def get_point(b):
    """
    Read 3 floats from the head of a byte array
    """
    assert len(b) >= INT_SIZE
    x = get_float(b[:2])
    y = get_float(b[2:4])
    z = get_float(b[4:6])
    return Point(x, y, z)

def deserialize_packet(packet):
    """
    Convert a packet to an BNOEvent object
    """
    event = BNOEvent()
    p = packet_structure

    event.acceleration = get_point(packet[
        p["acceleration"]["offset"]:p["acceleration"]["offset"] + p["acceleration"]["size"]])
    event.gyro = get_point(packet[
        p["gyro"]["offset"]:p["gyro"]["offset"] + p["gyro"]["size"]])
    event.magnetic = get_point(packet[
        p["magnetic"]["offset"]:p["magnetic"]["offset"] + p["magnetic"]["size"]])
    event.orientation = get_point(packet[
        p["orientation"]["offset"]:p["orientation"]["offset"] + p["orientation"]["size"]])
    event.temperature = get_float(packet[
        p["temperature"]["offset"]:p["temperature"]["offset"] + p["temperature"]["size"]])

    return event

def get_arduino_serial_port():
    """
    Return the serial port for the Arduino
    Finds it by VID/PID
    """
    print("Searching for serial port...")
    for port in list_ports.comports():
        if port.vid == ARDUINO_VID and port.pid == ARDUINO_PID:
            print("Found Arduino on port: {}".format(port.device))
            return port.device
    raise Exception("Arduino USB port not found")

def packet_is_valid(packet):
    """
    Return True if the packet size is as expected
    """
    return len(packet) == PACKET_SIZE

def BNO():
    """
    A generator that returns sensor readings
    """
    with serial.Serial(get_arduino_serial_port()) as ser:
        while True:
            packet = ser.readline()[:-1]  # strip newline character
            # Skip invalid packets. this will usually occur because a the delimiter accidentally
            # occurs in the middle of the packet, resulting in it being read as two smaller packets.
            if not packet_is_valid(packet):
                print("Incorrect packet: size={}".format(len(packet)))
                continue
            event = deserialize_packet(packet)
            yield event

if __name__ == "__main__":
    for event in BNO():
        print(event)
