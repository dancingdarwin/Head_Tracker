#include <Arduino.h>
#line 1 "g:\\My Drive\\FileSyncs\\Dropbox\\Research\\Airan\\Codes\\HeadTracker\\Arduino\\Headtracker_IMU.ino"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

// Sensors
Adafruit_BNO055 bno = Adafruit_BNO055(55);

// Global Variables
bool isStreaming;

#line 12 "g:\\My Drive\\FileSyncs\\Dropbox\\Research\\Airan\\Codes\\HeadTracker\\Arduino\\Headtracker_IMU.ino"
void setup(void);
#line 30 "g:\\My Drive\\FileSyncs\\Dropbox\\Research\\Airan\\Codes\\HeadTracker\\Arduino\\Headtracker_IMU.ino"
void loop(void);
#line 68 "g:\\My Drive\\FileSyncs\\Dropbox\\Research\\Airan\\Codes\\HeadTracker\\Arduino\\Headtracker_IMU.ino"
void processCmd(char input);
#line 12 "g:\\My Drive\\FileSyncs\\Dropbox\\Research\\Airan\\Codes\\HeadTracker\\Arduino\\Headtracker_IMU.ino"
void setup(void) 
{
  Serial.begin(115200);
  Serial.println("Orientation Sensor Test"); Serial.println("");
  
  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("ERROR: no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  
  delay(1000);
    
  bno.setExtCrystalUse(true);
}

void loop(void) 
{

  //Check the Serial port
  if (Serial.available() > 0) {
    char incomingByte = Serial.read();
    processCmd(incomingByte);
  }

  if (isStreaming) {
    /* Get a new sensor event */ 
    sensors_event_t event; 
    bno.getEvent(&event);

    /* Get Calibration Values */
    uint8_t system, gyro, accel, mag;
    system = gyro = accel = mag = 0;
    bno.getCalibration(&system, &gyro, &accel, &mag);
  
    /* Display the floating point data */
    Serial.print(event.orientation.x, 4); // Yaw
    Serial.print("\t");
    Serial.print(event.orientation.z, 4); // Pitch
    Serial.print("\t");
    Serial.print(event.orientation.y, 4); // Roll
    Serial.print("\t");
    Serial.print(system, DEC);
    Serial.print("\t");
    Serial.print(gyro, DEC);
    Serial.print("\t");
    Serial.print(accel, DEC);
    Serial.print("\t");
    Serial.print(mag, DEC);
    Serial.println("");
  }
  
}

void processCmd(char input) {
  switch (input) {
    case 'h':
      isStreaming = false;
      Serial.println("Hi");
      break;
    case 'y':
      isStreaming = true;
      break;
    case 'n':
      isStreaming = false;
      break;
  }
}

