# uncompyle6 version 3.4.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (default, Apr  6 2019, 01:42:57) 
# [GCC 8.2.0]
# Embedded file name: GpsMqtt_V1.0.py
# Compiled at: 2019-09-03 11:48:19
import paho.mqtt.client as mqtt, time, socket, serial
from decimal import *
from subprocess import call
import RPi.GPIO as GPIO, logging, sys
count = 0

def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i


GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename='logfile', filemode='a+', format='%(asctime)-15s %(levelname)-8s %(message)s')

def on_log(client, userdata, level, buf):
    logging.info(('log').format(+buf))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info('connected Ok')
    else:

	print 'dsff'
        logging.info(('Error').format(rc))


def on_disconnect(client, userdata, flags, rc=0):
    print 'Disconnected result code ' + str(rc)
    client.reconnect(broker)

def on_message(client, userdata, msg):
    topic = msg.topic
    GPS_Coordinates = str(s1) + ',' + str(s2)
    m_decode = str(msg.payload.decode('utf-8'))
    if m_decode == 'ON':
        client.publish('testTopic', GPS_Coordinates)


broker = 'broker.mqtt-dashboard.com'
client = mqtt.Client('py1')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_log = on_log
client.on_message = on_message
logging.info(('connecting to broker').format(broker))
try:
    client.connect(broker)
except (socket.error, socket.gaierror) as e:
    time.sleep(15)
    client.connect(broker)

client.loop_start()
client.subscribe('testTopic2')
client.publish('testTopic', "Now the GPS is ON, Please send 'ON' command to get the Machine Location. You don't get coordinates? Please wait for 10-15 minutes, GPS is searching for satellites....")
port = serial.Serial('/dev/GPScomm', baudrate=115200, timeout=4)
port.write('AT\r\n')
rcv = port.read(200)
if 'OK' in rcv:
    pass
else:
    GPIO.output(7, GPIO.LOW)
    time.sleep(4)
    GPIO.output(7, GPIO.HIGH)
time.sleep(0.1)
port.write('AT+CGNSPWR=1\r\n')
rcv = port.read(200)
if 'OK' in rcv:
    pass
else:
    GPIO.output(7, GPIO.LOW)
    time.sleep(4)
    GPIO.output(7, GPIO.HIGH)
    port.write('AT+CGNSPWR=1\r\n')
    rcv = port.read(200)
print rcv
GPIO.cleanup()
time.sleep(0.1)
port.write('AT+CGNSIPR=115200\r\n')
rcv = port.read(200)
time.sleep(0.1)
port.write('AT+CGNSTST=1\r\n')
rcv = port.read(100)
time.sleep(0.1)
port.write('AT+CGNSINF\r\n')
rcv = port.read(200)
time.sleep(0.1)
ck = 1
while True:
    fd = port.read(200)
    time.sleep(0.5)
    if '$GNRMC' in fd:
        ps = fd.find('$GNRMC')
        dif = len(fd) - ps
        if dif > 50:
            data = fd[ps:ps + 50]
            ds = data.find('A')
            if ds > 0 and ds < 20:
                p = list(find(data, ','))
                lat = data[p[2] + 1:p[3]]
                lon = data[p[4] + 1:p[5]]
                s1 = lat[2:len(lat)]
                s1 = Decimal(s1)
                s1 = s1 / 60
                s11 = int(lat[0:2])
                s1 = s11 + s1
                s2 = lon[3:len(lon)]
                s2 = Decimal(s2)
                s2 = s2 / 60
                s22 = int(lon[0:3])
                s2 = s22 + s2
# okay decompiling GpsMqtt_V1.0.pyc
