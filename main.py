import cv2
from pyzbar.pyzbar import decode
from picamera2 import Picamera2, Preview
from libcamera import controls
from libcamera import Transform
import time
from oledDi import OledDisplay

display = OledDisplay();

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
config = picam2.create_preview_configuration(main={"size": (640, 480)}, transform=Transform(hflip=True, vflip=True)) # tas ir domats testesanai
picam2.configure(config)
picam2.start()

picam2.set_controls({"AfMode": 2, "AfTrigger": 0})

barcodes = []
correctCode = ""
delay = 2.5
delayAfter = 4
lastCode = None

while True:
    captureRGB = picam2.capture_array("main")
    barcodes = decode(captureRGB)
    if barcodes: 
        correctCode = barcodes[0].data.decode("utf-8")
        if lastCode != correctCode:
            print(f"Jaunais kods ir: {correctCode}")
            display.showMessage(f"Jaunais kods ir: {correctCode}")
            time.sleep(delay)
            
            captureRGB = picam2.capture_array("main")
            newBarcodes = decode(captureRGB)
            
            if newBarcodes and newBarcodes[0].data.decode("utf-8") == correctCode:
                print(f"Kods: {correctCode} ir pareizs")
                time.sleep(delayAfter)
            else:
                print(f"notika kluda")
                
        
                    
            
            
