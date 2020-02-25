from picamera import PiCamera
from time import sleep

camera = PiCamera()

for i in range (5):
    # Alpha makes preview transparets for debuging
    camera.start_preview(alpha=200)
    #Sleep to allow camera brightness to adjust
    sleep(5)
    camera.capture('/home/pi/Desktop/image%s.jpg' % i)
camera.stop_preview()

# Rotate Camera 180 Degrees
# camera = PiCamera()
# camera.rotation = 180