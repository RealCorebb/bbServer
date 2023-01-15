from luma.core.render import canvas
from PIL import ImageFont, Image , ImageDraw
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1309
from time import sleep
import threading

serial = i2c(port=5, address=0x3C)

font = ImageFont.truetype('fonts/Jorolks.ttf',24)
smallJorolks = ImageFont.truetype('fonts/Jorolks.ttf',10)
seledom = ImageFont.truetype('fonts/Seledom.otf',14)
pixelCorebb = ImageFont.truetype('fonts/PixelCorebb.ttf',7)
device = ssd1309(serial)

def bootLogo():
    #draw image
    with canvas(device) as draw:
        draw.text((5, 20), "bbServer", fill="white", font = font)
    sleep(1)

def bootLogo2():
    #draw image
    with canvas(device) as draw:
        draw.text((5, 20), "bbTown", fill="white", font = font)
    sleep(1)
        

tps = 20
cpu = 50
playerCount = 0

def mcStatus():
    global playerCount
    player = Image.open('icons/steve24.png')
    performance = Image.open('icons/performance.png')
    with canvas(device) as draw:  
        draw.bitmap((69,2),player,fill="white")
        #draw.bitmap((5,5),performance,fill="white")
        draw.rounded_rectangle((2,2,25,11), radius=3, fill="white")
        draw.text((5,3), "CPU", fill="black", font = smallJorolks)
        draw.text((28,0), str(cpu)+"%", fill="white",font = seledom)
        draw.rounded_rectangle((2,16,25,25), radius=3, fill="white")
        draw.text((5,17), "TPS", fill="black", font = smallJorolks)
        draw.text((28,14), str(tps), fill="white",font = seledom)
        draw.text((98,5), str(playerCount), fill="white",font= font)
        draw.text((20,50), "Corebb killed Foambb 哈哈", fill="white",font= pixelCorebb)
    sleep(10)
    #draw rounded rectangle

def main():
    while True:
        bootLogo()
        time.sleep(5)
    #bootLogo()
    #bootLogo2()
    #mcStatus()

if __name__ == "__main__":     
    try:
        main()
    except KeyboardInterrupt:
        pass
'''
    #threading.Timer(3.0, mcStatus(draw))
    #mcStatus(draw)
    #time.sleep(3)
    while True:
        if(playerCount < 99):
            playerCount += 1
        else:
            playerCount = 0
        time.sleep(100)
        mcStatus(draw)
        '''

