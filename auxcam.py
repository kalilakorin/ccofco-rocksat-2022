# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Skyler Puckett (modified for CC of CO RockSat-X 2022)

"""VC0706 image capture to local storage.
You must wire up the VC0706 to a USB or hardware serial port.
Primarily for use with Linux/Raspberry Pi but also can work with Mac/Windows"""

# import general python library's
import time
import logging
import serial
import os
# import Camera module library
import adafruit_vc0706

# Acquire the existing logger
try:
    logger = logging.getLogger(__name__)
except:
    logger = None
    print('Unable to acquire the global logger object, assuming that auxcam.py is being run on its own')


def main():

    logging.info('Initializing engineering camera')

    # Create a directory if not already there
    os.system('mkdir -p ./data-pictures')

    # For use with USB to serial adapter:
    try:
        uart = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=0.25)
        logging.info('serial port USB0... OK')
    except:
        logging.critical('failed to enable serial port USB0')
        return
    # Setup VC0706 camera
    try:
        vc0706 = adafruit_vc0706.VC0706(uart)
        logging.info('vc0706 (camera) ... OK')
    except:
        logging.critical('failed to enable vc0706 (engineering camera)')
        return
    print("VC0706 version:")
    print(vc0706.version)
    # Set the image size.
    vc0706.image_size = adafruit_vc0706.IMAGE_SIZE_640x480
    logging.info('engineer camera image size set to 640x480')

    # Note you can also read the property and compare against those values to
    # see the current size:
    size = vc0706.image_size
    if size == adafruit_vc0706.IMAGE_SIZE_640x480:
        print("Using 640x480 size image.")
    elif size == adafruit_vc0706.IMAGE_SIZE_320x240:
        print("Using 320x240 size image.")
    elif size == adafruit_vc0706.IMAGE_SIZE_160x120:
        print("Using 160x120 size image.")
    logging.info('engineer camera image size set to 640x480')

    # Set to take a photo when last photo finishes saving
    while True:
        IMAGE_FILE = "./data-pictures/image" + str(int(time.time() * 1000)) + ".jpg"
        # Take a picture.
        print("taking picture")
        if not vc0706.take_picture():
            logger.info("Failed to take picture!")
            print("OH gAwD! didnt TakE a Pic!")
            main()
        logging.info('image taken')
        print("picture taken")
        # Print size of picture in bytes.
        frame_length = vc0706.frame_length
        print("Picture size (bytes): {}".format(frame_length))

        # Open a file for writing (overwriting it if necessary).
        # This will write 50 bytes at a time using a small buffer.
        # You MUST keep the buffer size under 100!
        print("Writing image: {}".format(IMAGE_FILE), end="", flush=True)
        stamp = time.monotonic()
        # Pylint doesn't like the wcount variable being lowercase, but uppercase makes less sense
        # pylint: disable=invalid-name
        logging.info('image save beginning')
        with open(IMAGE_FILE, "wb") as outfile:
            wcount = 0
            while frame_length > 0:
                t = time.monotonic()
                # Compute how much data is left to read as the lesser of remaining bytes
                # or the copy buffer size (32 bytes at a time).  Buffer size MUST be
                # a multiple of 4 and under 100.  Stick with 32!
                to_read = min(frame_length, 32)
                copy_buffer = bytearray(to_read)
                # Read picture data into the copy buffer.
                if vc0706.read_picture_into(copy_buffer) == 0:
                    logger.info("Failed to read picture frame data!")
                    print("OH gAwD! I cOUldnT rEad pIC!")
                    main()
                # Write the data to SD card file and decrement remaining bytes.
                outfile.write(copy_buffer)
                frame_length -= 32
                # Print a dot every 2k bytes to show progress.
                wcount += 1
                if wcount >= 64:
                    print(".", end="", flush=True)
                    wcount = 0
        logging.info('image saved... OK')
        print()
        print("Finished in %0.1f seconds!" % (time.monotonic() - stamp))

if __name__ == '__main__':
    main()