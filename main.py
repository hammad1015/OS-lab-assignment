import os
import json


def save():
    data = json.dumps(metaData).replace(' ', '')
    print(data)
    FILE.seek(0)
    FILE.write(data[:-1])
    FILE.write((maxMetaDataSize - len(data)) * ' ')
    FILE.write('}')
    FILE.seek(0)


maxMetaDataSize    = 2**10

# initialization code
if not os.path.exists('sample.data'):
    FILE     = open('sample.data', 'w+')
    metaData = {0:[],1:{}}
    save()
else:
    FILE = open('sample.data', 'r+')

# setting root and present working directory
metaData = json.loads(FILE.read(maxMetaDataSize))

holes = metaData[0]
root  = metaData[1]
PWD   = root



# system functions

def Create(*fnames):
    for fname in fnames:
        dir = fname.split('/')
        Chdir(dir)
        PWD[fname] = []
    
def Delete(*fnames):
    for fname in fnames: holes.extend(PWD[fname]); del PWD[fname]

def Mkdir(*dirs):
    for dir in dirs: PWD[dir] = {}

def Chdir(dir):
    global PWD
    PWD = PWD[dir]

def Move(dir1, dir2):
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



# CLI 
switch = {
    'create': Create,
    'delete': Delete,
    'mkdir' : Mkdir,
    'chdir' : Chdir,
    'move'  : Move,
    'open'  : Open,
    'close' : Close,
    'quit'  : quit,
}

if __name__ == '__main__':

    while True:
        try:
            stmt = input("> ").split(" ")
            case = stmt[0].lower()
            args = stmt[1:]

            save()
            switch[case](*args)
            
            
        except KeyboardInterrupt:
            print()
            break

        except Exception as e:
            print("Invalid syntax!")
            print(e)