from pyzbar.pyzbar import decode
from picamera2 import Picamera2, Preview
from libcamera import Transform
import time
from oledDi import OledDisplay
from relay import Relay
from supabaseMod import SupabaseMod

def initialization():
    supabase = SupabaseMod()
    display = OledDisplay()
    firstRelay = Relay()
    return supabase, display, firstRelay

def cameraConfig():
    picam2 = Picamera2()
    picam2.start_preview(Preview.QTGL)
    config = picam2.create_preview_configuration(main={"size": (640, 480)}, transform=Transform(hflip=True, vflip=True)) # tas ir domats testesanai
    picam2.configure(config)
    picam2.start()
    picam2.set_controls({"AfMode": 2, "AfTrigger": 0})
    return picam2

def decodedQr(picam2):
    captureRGB = picam2.capture_array("main")
    return decode(captureRGB)

def checkCode(newBarcodes, correctCode, display, firstRelay):
    if newBarcodes and newBarcodes[0].data.decode("utf-8") == correctCode and supabase.checkCodeInDatabase(correctCode):
        display.showMessage("Laipni lūdzam")
        firstRelay.onOff()
        time.sleep(delayAfter)
    else:
        display.showMessage("Kods nav derīgs")
        

supabase, display, firstRelay = initialization()
picam2 = cameraConfig()

barcodes = []
correctCode = ""
delay = 1
delayAfter = 2
lastCode = None


try:
    while True:
        barcodes.clear()
        barcodes = decodedQr(picam2)
        if barcodes: 
            correctCode = barcodes[0].data.decode("utf-8")
            if lastCode != correctCode:
                time.sleep(delay)
                newBarcodes = decodedQr(picam2)
                print(newBarcodes,barcodes)
                checkCode(newBarcodes, correctCode, display, firstRelay)
                newBarcodes.clear()
except KeyboardInterrupt:
    display.showMessage("Programma tika apturēta")
finally:
    picam2.stop()
    display.clear()


  
    


                 
        
                    
            
            
