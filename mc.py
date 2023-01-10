url = 'F:\server\logs\latest.log'

import subprocess

# Open the "tail" command as a subprocess
p = subprocess.Popen(["tail", "-f", url], stdout=subprocess.PIPE)

# Poll the subprocess for new output until it terminates
while p.poll() is None:
    line = p.stdout.readline()
    if line:
        print(line.strip())