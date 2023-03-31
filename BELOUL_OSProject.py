#!/usr/bin/python3

import os
import subprocess

def command_executor(com):
    """execute commands and handle piping"""
    try:
        if "|" in com:
            f_in, f_out = (0, 0)
            f_in = os.dup(0)
            f_out = os.dup(1)
            fd_in = os.dup(f_in)

            #iteratation over all piped commands
            for cmd in com.split("|"):
                os.dup2(fd_in, 0)
                os.close(fd_in)

                #restore of fd_out
                if cmd == com.split("|")[-1]:
                    fd_out = os.dup(f_out)
                else:
                    fd_in, fd_out = os.pipe()

                #redirect fd_out to pipe
                os.dup2(fd_out, 1)
                os.close(fd_out)

                try:
                    subprocess.run(cmd.strip().split(),shell=True)
                except Exception:
                    print("error: command not found: {}".format(cmd.strip()))

            #restore of f_out f_in
            os.dup2(f_in, 0)
            os.dup2(f_out, 1)
            os.close(f_in)
            os.close(f_out)
        else:
            if "echo" not in com:
                subprocess.run(com.split(" "),shell=True)
            else:
                subprocess.run(com.split(" "))
    except Exception:
        erreur = "An error has occurred\n"
        print(erreur, file=os.sys.stderr)



def pwd():
    try:
        print(os.getcwd())
    except Exception:
        erreur = "An error has occurred\n"
        print(erreur, file=os.sys.stderr)



def cd(path):
    """convert to absolute path and change directory"""
    try:
      if(path!=" "):
        os.chdir(os.path.abspath(path))
      else:
        os.getenv("HOME")
    except Exception:
        erreur = "An error has occurred\n"
        print(erreur, file=os.sys.stderr)




def bmode(file):
    try :
        with open(file,'r') as file:

            for line in file:
                line=line.strip("\n")

                if line == "exit":
                    os._exit(0)

                elif line[:3] == "pwd":
                    pwd()

                elif line[:3] == "cd ":
                    cd(line[3:])

                elif line == "help":
                    print("sorry, no help")

                else:
                    command_executor(line)

    except:
        erreur = "An error has occurred\n"
        print(erreur, file=os.sys.stderr)






def main():
    print("$ ./mysh")
    while True:
        input1 = input("mysh$ ")
        input1=input1.strip()
        if input1 == "exit":
            os._exit(0)
        elif input1[:3] == "cd ":
            cd(input1[3:])
        elif input1[:3] == "pwd":
            pwd()
        elif input1 == "help":
            print("sorry, no help")
        elif input1[:1]=="[":
            input2=input1.strip("[")
            input3=input2.strip("]")
            bmode(input3)
        else:
            command_executor(input1)


main()