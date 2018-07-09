# BNO055

This repo holds an Arduino sketch for reading data from a
[BNO055 Absolute Orientation Sensor](https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/overview),
serializing it, and writing it out to serial. It also has a python library for reading that serial
output, deserializing it, and making it available as an iterable.

### Usage

```python
from bno import BNO

for event in BNO():
    print(event.acceleration.x)
    print(event.orientation.pitch)
    print(event.temperature)
    # do more things with event
```

Events of type BNOEvent have the following properties
- acceleration: m/s^2 (.x, .y, .z)
- gyro: rad/s (.x, .y, .z)
- magnetic: micro Tesla (.x, .y, .z)
- orientation: degrees (.roll, .pitch, .heading)
- temperature: degrees Celsius

### Dependencies
- [Adafruit BNO055 Driver](https://github.com/adafruit/Adafruit_BNO055)
- [Adafruit Unified Sensor Driver](https://github.com/adafruit/Adafruit_Sensor)
- [pyserial](https://pythonhosted.org/pyserial/)

### Installing

```sh
python setup.py install
```
