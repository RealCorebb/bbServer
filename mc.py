url = '/opt/mcsmanager/daemon/data/InstanceData/98a44a22da7e4b84954e6a023a15910a/logs/latest.log'

import subprocess
import threading
import time
from adaoled import mcStatus, updateInfo
import textwrap
import psutil
from mcstatus import JavaServer

def getMC():
    print('start MC Monitor')
    while True:
        server = JavaServer.lookup("127.0.0.1:25565")
        status = server.status()
        query = server.query()
        updateInfo(p=status.players.online,pl='  '.join(query.players.names))
        time.sleep(5)

def getCPU():
    print('start CPU Monitor')
    while True:
        cpu = int(psutil.cpu_percent(interval=1))
        updateInfo(c=cpu)
        time.sleep(1)

#create a thread to get cpu usage
cpuThread = threading.Thread(target=getCPU)
cpuThread.start()


# Open the "tail" command as a subprocess
p = subprocess.Popen(["tail", "-f", url, "-n", "5"], stdout=subprocess.PIPE)
msg = ''
# Poll the subprocess for new output until it terminates
while p.poll() is None:
    print('start Log Monitor')
    data = p.stdout.readline().decode("utf-8").split(']:')
    if (len(data) > 1):
        line = data[1]
        #print(line)
        if line:
            #print('\n' in line)
            msg += line
            #print(msg)
    #print(len(msg.split('\n')))
    #print (len(msg.splitlines()))
    if(len(msg.splitlines())>=5):
        msg = msg.split('\n', 1)[1]
        #print(msg)
        wrapMsg = textwrap.fill(msg,width=42,replace_whitespace=False)
        #print(wrapMsg)
        updateInfo(co = wrapMsg)
        #mcStatus(console=wrapMsg)
