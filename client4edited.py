import socket, select, string, sys

name = []
HOST = 'localhost'
PORT = 9999

if __name__ == "__main__":
	
	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_sock.settimeout(2)

	try:
		client_sock.connect((HOST, PORT))
	except:
		print "Gagal tersambung!"
		sys.exit()


	print "Login"
	sys.stdout.write('Username : ')
	sys.stdout.flush()

	
	name = sys.stdin.readline().rstrip('\n')
	a = ("UN", name)
	b = ' '
	c = b.join(a)
	client_sock.send(c)

	flag = "gas..."
	data1 = client_sock.recv(4096)
	if flag != str(data1):
		sys.stdout.write(data1)
		print "\rUser meninggalkan percakapan...\n"
		sys.exit()

	print "Selamat datang pada ruang percakapan... 		200-OK"
	print "Ketik 'help' untuk membantumu."
	sys.stdout.write('<'+name+'> : ')
	sys.stdout.flush()

	while True:
		socket_list = [sys.stdin, client_sock]
		ready_to_read,ready_to_write,in_error = select.select(socket_list, [], [])
	
		for sock in ready_to_read:
			if sock == client_sock:
				data2 = sock.recv(4096)
				if not data2 :
					print '\nSaluran server diputus!'
					sys.exit()
				else :
					sys.stdout.write(data2)
					sys.stdout.write('<'+name+'> : ')
					sys.stdout.flush()
			else :
				msg = sys.stdin.readline()
				client_sock.send(msg)
				sys.stdout.write('<'+name+'> : ')
				sys.stdout.flush()