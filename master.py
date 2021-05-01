from utils.socks import Master , Log

slaves = ["192.168.175."+str(i) for i in range(1,255)]

print("Slave List Created")

master = Master(slaves=slaves)

def showHelp() :
    print("""
        ping - To check available machines
        kill - To Stop all slaves
        exit - To exit master
        help - To display this help
    """)

try :
    while True :
        cmd = input(">>> ")
        if cmd == "ping" :
            master.ping()
        elif cmd == "help" :
            showHelp()
        elif cmd == "kill" :
            print(Log("Killing Slaves"))
            master.killSlaves()
        elif cmd == "up" :
            print(master.up)
        elif cmd == "exit" :
            print(Log("Stopping Master"))
            exit(0)
        else :
            print("Unrecognized Command")
            print("Try")
            showHelp()
except KeyboardInterrupt :
    print(Log("Keyboard Interrupt Received"))
    print(Log("Exiting Master"))