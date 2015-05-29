import logging

from .logger import log


class Service:
	def __init__(self, host, port, factory):
		self.host = host
		self.port = port
		self.factory = factory


class Config:
	telnet_enabled = True
	telnet_port = 40001
	services = []

	def __init__(self):
		pass


	def add_service(self, host, port, factory):
		if host is None:
			raise ConfigError('host cannot be none')

		self.check_port_value(port)

		if factory is None:
			raise ConfigError('factory cannot be none')

		self.services.append(Service(host, port, factory))


	def check_port_value(self, port):
		if port is None or port < 0 or port > (2 ** 16 - 1) or type(port) != int:
			raise ConfigError('invalid port')

	
	def start_logger(self, target='stdout', level=logging.ERROR):
		log.start(target, level)


	def disable_telnet(self):
		self.telnet_enabled = False


	def set_telnet_port(self, port):
		self.check_port_value(port)
		self.telnet_port = port
