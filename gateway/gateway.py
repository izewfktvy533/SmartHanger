#!/usr/bin/env python3
from xbee import ZigBee
from datetime import datetime
import serial
import ast
import time


PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600



def xbee_handler(packet):
    print(packet)
    print()
    timestamp_datetime = datetime.now()
    timestamp_str = timestamp_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    print(timestamp_str)

    try:
        data_dit = ast.literal_eval((packet['rf_data']).decode('utf-8'))
        print(data_dit)
        print(data_dit['tem_val1'])
        print()

    except:
        print("error")
        pass



if __name__ == '__main__':
    ser = serial.Serial(PORT, BAUD_RATE)
    xbee = ZigBee(ser, escaped=True, callback=xbee_handler)

    try:
        while True:
            time.sleep(0.000001)

    except KeyboardInterrupt:
        xbee.halt()
        ser.close()
