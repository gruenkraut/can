#!/bin/bash

#Live demo
#ip -det -stat link show can0

#Recover from bus-off
#ip link set can0 type can restart

ifconfig can0 down
ip link set can0 type can bitrate 20000
ip link set can0 type can restart-ms 5
ifconfig can0 up
