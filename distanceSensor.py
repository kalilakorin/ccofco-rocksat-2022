# ### Testings distance sensor
# <<<<<<< HEAD
#
# =======
# #import sys
# #sys.path.insert(0, "build/lib.linux-armv71-2.7/")
# >>>>>>> 9d8c1ca4bf601053f98d66ef08406de2befe0c47
# import VL53L1X
# import time
# from datetime import datetime
#
# distance = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
# distance.open()
# distance.start_ranging(1)
# try:
#     while True:
#         distance_mm = distance.get_distance()
#         print(distance_mm)
#
# except KeyboardInterupt:
#     distance.stop_ranging()

import adafruit_vl53l1x
import time
import board
i2c = board.I2C()

distance = adafruit_vl53l1x.VL53L1X(i2c)
distance.distance_mode = 1
distance.start_ranging()
while True:
    if distance.data_ready:
        print("{}".format(distance.distance))
        time.sleep(1.0)



