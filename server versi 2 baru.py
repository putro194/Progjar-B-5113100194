import sys, socket, select

username = []
addresss = []
socket_lists = []

HOST = ''
CONNECTION_LIST = []
RECV_BUFFER = 4096
PORT = 9999

def broadcast(sock, message):
	for socket in CONNECTION_LIST:
		if socket != server_socket and socket != sock :
			try :
				socket.send(message)
			except :
				socket.close()
				CONNECTION_LIST.remove(socket)

if __name__ == "__main__":

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #<-
	server_socket.bind((HOST, PORT))
	server_socket.listen(5)
	CONNECTION_LIST.append(server_socket)

	print "Saluran tersambung... port " + str(PORT)

	while True:
		ready_to_read, ready_to_write, in_error = select.select(CONNECTION_LIST,[],[])

		for sock in ready_to_read:
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				CONNECTION_LIST.append(sockfd)
				print "User (%s, %s) tersambung dengan jaringan" %addr
			
			else:
				try:
					data = sock.recv(RECV_BUFFER)
					if data:

						if(data == 'list\n'):
							if(data == 'list\n'):
								for i in range(len(username)):
									sock.send("-> "+username[i])
									sock.send("\n")

							elif data != 'list\n':
								sock.send("Perintahmu salah!\n")

						if(len(data) > 0) :
							temp = data.split(' ', 1)
							if temp[0] == "UN":
								flag = 0
								
								for i in range (len(username)):
									if str(temp[1]) == str(username[i]):
										flag = 1
								
								if flag==0:
									addresss.append(str(sock.getpeername()))
									username.append(str(temp[1]))
									socket_lists.append(sock)
								
									print "User " +str(sock.getpeername())+ " alias " +str(temp[1])

									broadcast(sock, str(temp[1])+ " masuk percakapan\n")
									sock.send("gas...")
								
								if flag==1:
									print "User "+str(sock.getpeername())+ " sudah dipakai"
									sock.send("login gagal!\n")
									sock.close()
									CONNECTION_LIST.remove(sock)
									continue

							elif temp[0] == "sendall":
								user = username[addresss.index(str(sock.getpeername()))]
								broadcast(sock, "\r" + '<' + user + '> berkata ' +str(temp[1]))

							elif temp[0] == "sendto":
								user = username[addresss.index(str(sock.getpeername()))]	
								kirim = str(temp[1]).split(' ', 1)
								index_kirim = kirim[0]
								flag2 = 0
								
								for i in range (len(username)):
									if username[i] == index_kirim:
										temp_kirim = i
										flag2 = 1
						
								if flag2 == 0 :
									sock.send("User yang dituju tidak ada!\n")
								else:
									temp_kirim = username.index(index_kirim)
									socket_lists[temp_kirim].send("\r" + '<' + user + '> : ' + str(kirim[1]))

							elif temp[0] == "whoami":
								print "Anda login sebagai..."
							#	user = username[addresss]
							#	addresss.append(str(sock.getpeername()))
							#	username.append(str(temp[1]))
							#	socket_lists.append(sock)
								
#
#								sock.send() "Anda login sebagai "+str(temp[1])
#
						else:
							sock.send("Bukan data valid!\n")

				except:
					user2 = username[socket_list.index(sock)]
					broadcast(sock, "User " + user2 + "sedang tidak aktif\n")
					sock.close()
					CONNECTION_LIST.remove(sock)
					continue

	server_socket.close()
