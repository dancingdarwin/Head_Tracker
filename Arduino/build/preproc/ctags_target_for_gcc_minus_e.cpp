# 1 "g:\\My Drive\\FileSyncs\\Dropbox\\Research\\Airan\\Codes\\HeadTracker\\Arduino\\Headtracker_IMU.ino"
# 2 "g:\\My Drive\\FileSyncs\\Dropbox\\Research\\Airan\\Codes\\HeadTracker\\Arduino\\Headtracker_IMU.ino" 2
# 3 "g:\\My Drive\\FileSyncs\\Dropbox\\Research\\Airan\\Codes\\HeadTracker\\Arduino\\Headtracker_IMU.ino" 2
# 4 "g:\\My Drive\\FileSyncs\\Dropbox\\Research\\Airan\\Codes\\HeadTracker\\Arduino\\Headtracker_IMU.ino" 2
# 5 "g:\\My Drive\\FileSyncs\\Dropbox\\Research\\Airan\\Codes\\HeadTracker\\Arduino\\Headtracker_IMU.ino" 2

// Sensors
Adafruit_BNO055 bno = Adafruit_BNO055(55);

// Global Variables
bool isStreaming;

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
    Serial.print(system, 10);
    Serial.print("\t");
    Serial.print(gyro, 10);
    Serial.print("\t");
    Serial.print(accel, 10);
    Serial.print("\t");
    Serial.print(mag, 10);
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
