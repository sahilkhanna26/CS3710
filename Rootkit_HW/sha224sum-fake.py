#!/usr/bin/python3
import sys
import subprocess

def main():
    args1 = sys.argv
    print("God is real … unless declared integer.")
    if ("--be-evil" in args1):
        print("my name is jeff")
    
        args1.remove("--be-evil")
    args2 = []
    args2.append("/usr/bin/sha224sum.original")
    for item in args1:
        args2.append(item)
    subprocess.run(args2)
       
    


if __name__ == '__main__':
    main()
    
