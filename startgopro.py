#command that can be used to start the gopro
#https://gopro.github.io/labs/control/settings/
#resolution "r5" is 5k360 for the max r5K or "24"

import gopromain as gopro
import time

#--verbose --address "D1:70:A4:FC:21:4F" --command "record start"

gopro.is_verbose = True
#set the address
gopro.address = "D1:70:A4:FC:21:4F"
print('address:', gopro.address)

print(gopro.settings_supported.values())

#gopro.settings_supported.__getattribute__("resolution")
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

#resolution "r5" is 5k360 for the max
#gopro.settings_supported.setdefault(__resolution = "r5")
#gopro.settings_supported.setdefault(resolution)

'''
from goprocam import GoProCamera, constants

goproCamera = GoProCamera.GoPro()

goproCamera.shoot_video(10)
'''