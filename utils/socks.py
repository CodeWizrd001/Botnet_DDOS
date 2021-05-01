import time 
import socket
import threading
from threading import Thread

def Log(event) :
    return "[{}] {}".format(time.ctime(),event)

class Server :
    def __init__(self,addr=('0.0.0.0',10000)) :
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ReadBuffer = 8192
        self.addr = addr
        self.sock.bind(addr)
        self.running = True
    def start(self) :
        self.sock.listen(50)
        print(Log("Listening At {}:{}".format(self.addr[0],self.addr[1])))
        while self.running :
            cl , addr = self.sock.accept()
            # print(Log("Accepted connection from {}:{}".format(addr[0],addr[1])))
            self.handle_accepted(cl,addr)
    def handle_accepted(self,cl,addr) :
        """
        Currently handling "parallelism" by multithreading"""
        thread = Thread(target=self.handle_io,args=(cl,addr,))
        thread.start()
    def handle_io(self,cl,addr) :
        """
        Should Be Overridden in child class
        Or Will Funcion as Echo server"""
        client = cl 
        client.send('Welcome\n'.encode())
        while True :
            try :
                client.send(">>> ".encode())
                a = client.recv(self.ReadBuffer)
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


class ServerFarm :
    def __init__(self) :
        self.created = time.ctime()
    def create(self,port) :
        server = Server(('0.0.0.0',port))
        server.start()
    def start(self,port) :
        th = Thread(target=self.create,args=(port,))
        th.start()
    def startrange(self,port_start,port_end) :
        for port in range(port_start,port_end) :
            th = Thread(target=self.create,args=(port,))
            th.start()


class Client :
    def __init__(self,ip='0.0.0.0',port=8000) :
        addr = (ip,port)
        self.addr = addr 
        self.cl = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ReadBuffer = 8192
    def start(self) :
        print(self.addr)
        self.cl.connect(self.addr) 
        self.handle_connected()
    def handle_connected(self) :
        """
        To Be Overloaded
        In The Derived Class
        """
        print(Log("Connection Was Made"))
        self.cl.close()

class Master :
    def __init__(self,slaves = []) :
        print(Log("Master Initialization Started"))
        if len(slaves) > 255 :
            raise Exception("Master Cannot Handle More Than 255 Slaves Currently")
        self.slaves = slaves
        self.socks = []
        self.up = []
        self.bPort = 60000
        self.ReadBuffer = 4096
        print(Log("Creating Slave Connections"))
        for slave in slaves :
            self.socks.append(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
        print(Log("Master Online"))
        print(Log("Checking Slaves"))
        self.ping()

    def upCheck(self,sock,slave) :
        port = self.bPort
        try :
            # print(Log(f"Trying To Connect To {slave}"))
            sock.settimeout(3)
            sock.connect((slave,port))
            print(Log(f"{slave} is up"))
            self.up.append(slave)
            sock.send("ping".encode())
            sock.close()
            self.socks[self.slaves.index(slave)] = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.timeout:
            # print(Log(f"{slave} is down"))
            pass
        except Exception as e :
            print(Log(f"Error {slave} {port} {e}"))
            
    def ping(self) :
        self.up = []
        port = self.bPort
        threads = []
        for i in range(len(self.socks)) :
            sock = self.socks[i]
            slave = self.slaves[i]
            t = Thread(target=self.upCheck,args=(sock,slave,))
            t.start()
            threads.append(t)
        for thread in threads :
            thread.join()
    
    def kill(self,sock,slave) :
        port = self.bPort
        try :
            print(Log(f"Connecting {slave}"))
            sock.settimeout(3)
            sock.connect((slave,port))
            print(Log(f"Killing {slave}"))
            sock.send("kill".encode())
            sock.send("kill".encode())
            sock.close()
            self.socks[self.slaves.index(slave)] = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.timeout:
            pass
        except Exception as e :
            print(Log(f"Error {slave} {port} {e}"))

    def killSlaves(self) :
        port = self.bPort
        print(self.up)
        threads = []
        for slave in self.up :
            sock = self.socks[self.slaves.index(slave)]
            t = Thread(target=self.kill,args=(sock,slave,))
            t.start()
            threads.append(t)
        for thread in threads :
            thread.join()

    def updateSlaves(self,slaves) :
        self.slaves = slaves
        for sock in self.socks :
            del sock
        del self.socks 
        self.socks = []
        for slave in slaves :
            self.socks.append(socket.socket(socket.AF_INET,socket.SOCK_STREAM))