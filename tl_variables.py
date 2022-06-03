#!/usr/bin/env python

# # +3.3v is pin 1 of the 40pin connector - use this to power tinyLiDAR (red wire)
SDA = 2  # gpio pin for data - this is pin 3 of the 40pin connector (white wire) BCM mode
SCL = 3  # gpio pin for clock - this is pin 5 of the 40pin connector (yellow wire) BCM mode
# # Ground is pin 9 of the 40pin connector (black wire)

TimeBetweenMeasurements = 16  # in ms for sampling rate
I2C_Speed = 100000  # in bps, we require 100Kbps

default_tinyLiDAR_address = 0x10  # the Default tinyLiDAR address
I2C_Address = default_tinyLiDAR_address  # terminal's address
i2cAdr = default_tinyLiDAR_address  # tinyLiDAR's address

cal_offset_distance = 100  # exact distance to target in mm used for the CD command
cal_xtalk_distance = 400  # exact distance to target in mm used for the CX command

# default config values for the W command
SignalRateLimit = 10  # default value for SignalRateLimit which can be 0.00 to 65.00 MCPS, is entered here as 100x the required value
SignalEstimateLimit = 60  # default value for SignalEstimateLimit in mm
TimingBudget = 20  # default value for TimingBudget in milliseconds (ms), value can be 18 to 2000ms
VCELperiod = 18  # default value for VCELperiod selection, can choose either 18/14 or 14/10. 18 = 18/14, 14 = 14/10

broadcast_address = 0
rebootTime = 1000  # time in ms

# available commands
tinyLiDAR_commands = {

    'D': "'D' to measure distance",
    'DC': "'DC' Continuous Read from Terminal. Press Enter to Quit.",
    'V': " 'V' scan and verify I2C addr loop",  # not available
    'X': " 'X' to reboot",
    'Y': " 'Y' to save LED config and reboot",
    'E': " 'E' LED off",
    'F': " 'F' LED indicator",
    'G': " 'G' LED on",
    'I': " 'I' set terminal's I2C address",
    'Q': " 'Q' configuration parameters",
    'R': " 'R' set tinyLiDAR's I2C address",
    'W': " 'W' write custom VL53L0X config",
    'AR': " 'A R' auto I2C addr config loop",  # not available
    'PL': " 'P L' long range preset",
    'PS': " 'P S' high speed preset",
    'PH': " 'P H' high accuracy preset",
    'PT': " 'P T' tinyLiDAR preset",
    'MS': " 'M S' SingleStep mode",
    'MC': " 'M C' Continuous mode",
    'RESET': " 'Reset' command to Address 0x00, will set all boards to Factory Defaults.",
    'T0': " 'T 0' WDT off",
    'T1': " 'T 1' WDT on",
    'CD': " 'C D' calibrate distance offset ",
    'CX': " 'C X' calibrate crosstalk "

}
