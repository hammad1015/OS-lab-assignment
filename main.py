import os
import json

root = json.load(open('sample.data'))
CWD  = root


def Create(fname):
    CWD[fname] = ''
    

def Delete(fname):
    del CWD[fname]

def Mkdir(dir):
    CWD[dir] = {}

def Chdir(dir):
    global CWD
    CWD = CWD[dir]

def Move():
    pass

def Open(fname, mode= 'w'):
    pass

def Close():
    pass



'''
def ():
    pass

def ():
    pass

def ():
    pass

def ():
    pass

def ():
    pass
'''