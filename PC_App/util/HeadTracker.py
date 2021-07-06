import threading
import util.Arduino as Arduino
import socket
import numpy as np
import traceback

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

        self.arduino.auto_connect()

        self.latest_position = np.zeros(6,dtype='f8')

    def start(self):
        if not self.streaming:
            try:
                self.arduino.start()
            except:
                ConnectionError('Unable to start Arduino')
        
        self.streaming = True
        self.arduino.start()
        self.stream_thread = threading.Thread(target=self.stream)
        self.stream_thread.start()

    def stop(self):
        if self.streaming:
            self.arduino.stop()
            self.streaming = False
            self.stream_thread.join()

    def stream(self):
        print('Starting Stream')
        while self.streaming:
            self.latest_position[3:] = self.arduino.latest_position
            self.socket.send(self.latest_position.tobytes())

    def disconnect(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()