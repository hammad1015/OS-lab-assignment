import os
import json


def save(data):
    metaData = json.dumps(data)
    FILE.seek(0)
    FILE.write(metaData[:-1])
    FILE.write((maxMetaDataSize - len(metaData)) * ' ')
    FILE.write('}')
    FILE.seek(0)


maxMetaDataSize    = 2**10

if not os.path.exists('sample.data'):
    FILE = open('sample.data', 'w+')
    save({})
else:
    FILE = open('sample.data', 'r+')


root = FILE.read(maxMetaDataSize)
root = json.loads(root)

CWD  = root

def Create(fname):
    CWD[fname] = [[]]
    

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