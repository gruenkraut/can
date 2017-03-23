#!/bin/sh

#*************************
#NETDEV interface:
#*************************

#- download the driver peak-linux-driver-7.4.tar.gz from our linux website and copy it into your home directory.

#- Install libpopt-dev: sudo apt-get install libpopt-dev
#- Install g++: sudo apt-get install g++
#(only necessary to build the chardev test tool transmittest)

#- unpack the driver: tar -xzf peak-linux-driver-7.4.tar.gz
#- cd peak-linux-driver-7.4
#- make clean
#- make
#- sudo make install
#- sudo modprobe pcan
#check with cat /proc/pcan that the driver was successfully installed.
#*------------ PEAK-Systems CAN interfaces (http://www.peak-system.com) -------------
#*-------------------------- Release_20110912_n (7.4.0) ----------------------
#*------------- [mod] [isa] [pci] [dng] [par] [usb] [pcc] [net] --------------
#*--------------------- 1 interfaces @ major 250 found -----------------------
#*n -type- ndev --base-- irq --btr- --read-- --write- --irqs-- -errors- status
#32 usb can0 30520000 255 0x001c 00000000 00000000 00000000 00000000 0x0000

#Now we are ready to install the SocketCAN Tools:

#- goto home directory again:
#cd
#- Install git:
#sudo apt-get install git
#- Get the SocketCAN Tools:
#git clone git://gitorious.org/linux-can/can-utils.git
#- build and install the tools:
#cd can-utils
#make
#sudo make install

#Set the network up:
#sudo ifconfig can0 up

#Test the communication with candump:
#candump can0

#-available tools are:
#candump
#cangen 
#cansend
#canbusload
#canecho
#canlogserver 
#cansniffer
#canfdtest 
#canplayer

#define CAN_BAUD_1M 0x0014 // 1 Mbit/s 
#define CAN_BAUD_500K 0x001C // 500 kBit/s 
#define CAN_BAUD_250K 0x011C // 250 kBit/s 
#define CAN_BAUD_125K 0x031C // 125 kBit/s 
#define CAN_BAUD_100K 0x432F // 100 kBit/s 
#define CAN_BAUD_50K 0x472F // 50 kBit/s 
#define CAN_BAUD_20K 0x532F // 20 kBit/s 
#define CAN_BAUD_10K 0x672F // 10 kBit/s 
#define CAN_BAUD_5K 0x7F7F // 5 kBit/s 


echo "i 0x532F e" > /dev/pcanusb2
