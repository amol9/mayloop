import struct
import socket

def send_something():
	data = 'hello'
	message = struct.pack('>i', len(data)) + data

	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection.connect(('', 40002))

	connection.send(message)
	res = connection.recv(512)
	print res


send_something()
