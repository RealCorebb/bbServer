from luma.emulator.device import pygame
from luma.core.render import canvas
from PIL import ImageFont, Image , ImageDraw
import time
font = ImageFont.truetype('Jorolks.ttf',24)
smallJorolks = ImageFont.truetype('Jorolks.ttf',8)

device = pygame()

def bootLogo():
    with canvas(device) as draw:
        #draw image
        draw.text((5, 20), "bbServer", fill="white", font = font)
        

tps = 20
cpu = 0
playerCount = 0

def mcStatus():
    global playerCount
    with canvas(device) as draw:
        player = Image.open('icons/steve24.png')
        performance = Image.open('icons/performance.png')
        draw.bitmap((60,5),player,fill="white")
        #draw.bitmap((5,5),performance,fill="white")
        draw.text((5,5), "CPU", fill="white", font = smallJorolks)
        draw.text((5,15), "TPS", fill="white", font = smallJorolks)
        draw.text((90,5), str(playerCount), fill="white",font= font)

bootLogo()
time.sleep(3)
mcStatus()
while True:
    if(playerCount < 99):
        playerCount += 1
    else:
        playerCount = 0
    print('loop')
    mcStatus()