 
import os
import sys
import socket
from termcolor import colored

host =  input("[*]Enter the host IP to scan: ")

tcp =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.setdefaulttimeout(3)

def main():
    for port in range (1,1024):
        if tcp.connect_ex((host,port))==0:
            print(colored("[+] port {} is open.".format(port),'green'))
        else:
            print(colored("[-] port {} is closed.".format(port),'red'))
main()