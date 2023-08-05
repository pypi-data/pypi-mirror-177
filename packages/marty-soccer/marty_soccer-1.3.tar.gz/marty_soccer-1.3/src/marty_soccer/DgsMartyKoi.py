# need to install the following libraries using pip
import nums_from_string
from martypy import Marty

from datetime import datetime
import serial 

class DgsMartyKoi:
    def __init__(self):
        self.IsDebug = True
        self.my_marty = Marty("exp", "/dev/ttyAMA0")
        self.COM_PORT = '/dev/ttyACM0'
        self.BAUD_RATES = 115200
        self.timeout = 1
        self.ser = serial.Serial(self.COM_PORT, self.BAUD_RATES, timeout=self.timeout)

    def close(self):
        self.ser.close()
        self.my_marty.close()
        
    # When the whole system reboot, error may occur for the first serial communication
    # this function write a rotation command and flush all errors from the serial port
    # just let it read and wait for 3 seconds and return 
    
    def mt_koi_init(self):
        # write command and expect error and timeout
        self.ser.write('lcd.rotation(2)\r\n'.encode('UTF-8'))
    
        # expect 4 messages return (stdin error, rotation, Traceback, invalid syntax)
        try:
            starttime = datetime.now()
            while True:
                diff = datetime.now() - starttime
                sec = diff.total_seconds()
                if sec > 3:
                    break
                
                while self.ser.in_waiting:         
                    data_raw = self.ser.readline()  # will timeout if no return for 1 second (self.timeout = 1)
                    data = data_raw.decode()
                    # hide the error message anyway
                    #if self.IsDebug:
                    #   print('Received: ', data) 
        except:
            return
    
    # mt_koi_rotation is basically the same as mt_koi_init
    # It is to ensure the roration of the KOI lens has been set to what you need
    
    def mt_koi_rotation(self, orientation):
        # write command rotation to KOI lens
        self.ser.write(f'lcd.rotation({orientation})\r\n'.encode('UTF-8'))
    
        try:
            # set to return for 2 seconds
            starttime = datetime.now()
            while True:
                diff = datetime.now() - starttime
                sec = diff.total_seconds()
                if sec > 2:
                    break
            
                while self.ser.in_waiting:         
                    data_raw = self.ser.readline()
                    data = data_raw.decode()
                    if self.IsDebug:
                        print('Received: ', data)
        except:
            return
    

    # -----------------------------------------#
    #  usage: x, y = mt_koi_findCircle(7000)
    # -----------------------------------------# 
    def mt_koi_findCircle(self, threshold):
        # write findCircle command to KOI lens 
        self.ser.write(f'findCircle({threshold})\r\n'.encode('UTF-8'))   
            
        try:
            # start an infinite loop and wait for the result to return
            proceed = True
            xy_return = False
            cmd_return = False
            x = 0
            y = 0
            # proceed will be False if
            # (1) magnitude return / or empty list returned
            # (2) findCircle command returned
            while proceed:
                while self.ser.in_waiting:         
                    data_raw = self.ser.readline()
                    data = data_raw.decode()
                    if self.IsDebug:
                        print('Received: ', data)
                
                    if 'findCircle' in data:
                        cmd_return = True
                
                    if 'magnitude' in data:
                        xy_return = True
                    
                        info = nums_from_string.get_nums(data)
                        # extract the co-ordinate
                        x = info[0] 
                        y = info[1]
                        
                        if x < 30:
                            # don't why, it could be an error
                            # try reading second circle instead
                            if len(info) > 4:
                                x = info[4]
                                y = info[5]
                
                    if '[]' in data:
                        xy_return = True
                
                    if xy_return and cmd_return:
                        proceed = False
                        break
            return x, y
        except:
            return 0, 0
