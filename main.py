import cv2
from picamera2 import Picamera2
import os
from libcamera import controls
picam2 = Picamera2()
os.system("v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0")
picam2.preview_configuration.main.size = (640,480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast})
picam2.start()

qr= cv2.QRCodeDetector()
while True:
    image = picam2.capture_array()
    data, points, _ = qr.detectAndDecode(image)
    if points is not None:
        print("QR Code detected: ", data)
    cv2.imshow("Camera", image)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
picam2.stop()
