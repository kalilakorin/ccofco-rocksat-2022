#!/usr/bin/python
'''
    This is the main control script for the CC of CO RockSat 2021-2022 payload.

    Contributors:
	    Jillian Frimml
	    Skyler Puckett
        Konstantin Zaremski
    
    --- This product contains software from the previous payload written
        by Andrew Bruckbauer and Konstantin Zaremski for RockSat 2019 - 2021.
    
    Testing:
        The control program can be tested using the '--test' argument. Testing
        mode simulates a shutdown.
    
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
        their own sub processes/threads. Timer events should be listened to within
        this file and not any of the other sub modules in case changes need to be 
        made to timing.
'''

# Import required modules
import time
import logging
from logging.handlers import RotatingFileHandler
import os
import multiprocessing as multiprocessing
import sys

# Import system modules
import sensors
import fram

# Set up logging and log boot time
boottime = int(time.time() * 1000)
rotatingFileHandler = RotatingFileHandler(
 	filename=f'logs/rocksat_payload_{str(boottime)}.log', 
  	mode='a',
  	maxBytes=20*1024*1024,
  	backupCount=2,
  	encoding='utf-8',
  	delay=0
)
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s.%(msecs)03d][%(module)7s][%(levelname)8s]\t%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[rotatingFileHandler])
    
#formatter = logging.Formatter('[%(asctime)s.%(msecs)03d][%(module)7s][%(levelname)8s]\t%(message)s')

logger = logging.getLogger(__name__)

# Output all logs to console
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

logger.info(f'CC of CO payload finished booting at {boottime}')

# Entry point
if __name__ == '__main__':
    try:
        multiprocessing.set_start_method('fork')
        processQueue = multiprocessing.Queue()
        # Accept command line arguments
        #arguments = sys.argv

        # Secondary experiment (radiation RAM)
        goproThread = multiprocessing.Process(target=gopro.main)
        goproThread.start()

        # Secondary experiment (radiation RAM)
        framExperimentThread = multiprocessing.Process(target=fram.main)
        framExperimentThread.start()

        # Tertiary experiment (sensors)
        sensorThread = multiprocessing.Process(target=sensors.main)
        sensorThread.start()

        # Prim
        #p2.join()
        #p1.terminate()
    except KeyboardInterrupt:
        print ('Caught KeyboardInterrupt exiting')
        
