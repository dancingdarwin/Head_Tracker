import util.HeadTracker as HeadTracker
import util.Arduino as Arduino
import traceback
import util.WebcamUtil.Webcam as Webcam

if __name__ == "__main__":
    print("Initializing Arduino Board")
    #arduino = Arduino.Arduino()
    arduino = None 
    webcam = Webcam.Webcam(0)
    HeadTracker = HeadTracker.HeadTracker(arduino,webcam)

    while True:
        try:
            cmd = input(">").lower()
            if cmd == "start":
                print("Starting Tracking...")
                HeadTracker.start()

            if cmd == "end":
                print("Stopping Tracking")
                HeadTracker.stop()

            
        except KeyboardInterrupt:
            HeadTracker.disconnect()
            arduino.stop()
        except Exception as err:
            print('ERROR: ' + str(err))
            print(traceback.format_exc())

