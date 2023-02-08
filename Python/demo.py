import threading
import board
import neopixel_spi
from PIL import Image, ImageDraw, ImageFont
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE, WHITE, AMBER, JADE, MAGENTA, ORANGE , BLACK , RED
import adafruit_ssd1306
import time
import psutil
import pathlib
dirPath = str(pathlib.Path(__file__).parent.resolve())
font = ImageFont.truetype(dirPath+'/fonts/Jorolks.ttf',24)
smallJorolks = ImageFont.truetype(dirPath+'/fonts/Jorolks.ttf',12)
seledom = ImageFont.truetype(dirPath+'/fonts/Seledom.otf',14)
bigSeledom = ImageFont.truetype(dirPath+'/fonts/Seledom.otf',33)
pixelCorebb = ImageFont.truetype(dirPath+'/fonts/PixelCorebb.ttf',15)
pixelCorebbBig = ImageFont.truetype(dirPath+'/fonts/PixelCorebb.ttf',14)
player = Image.open(dirPath+'/icons/steve24.png')
player16 = Image.open(dirPath+'/icons/steve16.png')
performance = Image.open(dirPath+'/icons/performance.png')


# ------------------- WS2812 RGB LED  -_,- ------------------

# Update to match the pin connected to your NeoPixels
pixel_pin = board.SPI()
# Update to match the number of NeoPixels you have connected
pixel_num = 40

pixels = neopixel_spi.NeoPixel_SPI(pixel_pin, pixel_num, brightness=0.1, auto_write=False)

blink = Blink(pixels, speed=0.5, color=JADE)
redFastBlink = Blink(pixels, speed=0.1, color=RED)
colorcycle = ColorCycle(pixels, speed=0.4, colors=[MAGENTA, ORANGE])
comet = Comet(pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=WHITE)
pulse = Pulse(pixels, speed=0.1, period=3, color=AMBER)
sparkle = Sparkle(pixels, speed=0.1, color=PURPLE, num_sparkles=10)
solid = Solid(pixels, color=JADE)
black = Solid(pixels, color = BLACK)
rainbow = Rainbow(pixels, speed=0.1, period=2)
sparkle_pulse = SparklePulse(pixels, speed=0.1, period=3, color=JADE)
rainbow_comet = RainbowComet(pixels, speed=0.05, tail_length=15, bounce=True)
rainbow_chase = RainbowChase(pixels, speed=0.1, size=3, spacing=2, step=8)
rainbow_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)
custom_color_chase = CustomColorChase(
    pixels, speed=0.1, size=2, spacing=3, colors=[ORANGE, WHITE, JADE]
)


animations = AnimationSequence(
    comet,
    blink,
    rainbow_sparkle,
    chase,
    pulse,
    sparkle,
    rainbow,
    solid,
    rainbow_comet,
    sparkle_pulse,
    rainbow_chase,
    custom_color_chase,
    advance_interval=5,
    auto_clear=True,
)

# ------------------------------------

# ------------------- SSD1306/SSD1309 OLED  -_,- ------------------
oled = None

# Create blank image for drawing.
image = Image.new("1", (128, 64))
draw = ImageDraw.Draw(image)

def clear():
    global image
    #image = Image.new("1", (oled.width, oled.height))
    draw.rectangle((0, 0, 128, 64), fill="black")
    oled.fill(0)

def bootLogo():
    draw.text((5, 20), "bbServer", fill="white", font = font)
    oled.image(image)
    oled.show()

def updateInfo():
    global oled
    i2c = board.I2C()  # uses board.SCL and board.SDA
    attempts = 0
    while attempts < 5:
        try:
            oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
            break
        except:
            attempts += 1
            print('OLED not found, retrying...')
            time.sleep(1)
        
    # Clear display.
    oled.fill(0)
    oled.rotate(False)
    oled.show()
    clear()
    bootLogo()
    time.sleep(1)
    while True:
        cpu = int(psutil.cpu_percent(interval=1))
        ram = int(psutil.virtual_memory().percent)
        timeNow = time.strftime("%H:%M")
        
        clear()
        draw.rounded_rectangle((2,2,28,12), radius=3, fill="white")
        draw.text((5,3), "CPU", fill="black", font = smallJorolks)
        draw.text((32,0), str(cpu)+"%", fill="white",font = pixelCorebb)
        draw.rounded_rectangle((67,2,96,12), radius=3, fill="white")
        draw.text((70,3), "RAM", fill="black", font = smallJorolks)
        draw.text((100,0), str(ram)+"%", fill="white",font = pixelCorebb)
        draw.text((2,24), timeNow, fill="white",font = bigSeledom)
        oled.image(image)
        oled.show()
        time.sleep(1)
# ------------------------------------

if __name__ == "__main__":
    oledThread = threading.Thread(target=updateInfo)
    oledThread.start()
    while True: 
        time.sleep(0.01)
        animations.animate()
