import time
import subprocess

subprocess.call('mkdir -p pics', shell=True)
# ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 out.jpg
i = 0
while True:

    subprocess.call(f'ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 ./pics/pic{str(i)}_{str(time.time())}.jpg', shell=True)
    i += 1