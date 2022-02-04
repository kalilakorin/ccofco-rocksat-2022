#command that can be used to start the gopro

import gopromain as gopro
import time

#--verbose --address "D1:70:A4:FC:21:4F" --command "record start"

gopro.is_verbose = True
#set the address
gopro.address = "D1:70:A4:FC:21:4F"

print(gopro.settings_supported.values())

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