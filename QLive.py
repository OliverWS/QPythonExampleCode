#! /usr/bin/env python3
import os
from glob import glob
import time
from datetime import datetime
import serial
import sys


def openSerialPort(port):
	ser = serial.Serial()
	ser.baudrate = 57600
	ser.port = port
	while not ser.is_open:
		time.sleep(1)
		print("Opening serial connection to %s at %d baud"%(ser.port,ser.baudrate))
		try:
			ser.open()
		except Exception as e:
			print(e)
			continue
	print("Successfully connected to %s"%(ser.port))
	return ser




def main(port):
	ser = openSerialPort(port)
	ID1 = "Q" + os.path.split(port)[-1][-8:-4]
	print("Starting data collection...")
	ser.reset_input_buffer()
	while True:
		try:
			packet = ser.readline().rstrip(b"\n").rstrip(b"\r")
			#Format: Sample #,Z-axis,Y-axis,X-axis,Battery,Temperature(C),EDA(uS)
			(Z, Y, X, vBat, Temp, EDA) = [float(x) for x in packet.split(",")[1:]]
			print("EDA = %0.3f | Accelerometer = [%0.3f,%0.3f,%0.3f] | Temperature (F) = %0.1f"%(EDA, X,Y,Z, (Temp*(9.0/5.0) + 32) ))
		except KeyboardInterrupt:
			ser.close()
			print("Closing stream and exiting...")
			sys.exit()
			

if __name__ == '__main__':
	print("Welcome to Q Live!")
	print("The following Q Sensors are paired to your computer:")
	sensors = glob("/dev/tty.AffectivaQ-v2*")
	for sensor in sensors:
		print("\t[%d] %s"%(sensors.index(sensor), sensor.replace("/dev/tty.AffectivaQ-v2-","").replace("-SPP","")))
	s1 = int(input("Type the number of the sensor you want to use: " ))
	main(sensors[s1])
	
