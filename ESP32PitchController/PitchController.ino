// See invensense-imu submodule for included libraries
#include "MPU9250.h"
// See arduino-esp32 submodule for included libraries
#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

// an MPU9250 object with the MPU-9250 sensor on I2C bus 0 with address 0x68
MPU9250 IMU(Wire, 0x68);
int status;

void setup() {
  SerialBT.begin("Evan ESP32");

  while (!SerialBT) {}

  status = IMU.begin();

  if (status < 0) {
    SerialBT.println("IMU initialization unsuccessful");
    SerialBT.println("Check IMU wiring or try cycling power");
    SerialBT.print("Status: ");
    SerialBT.println(status);
    while (1) {}
  }

  IMU.calibrateAccel();
}

void loop() {
  // Set the accelerometer range to 2G
  IMU.setAccelRange(MPU9250::AccelRange::ACCEL_RANGE_2G);
  IMU.readSensor();
  // Send data from the z-axis of the accelerometer to control pitch knob over Bluetooth
  SerialBT.println(IMU.getAccelZ_mss(), 6);
}