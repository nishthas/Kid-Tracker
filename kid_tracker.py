import serial
import time
import RPi.GPIO as GPIO
port = serial.Serial("/dev/ttyAMA0", 9600, timeout=3.0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(24 , GPIO.OUT)
GPIO.setup(23 , GPIO.OUT)

GPIO.output(23,False)
GPIO.output(24,False)
print"GSM 900\n"
print"List of operating Commands"
print"Commands		functions"
print"AT	to check operations"
port.write('AT\r\n')		
rcv = port.read(20)
print"GSM" + rcv
	
while True:
          
    port.flushInput()	
    rcv= port.read(100)
    print rcv
	    
    if '+CMTI:' in rcv:  
		print 'message received'
        #print rcv
		num = rcv[14:16]
	
		keyin2 = 'AT+CMGR='+str(num)+'\r\n'
		port.write(keyin2)
		
		
		port.flushInput()
	
		mesg= port.read(150)
	
		number = mesg[38:48]
		if number=="8587003475":
			print "Access granted"
			GPIO.output(24,True)
			GPIO.output(23,False)
			#print "Clap Sensed" +"\n"
			#time.sleep(2)
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
	
	       			a = "Latitude=" + data[3]+data[4]+"\n"
	       			b = "Longitude=" + data[5] + data[6]+"\n"
	       			c = "Speed=" + data[7]+"\n"
	       			d = "Course=" + data[8]+"\n"
				e=a+b+c+d

			#activating GSM
			GPIO.output(23,False)
			GPIO.output(24,False)
			port.write('AT+CGATT?\r\n')
			port.write('AT+CIPMUX=0\r\n')
			port.write('AT+CSTT="portalnmms","raspberry","pi"\r\n')
			port.write('AT+CIICR\r\n')
			port.write('AT+SAPBR=3,1,"APN","portalnmms"\r\n')
			port.write('AT+SAPBR=3,1,"CONTYPE","GPRS"\r\n')
			port.write('AT+SAPBR=1,1\r\n')
			port.write('AT+SAPBR=2,1\r\n')
			port.write('AT+EMAILCID=1\r\n')
			port.write('AT+EMAILTO=30\r\n')
			port.write('AT+EMAILSSL=1\r\n')
			port.write('AT+SMTPSRV="smtp.mail.yahoo.com",465\r\n')
			port.write('AT+SMTPAUTH=1,"tracker.child@yahoo.in","smartkid3"\r\n')
			port.write('AT+SMTPFROM="tracker.child@yahoo.in","child tracker"\r\n')
			port.write('AT+SMTPRCPT=0,0,"srishti.j93@gmail.com","Srishti Gupta"\r\n')
			port.write('AT+SMTPSUB="LOCATION"\r\n')
			port.write('AT+SMTPBODY\r\n')
			port.write('e\r\n')
			port.write('AT+SMTPSEND\r\n')

	
			"""
			print "Camera taking picture"+"\n"
			os.system("raspistill -t 100 -o img.jpg")
			time.sleep(1)
			print "Image captured.. saved"+"\n"
			print "Successful Completion"
		    """

		else:
			print "Access denied"
 

	



