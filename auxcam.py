# Skyler Puckett
#
# ffmpeg -y -video_size 1280x720 -framerate 60 -i /dev/video0 -f flv test.flv

import subprocess

subprocess.call('ffmpeg -y -video_size 1280x720 -framerate 60 -i /dev/video0 -f flv test.flv', shell=True)

