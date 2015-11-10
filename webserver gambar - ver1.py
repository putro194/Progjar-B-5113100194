import sys, socket, time

HOST = 'localhost'
RECV_BUFFER = 4096
PORT = 9999

def get_file(nama):
        myfile = open(nama)
        return myfile.read() 

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(5)

print "Connection to localhost... port " + str(PORT) 

while True:
        message = 'tanda-'
        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection...'
        connection, client_address = server_socket.accept()
        print >>sys.stderr, 'Connection from', client_address, '\n'
        
        req_recv = connection.recv(RECV_BUFFER)
        detail_info = req_recv.decode()

        if req_recv:
                message = message + req_recv
                print message
                #if(message.startswith("tanda-GET /8 HTTP/1.1")):
                if(message.startswith("tanda-GET /1 HTTP/1.1")):
                        #with open("gambar2.jpg" ,"rb") as ImageFile:
                        #        hasilencode=base64.b64encode(ImageFile.read())
                        #        print hasilencode
                        data_picture = get_file('gambar2.jpg')
                        connection.send(data_picture)
                        print (detail_info)

                        ##connection.send(data)
                        #self.client_socket.send(get_file('gambar2.jpg'))

                elif(message.startswith("tanda-GET /2 HTTP/1.1")):
                        data_picture = get_file('gambar3.jpg')
                        connection.send(data_picture)
                        print (detail_info)

                elif(message.startswith("tanda-GET /3 HTTP/1.1")):
                        data_picture = get_file('gambar4.jpg')
                        connection.send(data_picture)
                        print (detail_info)

                elif(message.startswith("tanda-GET /4 HTTP/1.1")):
                        data_picture = get_file('gambar5.png')
                        connection.send(data_picture)
                        print (detail_info)

                elif(message.startswith("tanda-GET /5 HTTP/1.1")):
                        data_picture = get_file('gambar6.png')
                        connection.send(data_picture)
                        print (detail_info)                

                elif (message.endswith("\r\n\r\n")):
                        data_picture = get_file('gambar.jpg')
                        data = "Terimakasih telah mengunjungi Webserver sederhana ini\n\n"
                        data2 = "200-OK !"

                        connection.send(data_picture)
                        print (detail_info)
                        
                        connection.send(data)
                        print(data2)

                        break
        else:
                break

# Clean up the connection
connection.close()
