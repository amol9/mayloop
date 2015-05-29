import logging

from mayserver.server import Server
from mayserver.config import Config
from mayserver.imported.twisted.internet_protocol import Factory
from .test_protocol import TestServer


def start_only_telnet():
	config = Config()
	config.start_logger(level=logging.DEBUG)

	server = Server(config)
	server.start()


def start_test_server():
	config = Config()
	config.add_service('', 40002, Factory.forProtocol(TestServer))
	config.start_logger(level=logging.DEBUG)

	server = Server(config)
	server.start()


if __name__ == '__main__':
	#start_only_telnet()
	start_test_server()

