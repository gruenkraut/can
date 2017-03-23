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
 
def build_can_frame(can_id, can_dlc, data):
        #can_dlc = len(data)
        data = data.ljust(8, b'\x00')
        print("ID: %X" % can_id)
        return struct.pack(can_frame_fmt, can_id, can_dlc, data)
 
def dissect_can_frame(frame):
        can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
        return (can_id, can_dlc, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
 
def on_connect(client, userdata, flags, rc):
 client.subscribe("can/classic_out")
 log.debug('Connected with result code ' + str(rc))

def on_message(client, userdata, msg):
 #print(msg.topic)
 #print("##########################################")
 #s.send(build_can_frame(0x01, b'\x01\x02\x03'),)
 #print("##########################################")
 sTmp=str(msg.payload)[2:-1]
 #print(sTmp)
 sTmp1="8000" + sTmp[2:4] + sTmp[:2]
 #print(sTmp1)
 sId=sTmp1
 iID=int(sId,16)
 #print(iID)
 sDa=sTmp.split(':')
 sI=bytearray(8)
 bFail=0
 for x in range(1,len(sDa)):
  #print(sDa[x])
  #print(len(sDa))
  try:
   sI[x-1]=int(sDa[x],16)
  except:
   sI[x-1]=0
   bFail=1
 #print(sDa)
 try:
  #pass
  #s.send(build_can_frame(0x01, b'\x01\x02\x03'))
  if bFail==0:
   s.send(build_can_frame(iID, len(sDa)-1, sI))
  else:
   bFail=0
 except Exception as inst:
  print('Error sending CAN frame')
  print(type(inst))     # the exception instance
  print(inst.args)      # arguments stored in .args
  print(inst)           # __str__ allows args to be printed directly
 #print("##########################################")

if len(sys.argv) != 2:
        print('Provide CAN device name (can0, slcan0 etc.)')
        sys.exit(0)
 
# create a raw socket and bind it to the given CAN interface
s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
s.bind((sys.argv[1],))

client = paho.Client("CAN_OUT")
client.connect("192.168.101.240")
client.on_connect = on_connect
client.on_message = on_message

print('MOSQUITTO-TO-CAN Running...')

while True:
        client.loop(timeout=5.0)
        try:
                pass #s.send(cf)
        except socket.error:
                print('Error sending CAN frame')
 
        try:
                pass #s.send(build_can_frame(0x01, b'\x01\x02\x03'))
        except socket.error:
                print('Error sending CAN frame')

