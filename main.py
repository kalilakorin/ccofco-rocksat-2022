#!/usr/bin/python
'''
    This is the main control script for the CC of CO RockSat 2021-2022 payload.
    Contributors:
        Konstantin Zaremski
	Jillian Frimml
	Skyler Puckett
        -- This software contains other software from the previous payload written
           by Andrew Bruckbauer and Konstantin Zaremski for RockSat 2019 - 2021.
    Testing:
        The control program can be tested using the '--test' argument. Testing
        mode simulates a shutdown
    Reset:
        The control program can be reset using the '--reset' argument.
        The reset argument clears any persisting save state so that operaiton
        can be tested as if running for the first time.
        $ python control.py --reset
        Flags can be supplied together (optional):    
        $ python control.py --reset --test
    Functionality:
        This program controls all payload functionality. All individual software
        subsystems for other experiments are integrated as modules that run in
        their own sub processes/threads.
    Spacecraft Battery Bus Timer Events:
        ID      Time    Description & Action
        GSE     T-30s   Spacecraft power is turned on and the Pi running this
                        control script boots up, loads this script as a service,
                        and waits unitl TE-R is triggered.
        TE-R    T+85s   The first timer event and one of two redundant lines is
                        powered, triggering motor extension and starting the 
                        video recording on the 360 degree camera.
        Interim         Between TE-R and TE-1 the camera will record the high
                        resolution 360 degree video at flight apogee.
        TE-1    T+261s  The first official timer event, but second for the VRSE
                        payload is powered triggering arm retraction and transfer
                        of the lower resolution file back to the Raspberry Pi for
                        data redundancy and durability if the camera is lost or
                        damaged during re-entry.
        TE-2    T+330s  The final timer event for the VRSE payload, which will
                        trigger a sync of filesystems and proper shutdown of the
                        Pi and other equipment for re-entry.
    Sensor Pins
        Temperature Sensor
            VCC - RED - 3.5v
            GND - BLK - Ground
            SDA - YLW - SDA
            SCL - BRN - SCL

        Accelerometer Sensor
            3v3 - RED - 3.5v
            GND - BLK - Ground
            SDA - YLW - SDA
            SCL - BRN - SCL

        Distance Sensor
            VIN - RED - 3.5v
            GND - BLK - Ground
            SDA - YLW - SDA
            SCL - BRN - SCL
'''

# Import required modules
import time
import logging
import os
import sys

# Set up logging and log boot time
boottime = int(time.time() * 1000)
logging.basicConfig(
    level=logging.DEBUG,
    encoding='utf-8',
    filename=f'logs/rocksat_payload_{str(boottime)}.log',
    format='[%(asctime)s.%(msecs)03d][%(levelname)s]\t%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logging.info(f'CC of CO payload finished booting at {boottime}')

# Entry point
if __name__ == '__main__':
    try:
        # Accept command line arguments
        arguments = sys.argv
        arguments.pop(0)

        # Primary experiment (360 camera and arm)
        mainThread = Process(target=main(arguments))
        mainThread.start()
        # Secondary experiment (radiation RAM)
        framExperiment = Process(target=fram)
        framExperiment.start()
        # Tertiary experiment (sensors)
        sensorThread = Process(target=sensors)
        sensorThread.start()

        # Prim
        p2.join()
        p1.terminate()
    except KeyboardInterrupt:
        print ('Caught KeyboardInterrupt exiting')
        
