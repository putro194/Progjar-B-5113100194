import sys
import socket
import select

HOST = 'localhost'
PORT = 10000
 
SOCKET_LIST = []
RECV_BUFFER = 4096 

def chat_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #membuat soket TCP/IP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((HOST, PORT))
    sock.listen(2)

    SOCKET_LIST.append(sock)
    print "Saluran tersambung..."

    while True:
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        for socket_n in ready_to_read:
            if socket_n == sock:
                sockfd, addr = sock.accept()
                SOCKET_LIST.append(sockfd)
                print "User (%s, %s) tersambung" % addr
                 
                broadcast(sock, sockfd, "User [%s:%s] Masuk percakapan\n" % addr)
             
            else: 
                try:
                    data = socket_n.recv(RECV_BUFFER)
                    if data:
                        broadcast(sock, socket_n, "\r" + '[Your friend] ' + data)  
                    else:
                        if socket_n in SOCKET_LIST:
                            SOCKET_LIST.remove(socket_n)

                        broadcast(sock, socket_n, "User (%s, %s) keluar percakapan\n" % addr) 

                # exception 
                except:
                    broadcast(sock, socket_n, "User (%s, %s) keluar percakapan\n" % addr)
                    continue
    sock.close()

def broadcast (sock, socket_n, message):
    for socket in SOCKET_LIST:
        if socket != sock and socket != socket_n :
            try :
                socket.send(message)
            except :
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())
