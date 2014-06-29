#Client program to be executed on RPi.
#Author:Aniket Shirsat

import threading
import time
import serial
import MySQLdb
import standdb as database
import RPi.GPIO as GPIO
import os
import subprocess

def restart():
    os.system('sudo shutdown -r now')
def shutdown():
    os.system('sudo shutdown -h now')
ONLINE=1
gps_data="INVALID"
zig_data='BUS-STAND10000\n'
slat=0.0
slon=0.0
bus_stop=10000
switch_count=0

#Init GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.output(24,GPIO.HIGH)
GPIO.output(23,GPIO.LOW)



def Display():
    current_stop=database.route_data[(int(zig_data[9:14]))][0]
    print "Current Stop=",current_stop
    NextStopbase=(database.route_order.index(int(zig_data[9:14])))+1
    next_stop_ID=database.route_order[(NextStopbase)]
    next_stop=database.route_data[(next_stop_ID)][0]
    print "Next Stop=",next_stop

def send(lat,lon):
    cur.execute("""
	INSERT INTO  `sql340295`.`busdata` (
	`busno` ,
	`lat` ,
	`lon` ,
	`speed` ,
	`stop`,
	`busdate`
	)
	VALUES (
	'100',  %s,  %s,  '10', %s , NOW( )
	);
	""",(lon,lat,bus_stop))
    print bus_stop
    db.commit()
       

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
	global zig_data,gps_data,bus_stop
	while(1):
	    if (self.threadID==1):
	        response=GPS.readlines(None)
		GGA=response[2]
		info=GGA.split(',')		
		if(info[6]=="1"):          # 1 stand for GPS FIX SUCCESS
		    gps_data=info
		else:
		    gps_data="INVALID"
            else:
	        response=ZIG.readline()
		time.sleep(5)
		if(response[0:9]=="BUS-STAND"):
                    zig_data=response
	            bus_stop=int(zig_data[9:-1])

GPS = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)
ZIG = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)

# Create new threads
thread1 = myThread(1, "GPS")
thread2 = myThread(2, "ZIG")

# Start new Threads
thread1.start()
thread2.start()
if(ONLINE==1):
	db = MySQLdb.connect(host="sql3.freemysqlhosting.net", # your host, usually localhost           
                     user="sql340295", # your username
                      passwd="iB7%eQ2%" ,  # your password
                      db="sql340295") # name of the data base
	cur = db.cursor() 
	cur.execute("SELECT * FROM busdata")
loop=1
counter=0
while(loop):
    counter=counter+1
    os.system('clear')
    print(zig_data[:-1])            #Removing the ending (\n) element
    print(gps_data)
    Display()
    if(gps_data!="INVALID"):
	counter=0
	slat=float(gps_data[2])
	print(slat) 
	slon=float(gps_data[4])
	print(slon)
	lat=int(slat/100)+(slat%100)/60  #Converting NMEA to decimal format for latitute
	lon=int(slon/100)+(slon%100)/60  #Converting NMEA to decimal format for longitute
	if(ONLINE==1):
            send( lat , lon )                #Transmit to MySQL
    time.sleep(2)
    switch_input=GPIO.input(23)
    if(switch_input==1):
        print  "SHUTTING DOWN"
	loop=0

print "Exiting Main Thread"
shutdown()
