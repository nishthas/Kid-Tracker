import RPi.GPIO as GPIO
import time
import serial
import pyaudio
import wave
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(24 , GPIO.IN)

while True:
	inputvalue = GPIO.input(24)
	if inputvalue==True:
	print "Clap Sensed" +"\n"
	time.sleep(2)
	print "GPS starts" +"\n"
	time.sleep(2)
	print "Waiting for GPS data....."+"\n"
	time.sleep(1)
	print "Loading....."
	time.sleep(1)
	f = open('data.txt','w')
	ser=serial.Serial('/dev/ttyAMA0',9600,timeout=300)
	x = ser.read(1200)
	pos1=x.find("$GPRMC")
	pos2=x.find("\n",pos1)
	loc=x[pos1:pos2]
	print "\n"+loc+"\n"
	f.write(loc)
	data=loc.split(',')
	if data[2]=='V':
	print "Invalid data"
	else:
		print "Latitude=" + data[3]+data[4]+"\n"
		print "Longitude=" + data[5] + data[6]+"\n"
		print "Speed=" + data[7]+"\n"
		print "Course=" + data[8]+"\n"
		print "Converting file to .gpx format" +"\n"
		os.system("gpsbabel -i NMEA -f data.txt -o GPX -F data.gpx")
		print "Camera taking picture"+"\n"
		os.system("raspistill -t 50 -o img.jpg")
		time.sleep(1)
		print "Image captured.. saved"+"\n"
		print "Opening GPSprune and showing location on map"
		os.system("gpsprune")
		print "Successful Completion "