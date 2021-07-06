import serial
import numpy as np
import serial.tools.list_ports as list_ports
import threading

class Arduino():
    """Class for interacting with the Arduino to get signal information
    """

    def __init__(self,baud=115200,timeout=0.2):
        self.baud = baud
        self.timeout = timeout

        self.ports_avail = list_ports.comports()
        self.port = None

        self.streaming = False

        self.stream_thread = None
        self.latest_position = np.array([0,0,0],dtype='f8')
        self.latest_calib = np.array([0,0,0,0])

    def update_ports(self):
        self.ports_avail = list_ports.comports()
        return self.ports_avail

    def connect(self,port_name):
        if self.port is not None and self.port.is_open:
            self.disconnect()

        self.port = serial.Serial(port_name,baudrate=self.baud,timeout=self.timeout)
        response = b'asdf'
        attempts = 0
        while attempts < 3 and response[0:2] != b'Hi':
            self.port.write(b'h')
            response = self.port.readline()
            attempts += 1
        
        if response[0:2] == b'Hi':
            return True
        else:
            return False

    def auto_connect(self):
        self.update_ports()
        for p in self.ports_avail:
            print("Attempting Connection to " + p.device)
            if self.connect(p.device):
                print("Successfully Connected to Arduino at " + p.device)
                return True
        
        ConnectionError('Connection failed! Check to see if connected to Arduino')
        return False

    def disconnect(self):
        if self.port is not None and self.port.is_open:
            self.port.close()
            self.port = None

    def start(self):
        if self.port is not None and self.port.is_open and not self.streaming:
            self.port.write(b'y')
            self.streaming = True
            self.stream_thread = threading.Thread(target=self.stream)
            self.stream_thread.start()

    def stop(self):
        if self.streaming:
            self.port.write(b'n')
            self.streaming = False
            self.stream_thread.join()
            self.stream_thread = None

    def stream(self):
        while self.streaming:
            data = self.port.readline().decode('ascii')
            data = np.array(data.split('\t')).astype(np.float)
            self.latest_position = data[0:3]
            self.latest_calib = data[3:]

