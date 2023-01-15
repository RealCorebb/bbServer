url = '/opt/mcsmanager/daemon/data/InstanceData/98a44a22da7e4b84954e6a023a15910a/logs/latest.log'

import subprocess
from adaoled import mcStatus
import textwrap

# Open the "tail" command as a subprocess
p = subprocess.Popen(["tail", "-f", url, "-n", "5"], stdout=subprocess.PIPE)

msg = ''
# Poll the subprocess for new output until it terminates
while p.poll() is None:
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
        print(wrapMsg)
        mcStatus(console=wrapMsg)
