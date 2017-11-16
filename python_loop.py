import serial
import time

s=serial.Serial('/dev/ttyACM0',115200);


while(1):
	for i in range(255):
		s.write("S"+chr(i)+chr(i)+"\r\n");
		s.write("S"+chr(i)+chr(i)+"\r\n");
		

