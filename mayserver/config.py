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
		if port is None or port < 0 or port > (2 ** 16 - 1):
			raise ConfigError('invalid port')
		if factory is None:
			raise ConfigError('factory cannot be none')

		self.services.append(Service(host, port, factory))

	
	def start_logger(self, target='stdout', level=logging.ERROR):
		log.start(target, level)
