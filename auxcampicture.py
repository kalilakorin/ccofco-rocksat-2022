import time
import subprocess

subprocess.call('mkdir -p pics', shell=True)
# ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 out.jpg
for i in range(0,69):

    subprocess.call(f'ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 ./pics/Pic{str(i)}{str(time.time())}.jpg', shell=True)
