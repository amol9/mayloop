import struct
import socket

def send_something():
	data = 'hello'
	message = struct.pack('>i', len(data)) + str.encode(data)

	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection.connect(('192.168.0.101', 40002))

	connection.send(message)
	res = connection.recv(512)
	print(res)


send_something()