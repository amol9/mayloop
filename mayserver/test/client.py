import struct
import socket
from time import sleep


def send_something():
	data = 'hello'
	message = struct.pack('>i', len(data)) + str.encode(data)

	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection.connect(('192.168.0.101', 40002))

	connection.send(message)
	res = connection.recv(512)
	print('1: '+ res[4:].decode('utf-8'))

	sleep(30)
	connection.send(message)
	res = connection.recv(512)
	print('2: '+ res[4:].decode('utf-8'))


send_something()
