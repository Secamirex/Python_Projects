import socket
import sys



def getBanner(host,port):

    try:
        socket.setdefaulttimeout(5)
        s = socket.socket()
        s.connect_ex((host,port))
        banner = s.recv(1024)
        return banner

    except:
        sys.exit(0)




def main():
    host = input('Enter the host IP: ')
    for port in range(1,1024):
        banner = getBanner(host,port)
        if banner:
            print("[+] " + host + ": " + str(banner.decode(encoding='utf-8')))
    else:
        print("Banner was not captured!")
main()

