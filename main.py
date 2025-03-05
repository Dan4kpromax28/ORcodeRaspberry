import cv2
from pyzbar.pyzbar import decode
from picamera2 import Picamera2, Preview
from libcamera import controls
from libcamera import Transform


picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
config = picam2.create_preview_configuration(main={"size": (640, 480)}, transform=Transform(hflip=True, vflip=True)) # tas ir domats testesanai
picam2.configure(config)
picam2.start()

picam2.set_controls({"AfMode": 2, "AfTrigger": 0})

barcodes = []
correctCode = ""

while True:
    captureRGB = picam2.capture_array("main")
    barcodes = decode(captureRGB)
    if barcodes: 
        for character in barcodes:
            correctCode = character.data.decode("utf-8")
    print(f"Kods ir {correctCode}")
