import os
import pickle


def save():
    data = pickle.dumps(metaData)
    SSD.seek(0)
    SSD.write(data)
    SSD.write((maxMetaDataSize - len(data)) * b' ')

maxMetaDataSize    = 2**10

# initialization code
if not os.path.exists('sample.data'):
    SSD      = open('sample.data', 'wb+')
    metaData = {0:[],1:{}}
    save()
else:
    SSD      = open('sample.data', 'rb+')
    metaData = pickle.loads(SSD.read(maxMetaDataSize))


# setting root and present working directory
holes = metaData[0]
root  = metaData[1]
pwd   = root
path  = []


# system functions

def create(*fnames):
    for fname in fnames: pwd[fname] = []

def mkdir(*dirs):
    for dir in dirs: pwd[dir] = {}
    
def delete(*fnames):
    for fname in fnames: holes.extend(pwd[fname]); del pwd[fname]

def chdir(pth):
    global path, pwd
    
    pth  = pth.split('/')
    rel  = pth[0] in pwd
    curr = pwd if rel else root

    for d in pth: curr = curr[d]

    path = path + pth if rel else pth
    pwd  = curr

def move(fname, pth):
    file = pwd[fname]
    lpth = '/'.join(path)
    chdir(pth)
    pwd[fname] = file
    chdir(lpth)
    delete(fname)

def tree(depth= 1):
    pass

class stream():

    def __init__(self, locs):
        self.locs = locs

    def read(self, start= 0, size= -1):
        for i,s in self.locs[::2]:
            if start < s:
                SSD.seek(start)
                SSD.read()




# CLI 
switch = {
    ''      : lambda: [0],
    'quit'  : lambda: [save(), print(), exit()],
    'pwd'   : lambda: [print('~/'+'/'.join(path))],
    'ls'    : lambda: [print(*pwd, sep= '\t')],
    'touch' : create,
    'rm'    : delete,
    'mkdir' : mkdir,
    'cd'    : chdir,
    'mv'    : move,

 #   'open'  : Open,
 #   'close' : Close,
}

if __name__ == '__main__':

    while True:
            
        save()
        stmt = input('£ ').split(' ')
        case = stmt[0]
        args = stmt[1:]

        try:switch[case](*args)
        
        except (KeyboardInterrupt, EOFError): print(); exit()
        except KeyError  as e               : print(e, 'command not found')
        except Exception as e               : print(type(e))
