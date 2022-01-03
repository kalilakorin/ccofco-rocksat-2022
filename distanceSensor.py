### Testings distance sensor
#import sys
#sys.path.insert(0, "build/lib.linux-armv71-2.7/")
import VL53L1X
import time
from datetime import datetime

distance = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
distance.open()
distance.start_ranging(1)
try:
    while True:
        distance_mm = distance.get_distance()
        print(distance_mm)

except KeyboardInterupt:
    distance.stop_ranging()

