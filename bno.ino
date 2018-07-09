/**
   Serialize readings from a BNO055 and write them to serial

   Author: Kelvin Abrokwa (kelvinabrokwa@gmail.com)
*/

#include <assert.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

struct int_vec3 {
  int x;
  int y;
  int z;
};

struct event_packet {
  struct int_vec3 acceleration;
  struct int_vec3 gyro;
  struct int_vec3 magnetic;
  struct int_vec3 orientation;
  int temperature;
};

Adafruit_BNO055 bno = Adafruit_BNO055(55);
sensors_event_t event;
struct event_packet packet;

/**
 * Initialize serial and the sensor
 */
void setup()
{
  Serial.begin(9600);
  // Initialize the sensor
  while (!bno.begin()) {
    Serial.println("No BNO055 detected. Check your wiring or I2C ADDR!");
    delay(1000);
  }
  delay(1000);
  bno.setExtCrystalUse(true);
}

/**
 * float to int conversion per our serializer
 */
int float2int(float x)
{
  return (int)(x * 100);
}

/**
 * Convert a float_vec3 to an int_vec3 per our serializer
 */
void float2int_vec3(sensors_vec_t* float_vec, struct int_vec3* int_vec)
{
  int_vec->x = float2int(float_vec->x);
  int_vec->y = float2int(float_vec->y);
  int_vec->z = float2int(float_vec->z);
}

/**
 * Copy event data to a buffer
 */
void serialize_event(sensors_event_t* event, void* buf, size_t buf_size)
{
  assert(buf_size >= sizeof(struct event_packet));

  struct event_packet* packet = (struct event_packet*)buf;

  float2int_vec3(&event->acceleration, &packet->acceleration);
  float2int_vec3(&event->gyro, &packet->gyro);
  float2int_vec3(&event->magnetic, &packet->magnetic);
  float2int_vec3(&event->orientation, &packet->orientation);
  packet->temperature = float2int(event->temperature);
}

/**
 * Read events from the BNO055, serialize the data, and write them to serial
 */
void loop()
{
  bno.getEvent(&event);
  serialize_event(&event, &packet, sizeof(struct event_packet));
  Serial.write((char*)&packet, sizeof(struct event_packet));
  Serial.write('\n'); // events are newline delimited
  delay(100);
}
