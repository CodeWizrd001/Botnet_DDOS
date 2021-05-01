import random

def ipGen() :
    ip = ['1','1','1','1']
    for _ in range(4):
        ip[_] = str(random.randint(1,255))
    return '.'.join(ip)
