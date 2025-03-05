from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
from time import sleep

class OledDisplay:
    def __init__(self):
        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial)
        self.font = ImageFont.truetype("DejaVuSans.ttf", 25)

    def showMessage(self, msg):
        x = self.device.width  
        text_width = len(msg) * 10  
        end_point = -text_width  

        while x > end_point:  
            with canvas(self.device) as draw:
                draw.text((x, 20), msg, font=self.font, fill=255)
            x -= 6  
            sleep(0.05)  
        self.clear()
        
    def clear(self):
        self.device.clear()
        self.device.show()
