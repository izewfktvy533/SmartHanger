#!/usr/bin/env python3

from xbee import ZigBee
from datetime import datetime
import ast
import json
import serial
import struct
import time


time.sleep(30)


PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
file_name = '/home/pi/SmartHanger/gateway/data/' + datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '.json'



def broadcast(xbee, data_str) :
    broadcast_addr = b'\x00\x00\x00\x00\x00\x00\xff\xff'

    xbee.send('tx', frame_id=b'\x00', broadcast_radius=b'\x01', optaions=b'\x01', dest_addr_long=broadcast_addr, data=data_str)
    


def handshake(count, message):
    for i in range(count):
        broadcast(xbee, message)
        time.sleep(1)



def start_handshake():
    handshake(3, "start\00")



def finish_handshake():
    handshake(6, "finish\00");



def parse_source_addr(packet):
    return struct.unpack('>q', packet['source_addr_long'])[0]
    

     
def xbee_handler(packet):
    timestamp_datetime = datetime.now()
    timestamp_str = timestamp_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    address_str = str(hex(parse_source_addr(packet)))
    
    try:
        data_dit = ast.literal_eval((packet['rf_data']).decode('utf-8'))
        data_dit.update({'timestamp': timestamp_str})
        data_dit.update({'address': address_str})

        print(data_dit)

        with open(file_name, 'a') as fp:
            fp.write(str(data_dit))
            fp.write("\n")
            fp.flush()

    except:
        print("error")
        pass



if __name__ == '__main__':
    ser = serial.Serial(PORT, BAUD_RATE)
    xbee = ZigBee(ser, escaped=True, callback=xbee_handler)

    start_handshake()
    


    try:
        while True:
            time.sleep(0.000001)

    except KeyboardInterrupt:
        print("finish process")
        finish_handshake();
        xbee.halt()
        ser.close()
