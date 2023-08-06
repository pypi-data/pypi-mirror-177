#!/bin/bash

from blendedUx.blendedcli.blendedcli import * 
import os
import sys
from signal import signal, SIGINT
import logging

# define our clear function
def clear():
 
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

# Restart to return script back to initial state. 
def restart():
    logging.getLogger('').handlers.clear()
    
# Handle CTRL+C command
def handler(sig, frame):
    restart()

# making sure executable is present in path
def add_to_path(exe_path):
    if exe_path not in os.environ['PATH'] : 
        os.environ['PATH'] = exe_path + os.pathsep + os.environ['PATH']

def run_command(cmd, inLoop=True):
    cmd = [elem.strip() for elem in cmd.split()]

    if len(cmd) == 1 :
        restart() 
    
    if cmd[0] == 'bd':
        # Listens for ctrl+c in MainThread and Once found call `:meth:` handler 
        try : 
            main(cmd[1:])
        except SystemExit:
            if inLoop: restart()
    else:
        os.system(' '.join(cmd))    
    if inLoop: restart()



if __name__ == '__main__':
    
    # add to PATH variable
    if sys.executable.endswith('.exe') : 
        add_to_path( os.path.dirname(sys.executable))
    
    # When used from cmd prompt
    if len(sys.argv) >= 2:
        run_command('bd ' + ' '.join(sys.argv[1:]), inLoop=False)
        
    else:
        while True:
            cmd = input('\n> ')
            if cmd == 'clear' : 
                clear()
                continue
            run_command(cmd)