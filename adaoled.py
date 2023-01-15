import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import time
import adafruit_ssd1306

font = ImageFont.truetype('fonts/Jorolks.ttf',24)
smallJorolks = ImageFont.truetype('fonts/Jorolks.ttf',10)
seledom = ImageFont.truetype('fonts/Seledom.otf',14)
pixelCorebb = ImageFont.truetype('fonts/PixelCorebb.ttf',8)
player = Image.open('icons/steve24.png')
performance = Image.open('icons/performance.png')


# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

players = ""
cpu = 50
playerCount = 0
console = ""

def updateInfo(pl = None ,c = None ,p = None , co = None):
    global players,cpu,playerCount,console
    if pl is not None:
        players = pl
    if c is not None:
        cpu = c
    if p is not None:
        playerCount = p
    if co is not None:
        console = co
    mcStatus()


def clear():
    global image
    #image = Image.new("1", (oled.width, oled.height))
    draw.rectangle((0, 0, 128, 64), fill="black")
    oled.fill(0)

def bootLogo():
    draw.text((5, 20), "bbServer", fill="white", font = font)
    oled.image(image)
    oled.show()

def mcStatus():
    #image = Image.new("1", (oled.width, oled.height))
    clear()
    l,t,r,b = draw.multiline_textbbox((5, 20), console,font= pixelCorebb)
    draw.text((2,85-b), console, fill="white",font= pixelCorebb)
    draw.rectangle((0, 0, 128, 32), fill="black")
    draw.bitmap((69,2),player,fill="white")
    #draw.bitmap((5,5),performance,fill="white")
    draw.rounded_rectangle((2,2,25,11), radius=3, fill="white")
    draw.text((5,3), "CPU", fill="black", font = smallJorolks)
    draw.text((28,0), str(cpu)+"%", fill="white",font = seledom)
    draw.rounded_rectangle((2,16,25,25), radius=3, fill="white")
    draw.text((5,17), "TPS", fill="black", font = smallJorolks)
    draw.text((28,14), str(players), fill="white",font = seledom)
    draw.text((98,5), str(playerCount), fill="white",font= font)
    oled.image(image)
    oled.show()

def startup():
    bootLogo()
    time.sleep(1)
    clear()
    mcStatus()

if __name__ == "__main__":  
    startup()
