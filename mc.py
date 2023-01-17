url = '/opt/mcsmanager/daemon/data/InstanceData/98a44a22da7e4b84954e6a023a15910a/logs/latest.log'

import subprocess
import threading
import time
from adaoled import mcStatus, updateInfo , event , startup , startLoop
import textwrap
import psutil
from mcstatus import JavaServer
from neopixel import rainbow,black,redFastBlink

startup()
startLoop()
def getMC():
    print('start MC Monitor')
    while True:
        server = JavaServer.lookup("127.0.0.1:25565")
        status = server.status()
        query = server.query()
        #print(status.players.online)
        #print(query.players.names)
        updateInfo(p=status.players.online,pl='  '.join(query.players.names))
        time.sleep(5)

def getCPU():
    print('start CPU Monitor')
    while True:
        cpu = int(psutil.cpu_percent(interval=1))
        updateInfo(c=cpu)
        time.sleep(1)

def neopixel(type):
    print('start Neopixel')
    if(type == 'join'):
        for i in range(0, 300):
            rainbow.animate()
            time.sleep(0.01)
    elif(type == 'kill'):
        for i in range(0, 200):
            redFastBlink.animate()
            time.sleep(0.01)
    black.animate()


#create a thread to get cpu usage
cpuThread = threading.Thread(target=getCPU)
cpuThread.start()
mcThread = threading.Thread(target=getMC)
mcThread.start()

# Open the "tail" command as a subprocess
p = subprocess.Popen(["tail", "-f", url, "-n", "5"], stdout=subprocess.PIPE)
msg = ''
# Poll the subprocess for new output until it terminates
while p.poll() is None:
    data = p.stdout.readline().decode("utf-8").split(']:')
    if (len(data) > 1):
        line = data[1]
        if line:
            if('joined the game' in line):
                neoThread = threading.Thread(target=neopixel('join'))
                neoThread.start()
                event('player16',line.split('joined the game')[0] + '加入了游戏')
            elif('was slain by' in line):
                neoThread = threading.Thread(target=neopixel('kill'))
                neoThread.start()
                event('player16',line.split('was slain by')[0] + '被杀掉了')
            elif('fell from a high place' in line):
                neoThread = threading.Thread(target=neopixel('kill'))
                neoThread.start()
                event('player16',line.split('fell from a high place')[0] + '摔死了')

            msg += line
    if(len(msg.splitlines())>=5):
        msg = msg.split('\n', 1)[1]
        wrapMsg = textwrap.fill(msg,width=42,replace_whitespace=False)
        updateInfo(co = wrapMsg)
