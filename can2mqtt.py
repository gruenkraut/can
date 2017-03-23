import paho.mqtt.client as paho
import socket
import struct
import sys

import logging
import logging.handlers

# Achtung!
# lauft nur mit python3
# /opt/python3.4.1/bin/python3
 

log = logging.getLogger("__name__")
log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')

formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)


# CAN frame packing/unpacking (see `struct can_frame` in <linux/can.h>)
can_frame_fmt = "=IB3x8s"
 
def build_can_frame(can_id, data):
        can_dlc = len(data)
        #data = data.ljust(8, b'\x00')
        #can_id=2147484321
        print("ID: %X" % can_id)
        print(can_dlc)
        print(data)
        return struct.pack(can_frame_fmt, can_id, can_dlc, data)
 
def dissect_can_frame(frame):
        can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
        return (can_id, can_dlc, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
 
if len(sys.argv) != 2:
        print('Provide CAN device name (can0, slcan0 etc.)')
        sys.exit(0)
 
def on_connect(client, userdata, flags, rc):
 client.subscribe("can/out")
 log.debug('Connected with result code ' + str(rc))

def on_message(client, userdata, msg):
 print(msg.topic)
 print("##########################################")
 #s.send(build_can_frame(0x01, b'\x01\x02\x03'),)
 #print("##########################################")
 sTmp=str(msg.payload)[2:-1]
 print(sTmp)
 sTmp1="8000" + sTmp[2:4] + sTmp[:2]
 print(sTmp1)
 sId=sTmp1
 iID=int(sId,16)
 print(iID)
 sDa=sTmp.split(':')
 sI=bytearray(8)
 for x in range(1,len(sDa)):
  print(sDa[x])
  sI[x-1]=int(sDa[x],16)
 print(sDa)
 try:
  #pass
  #s.send(build_can_frame(0x01, b'\x01\x02\x03'))
  s.send(build_can_frame(iID, sI))
 except Exception as inst:
  print('Error sending CAN frame')
  print(type(inst))     # the exception instance
  print(inst.args)      # arguments stored in .args
  print(inst)           # __str__ allows args to be printed directly
 print("##########################################")


# create a raw socket and bind it to the given CAN interface
s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
s.bind((sys.argv[1],))

client = paho.Client("CAN_IN")
client.connect("192.168.101.240")
client.on_connect = on_connect
client.on_message = on_message


print('CAN-TO-MOSQUITTO Running...')

while True:
        cf = s.recv(16)
        #cf, addr = s.recvfrom(16)
        sDa=dissect_can_frame(cf)
        #print("RAW: %04X" % sDa[0])
        sIn1="%04X" % sDa[0]
        sIn=sIn1[6:8] + sIn1[4:6] + '0000'
        sID=sIn1[6:8] + sIn1[4:6]
        sIn=sIn+":%02X" % sDa[1]
        sData=""
        for i in range(2,sDa[1]+2):
         sIn=sIn+":%02X" % sDa[i]
         sData=sData+"%02X" % sDa[i]
        sData=sData+";"
        #print(sIn)

        if sIn[1] != 'F':
                client.publish("can/norm/in/woF0",sIn,1)
        client.loop()
        if sID[:2] == 'C0':
         client.publish("can/status/" + sID[:2],sID[2:4] + sData,1)
        else:
         client.publish("can/IoT/" + sID,sData,1)
        client.loop()
        try:
                pass #s.send(cf)
        except socket.error:
                print('Error sending CAN frame')
 
        try:
                pass #s.send(build_can_frame(0x01, b'\x01\x02\x03'))
        except socket.error:
                print('Error sending CAN frame')

