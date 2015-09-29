import sys
import socket
import select
#HOST = 'localhost'
#PORT = 10000
def chat_client():
if(len(sys.argv) < 3) :
print 'perintah koneksi salah...'
sys.exit()
HOST = sys.argv[1]
PORT = int(sys.argv[2])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)
try :
sock.connect((HOST, PORT))
except :
print 'Gagal tersambung !'
sys.exit()
print 'Selamat datang pada saluran chatting...'
sys.stdout.write('[Me] ');
sys.stdout.flush()
while True:
socket_list = [sys.stdin, sock]
ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
for socket_n in ready_to_read:
if socket_n == sock:
data = socket_n.recv(2048)
if not data :
print '\nServer diputus...'
sys.exit()
else :
sys.stdout.write(data)
sys.stdout.write('[Me] ')
sys.stdout.flush()
else :
msg = sys.stdin.readline()
sock.send(msg)
sys.stdout.write('[Me] ')
sys.stdout.flush()
if __name__ == "__main__":
sys.exit(chat_client())
