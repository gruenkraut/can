#!/bin/bash


/etc/init.d/mqtt2can stop
/etc/init.d/can2mqtt stop

IN="$(ifconfig can0 | grep -i up | grep -v grep)"
if [ -z "$IN" ] ; then
 echo Init CAN0
 ifconfig can0 down
 ip link set can0 type can bitrate 20000
 ip link set can0 type can restart-ms 5
 ifconfig can0 up
fi
/etc/init.d/mqtt2can start
/etc/init.d/can2mqtt start
