#command that can be used to start the gopro
#https://gopro.github.io/labs/control/settings/
#resolution "r5" is 5k360 for the max r5K or "24"

#import gopromain as gopro
import time
import subprocess
from open_gopro import GoPro


#gopro.is_verbose = True
#set the address

#gopro.address = "D1:70:A4:FC:21:4F"
#print('address:', gopro.address)

'''
for key, value in gopro.settings_supported.items():
    print('key:', key, '\tvalue:', value, '\n')
print(gopro.settings_supported.values(), '\n')
'''


#gopro.settings_supported.__getattribute__('video.resolution')
#gopro.settings_supported.__setattr__("resolution", "R5K")


'''
#try to activate and connect to the gopro
goproIsOff = True
if (goproIsOff):
    try:
        time.sleep(1)
        gopro.run()
    except:
        goproIsOff = False
        #continue

#set the resolution

#set the video mode / 360

#set the frame rate

#start the video recording    
gopro.commands_supported = "record start"
'''

'''
#resolution "r5" is 5k360 for the max
print('Setting default video')
gopro.settings_supported.setdefault("r5")

subprocess.call(f'python3 gopromain.py --verbose --address "D1:70:A4:FC:21:4F" --command "mode video"', shell=True)
subprocess.call(f'python3 gopromain.py --verbose --address "D1:70:A4:FC:21:4F" --command "record start"', shell=True)
time.sleep(5)
subprocess.call(f'python3 gopromain.py --verbose --address "D1:70:A4:FC:21:4F" --command "record stop"', shell=True)
'''

'''
from goprocam import GoProCamera, constants

goproCamera = GoProCamera.GoPro()

goproCamera.shoot_video(10)
'''

with GoPro() as gopro:
    print("Yay! I'm connected via BLE, Wifi, initialized, and ready to send / get data now!")
    gopro.ble_setting.resolution.get_value()
    # Send some commands now