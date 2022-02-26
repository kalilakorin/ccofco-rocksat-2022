# Skyler Puckett
#
# ffmpeg -y -video_size 1280x720 -framerate 60 -i /dev/video0 -f flv test.flv
# ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 out.jpg

import subprocess

subprocess.call('ffmpeg -y -video_size 1280x720 -framerate 60 -i /dev/video0 -f flv test.flv', shell=True)

