from unittest import TestCase, main as ut_main
import logging
from threading import Thread
from Queue import Queue
from multiprocessing import Process

from mayloop.mainloop import MainLoop
from mayloop.config import Config
from mayloop.imported.twisted.internet_protocol import Factory
from .mock_protocols import ReturnFixedMessage
from .mock_client import Client


class TestMainLoop(TestCase):
	server_process = None
	port = 40002
	multiple_client_counts = [10, 100]

	@classmethod
	def setUpClass(cls):
		pass


	@classmethod
	def tearDownClass(cls):
		if cls.server is not None:
			print('press ^C to quit server)


	def start_server(port):
		config = Config()
		config.add_service('', port, Factory.forProtocol(ReturnFixedMessage))
		config.start_logger(level=logging.DEBUG)

		server = MainLoop(config)
		server.start()


	def start_server(test_func):
		def new_func(self):
			if self.server_process is None:
				self.server_process = Process(target=start_server, args=(self.port,))
				self.server_process.start()
			test_func(self)
		return new_func


	@start_server
	def test_single_client(self):
		exp_response = 'test response'
		ReturnFixedMessage.message = exp_response
		client = Client('', self.port)
		client.connect()
		client.close()

		self.assertEquals(client.response, exp_response)


	@start_server
	def test_multiple_clients_serial(self):
		exp_response = 'test response'
		ReturnFixedMessage.message = exp_response

		for i in self.multiple_client_counts:
			for j in range(i):
				client = Client('', self.port)
				client.connect()
				client.close()

				self.assertEquals(client.response, exp_response)

	
	@start_server
	def test_multiple_clients_parallel(self):
		exp_response = 'test response'
		ReturnFixedMessage.message = exp_response

		def client_thread(port, client_id, results):
			client = Client('', port)
			client.connect()
			client.close()
		
			results.put((client_id, client.response))


		for i in self.multiple_client_counts:
			threads = []
			results = Queue()
			for j in range(i):
				t = Thread(target=client_thread, args=(self.port, j, results))
				threads.append(t)

			for j in range(i):
				threads[j].join()
				client_id, response = results.get()
				self.assertEquals(response, exp_response, msg='client %d failed'%client_id)


