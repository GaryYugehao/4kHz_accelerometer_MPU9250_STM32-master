import datetime
import time

import serial

import numpy as np

from ctypes import cdll
from ctypes import c_double


def read_data(data, offset):
    arr = []
    for i in range(3):
        arr.append(int(data[i * 2 + offset] << 8 | data[i * 2 + 1 + offset]))
        if arr[i] >= 2 ** 15:
            arr[i] -= 2 ** 16
    return arr

def read_data1(data, offset):
    return int(data[offset] << 8 | data[1 + offset])


a = serial.Serial('COM7', 115200)

raw_datafile = open(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '-raw.txt', 'w')

a.write(b'\x01')

count = 0

while True:
    # read data
    data = a.read(16)
    raw_acc = read_data(data, 0)
    raw_gyr = read_data(data, 8)
    weight = read_data1(data, 14)

    # time interval between two samples (sec)
    tp = time.time()

    # attitude estimation

    raw_datafile.write(str(tp) + ' ' + str(raw_gyr[1]) + ' ' + str(raw_gyr[2]) + ' ' + str(raw_acc[0]) + ' ' + str(raw_acc[1]) + ' ' + str(raw_acc[2]) + ' ' + str(raw_gyr[0]) +' ' + str(weight) + '\n')

    count += 1

    if count % 250 == 0:
        count = 0
        # print("%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f" % (acc[0], acc[1], acc[2], gyr[0], gyr[1], gyr[2], q[0], q[1], q[2], q[3]),
            # end='\r')
        
        print(str(raw_gyr[1]) + ' ' + str(raw_gyr[2]) + ' ' + str(raw_acc[0]) + ' ' + str(raw_acc[1]) + ' ' + str(raw_acc[2]) + ' ' + str(raw_gyr[0]) + ' ' + str(weight), end='\r')

'''
连线
模块 -> 开发板
VCC     3.3
GND     G
SCLK    A5
SDI     A7
SDO     A6
INT     A1
NCS     A4

AO      A2
VCC     3,3
GND     GND

'''
