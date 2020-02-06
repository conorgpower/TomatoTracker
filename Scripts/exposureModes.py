from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
for mode in camera.EXPOSURE_MODES:
    camera.exposure_mode = mode
    camera.annotate_text = "Exposure Mode: %s" % mode
    sleep(5)
camera.stop_preview()