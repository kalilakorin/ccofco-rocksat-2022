#!/bin/bash

echo "Configuring operating system for payload..."
echo "** You will be prompted for your administrator account password!"

# Update package repositories and upgrade packages
sudo apt update
sudo apt upgrade -y

# Create data output directories
sudo mkdir -p ./data-fram
sudo mkdir -p ./data-sensors
sudo mkdir -p ./logs

# Enable i2c
sudo echo "dtparam=i2c_arm=on" >> /boot/config.txt

# Install python 3.9 and pip
#wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz
#tar -zxvf Python-3.9.9.tgz
#./configure --enable-optimizations
#sudo make altinstall

# Install python 3.7 (python3)
sudo apt install python3
sudo apt install python3-pip

# Disable splash screen and boot delay for faster boot
sudo echo "boot_delay=0" >> /boot/config.txt
sudo echo "disable_splash=1" >> /boot/config.txt

# Install python libraries/modules for sensors and hardware (systemwide)
sudo pip3 install adafruit-blinka 
sudo pip3 install adafruit-circuitpython-fram
sudo pip3 install adafruit-circuitpython-mpl115a2
sudo pip3 install adafruit-circuitpython-bme280
#sudo pip3 install vl53l1x #sudo pip3 install smbus2 # will uncomment if we need it
sudo pip3 install adafruit-circuitpython-vl53l1x

#Install the libraries/modules for the gopro connection
sudo pip3 install pybluez #bluetooth connection ble
sudo pip3 install open-gopro #open gopro so the pi and gopro can interact
sudo pip3 install goprocam #gopro api
sudo pip3 install gopro-ble-py-2 #ble control for gopro
sudo pip3 install termcolor
sudo pip3 install prettytable

echo "   *** DONE ***   "