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



# CLI 

while True:
    statement = input(">").split(" ")
    try:
        command = statement[0].lower()

        if command == "create":
            fname = statement[1]
            Create(fname)
        elif command == "delete":
            fname = statement[1]
            Delete(fname)
        elif command == "mkdir":
            dir_name = statement[1]
            Mkdir(dir_name)
        elif command == "chdir":
            dir_name = statement[1]
            Chdir(dir_name)
        elif command == "move":
            source_fname = statement[1]
            target_fname = statement[2]
            Move(source_fname, target_fname)
        elif command == "open":
            fname = statement[1]
            mode = statement[2]
            Open(fname, mode)
        elif command == "close":
            fname = statement[1]   
            Close(fname) 
    except:
        print("Invalid syntax!")