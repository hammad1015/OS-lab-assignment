import os
import pickle
import re


def save():
    data = pickle.dumps(metaData)
    SSD.seek(0)
    SSD.write(data)
    SSD.write((maxMetaDataSize - len(data)) * b' ')


# initialization code
maxMetaDataSize = 2**10
if not os.path.exists('sample.data'):
    SSD      = open('sample.data', 'wb+')
    metaData = {'h':[],'~':{}}
    save()
else:
    SSD      = open('sample.data', 'rb+')
    metaData = pickle.loads(SSD.read(maxMetaDataSize))


# setting root and present working directory
holes = metaData['h']
root  = metaData['~']
PATH  = '~'


# system functions

def dir(path):

    curr = metaData
    path = path if path.startswith('~') else f'{PATH}/{path}' if path else PATH
    path = path.split('/')

    temp = ''
    for i, d in enumerate(path):
        assert ((d in curr) and (type(curr[d]) is dict)),  f'{"/".join(path[:i+1])}: No such file or directory'
        curr = curr[d]

    return curr

def split(paths):

    paths = [ e.split('/')      for e in paths ]
    names = [ e[-1]             for e in paths ]
    paths = [ '/'.join(e[:-1])  for e in paths ]

    return paths, names

def create(*pfnames):
    paths, fnames = split(pfnames)

    for path, fname in zip(paths, fnames):
        dir(path)[fname] = []  

def mkdir(*pdnames):
    paths, dnames = split(pdnames)

    for path, dname in zip(paths, dnames):
        dir(path)[dname] = {}

def delete(*pfnames):
    paths, fnames = split(pfnames)

    for path, fname in zip(paths, fnames):
        holes.extend(dir(path)[fname])
        del dir(PATH)[fname]

def chdir(path):
    global PATH
    
    dir(path)
    PATH = path if path.startswith('~') else PATH + '/' + path

def move(fname, path):
    
    dir(path)[fname] = dir(PATH)[fname]
    del dir(PATH)[fname]

def tree(depth= 1):
    pass

def read(path, frm= 0, size= -1):
    f = file(path)
    f.seek(frm)
    print(f.read(size))
    print()
    f.close()

def write(path, text):
    f = file(path)
    f.write(text)
    f.close()


def help():
    print(
        "Usage: command [argument]\n"
        "rm [file/folder path] usage: removes file or directory\n"
        "touch [file path] usage: creates file\n"
        "mkdir [directory name] usage: creates directory\n"
        "mv [source directory] [target directory] usage: move file\n"
        "cat [file path] usage: read file\n"
        "wrt [file path] [input data] usage: write to file\n"
        "cd [path] usage: change working directory\n"
        "pwd usage:\n"
        "dump usage:\n"
        "ls usage: list files and folders in current directory\n"
        "quit usage: exit the file system\n"
    )


class file():

    def __init__(self, path):
        path, fname = split([path])
        path, fname = path[0], fname[0]

        self.chunks = dir(path)[fname]
        self.data   = b''
        self.ptr    = 0

        for i,s in self.chunks:
            SSD.seek(i)
            self.data += SSD.read(s) 

        self.size = len(self.data)
            


    def seek(self, pos):
        if pos == -1: pos = self.size
        assert pos <= self.size, f'File pointer out of range. File size is {self.size}'
        self.ptr = pos

    def tell(self):
        return self.ptr

    def read(self, size= -1):
        start = self.ptr
        end   = -1 if (size == -1) else start + size
        self.seek(end)
        return self.data[start: end]

    def write(self, data):
        
        while data:
            if holes:
                i, s = holes.pop()
                if s > len(data): 
                    holes.append([i+len(data), s-len(data)])

                towrite = data[:s].encode()
                data = data[s:]
        
            else:
                i = SSD.seek(0, 2)
                s = len(data)

                towrite = data.encode()
                data = ''

            i = SSD.seek(i)
            s = SSD.write(towrite)
            self.chunks.append([i, s])


    def close(self):
        del self


# CLI 

#PS1 = '£ '
PS1 = '¥ '
#PS1 = '• '

switch = {
    ''      : lambda: [0],
    'quit'  : lambda: [save(), print(), exit()],
    'pwd'   : lambda: [print(PATH)],
    'ls'    : lambda: [print(*dir(PATH), sep= '\t')],
    'touch' : create,
    'rm'    : delete,
    'mkdir' : mkdir,
    'cd'    : chdir,
    'mv'    : move,
    'cat'   : read,
    'wrt'   : write,
    'help'  : help,
    'dump'  : lambda : print(metaData)
}

if __name__ == '__main__':

    while True:
            
        save()
        stmt = input(PS1).split(' ')
        case = stmt[0]
        args = stmt[1:]

        try:switch[case](*args)
        
        except (KeyboardInterrupt, EOFError): print(); exit()
        except AssertionError as e          : print(e)
        except KeyError  as e               : print(e, 'command not found')
        #except Exception as e               : print(type(e))
