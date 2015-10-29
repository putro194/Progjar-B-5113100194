import sys, socket, select

username = []
addresss = []
socket_lists = []

HOST = ''
LIST_SOCKET = []
RECV_BUFFER = 4096
PORT = 9999

def broadcast(sock, message):
	for socket in LIST_SOCKET:
		if socket != server_socket and socket != sock :
			try :
				socket.send(message)
			except :
				socket.close()
				LIST_SOCKET.remove(socket)

if __name__ == "__main__":

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(5)
	LIST_SOCKET.append(server_socket)

	print "Saluran tersambung... port " + str(PORT)

	while True:
		ready_to_read, ready_to_write, in_error = select.select(LIST_SOCKET,[],[])

		for sock in ready_to_read:
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				LIST_SOCKET.append(sockfd)
				print "User (%s, %s) tersambung dengan jaringan" %addr
			
			else:
				try:
					data = sock.recv(RECV_BUFFER)
					if data:

						#if(data == 'list\n'):
						#	if(data == 'list\n'):
						#		for i in range(len(username)):
						#			sock.send("* "+username[i])
						#			sock.send("\n")
#
						#	elif data != 'list\n':
						#		sock.send("Perintahmu salah!\n")

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
									sock.send("Perhatian: Login gagal! Username sudah dipakai.\n")
									print "403-Username sudah dipakai"
									sock.close()
									LIST_SOCKET.remove(sock)
									continue

								print "200-OK"

							elif temp[0] == "help\n":
								sock.send("Protokol perintah yang bisa membantumu :\n1. Melihat daftar user: 'list'\n2. Mengirim pesan ke semua user: 'sendall' <spasi> pesan\n3. Mengirm pesan ke salah satu user: 'sendto' <spasi> nama_user <spasi> pesan\n4. Menghapus percakapan: 'clear'\n5. Melihat status login: 'whoami'\n6. Keluar dari percakapan: 'logout'\n7. Mengetauhi info bantuan: 'help'\n")

							elif temp[0] == "list\n":
								for i in range(len(username)):
									sock.send("* "+username[i])
									sock.send("\n")

							elif temp[0] == "sendall":
								user = username[addresss.index(str(sock.getpeername()))]
								broadcast(sock, "\r" + '<' + user + '> berkata : ' +str(temp[1]))

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
									sock.send("Perhatian: User yang dituju tidak ada!\n")
									print "402-User tidak terdaftar"
								else:
									temp_kirim = username.index(index_kirim)
									socket_lists[temp_kirim].send("\r" + '<' + user + '> privasi : ' + str(kirim[1]))

							elif temp[0] == "clear\n":
								sock.send(100*"\n")

							elif temp[0] == "whoami\n":
								user_whomai = username[addresss.index(str(sock.getpeername()))]
								sock.send("Kamu login sebagai" +user_whomai +"\n")

							elif temp[0] == "logout\n":
								user3 = username[socket_lists.index(sock)]
								broadcast(sock, "" + user3 + " keluar percakapan\n")
								sock.close()
								LIST_SOCKET.remove(sock)			

							elif ((len(data) > 0) and temp[0] != "sendto") or ((len(data) > 0) and temp[0] != "sendall") or ((len(data) > 0) and temp[0] != "list") or ((len(data) > 0) and temp[0] != "help") or ((len(data) > 0) and temp[0] != "clear") or ((len(data) > 0) and temp[0] != "whoami"):
								sock.send("Perhatian: Bukan data valid!\n")
								print "401-Data tidak valid"

						else:
							sock.send("Error system!\n")

				except:
					user2 = username[socket_lists.index(sock)]
					broadcast(sock, "User " + user2 + " sedang tidak aktif\n")
					sock.close()
					LIST_SOCKET.remove(sock)
					continue

	server_socket.close()