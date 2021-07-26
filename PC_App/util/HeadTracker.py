import threading
import util.Arduino as Arduino
import socket
import numpy as np
import traceback

# TODO add webcam class to parameters
class HeadTracker():
    def __init__(self, arduino:Arduino.Arduino, udp_address="localhost", port=4242):
        self.stream_thread = None
        self.streaming = False
        self.arduino = arduino


        # Connect UDP Port
        self.udp_addr = udp_address
        self.udp_port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((self.udp_addr,self.udp_port))

        if not (self.arduino is None):
            self.arduino.auto_connect()
        else:
            print('error arduino not found')

        #self.arduino.auto_connect()

        self.latest_position = np.zeros(6,dtype='f8')

# TODO: Check if arduino is connected before running this bit

    def start(self):
        if not (self.arduino is None):
            if not self.streaming:
                try:
                    self.arduino.start()
                except:
                    ConnectionError('Unable to start Arduino')
        
            self.streaming = True       # NEED THIS PART
            self.arduino.start()
            self.stream_thread = threading.Thread(target=self.stream) #####NEED THIS PART
            self.stream_thread.start() # NEED THIS PART
        

    def stop(self):
        if not (self.arduino is None):
            if self.streaming: # NEED THIS PART
                self.arduino.stop()
                self.streaming = False # NEED THIS PART
                self.stream_thread.join() # NEED THIS PART
        

    def stream(self):
        if not (self.arduino is None):
            print('Starting Stream')
            while self.streaming:
                self.latest_position[3:] = self.arduino.latest_position
                self.socket.send(self.latest_position.tobytes())
        

    def disconnect(self):
        if not (self.arduino is None):
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()\
        
