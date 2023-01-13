from luma.emulator.device import pygame
from luma.core.render import canvas
from PIL import ImageFont, Image , ImageDraw
import time
font = ImageFont.truetype('fonts/Jorolks.ttf',24)
smallJorolks = ImageFont.truetype('fonts/Jorolks.ttf',10)
seledom = ImageFont.truetype('fonts/Seledom.otf',14)
pixelCorebb = ImageFont.truetype('fonts/PixelCorebb.ttf',7)
device = pygame( transform='none',scale=4)

def bootLogo():
    with canvas(device) as draw:
        #draw image
        draw.text((5, 20), "bbServer", fill="white", font = font)
        

tps = 20
cpu = 50
playerCount = 0

def mcStatus():
    global playerCount
    with canvas(device) as draw:
        player = Image.open('icons/steve24.png')
        performance = Image.open('icons/performance.png')
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
        #draw rounded rectangle
        


bootLogo()
#time.sleep(3)
mcStatus()
while True:
    if(playerCount < 99):
        playerCount += 1
    else:
        playerCount = 0
    print('loop')
    mcStatus()