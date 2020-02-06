from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
for modes in camera.AWB_MODES:
    camera.awb_modes = mode
    camera.annotate_text = "Mode: %s" % mode
    sleep(5)
camera.stop_preview()
