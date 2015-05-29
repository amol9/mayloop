import socket
import os
from os.path import exists
from time import time

from .select_call import SelectCall, SelectError
from .server_helper import ServerStats, ServerSharedState, LinuxLimits, StartError
from .transport.tcp_connection import TCPConnection, HangUp, ConnectionAbort
from .transport.address import Address
from .protocol.telnet_server import TelnetServer
from .transport.pipe_connection import PipeConnection
from .protocol.telnet_server_factory import TelnetServerFactory
#from ..logger import log


def scheduled_task_placeholder():
	pass


class Server():
	def __init__(self, config):
		self._config = config
		self._servers = []
		self._server_to_factory = {}
		#self._shared_state = ServerSharedState()
		self._limits = LinuxLimits()
		self._stats = ServerStats()

		self._client_list = []
		self._telnet_client_list = []


	def start_server_sockets(self):
		for service in self._config.services:
			server = self.create_socket(service.port)
			self._server_to_factory[server] = service.factory

		#self._stats.start_time = time()


	def start_telnet_server_socket(self):
		if self._config.telnet_enabled:
			self._telnet_server = self.create_socket(self._config.telnet_port)
			self._server_to_factory[self._telnet_server] = TelnetServerFactory()


	def create_socket(self, port):
		try:
			server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server.setblocking(0)
			server.bind(('', port))
			server.listen(5)

			return server
		except socket.error as e:
			if e.errno == 98:
				msg = 'address %s:%d already in use'%('', port)
				log.error(msg)
				raise StartError(msg)


	def start(self):
		log.info('starting server...')

		self.start_server_sockets()
		self.start_telnet_server_socket()
		self.start_select_loop()


	def start_select_loop(self):
		select = SelectCall()
		self._pause_server = False

		while True:
			readable = writeable = exceptions = None
			self._stats.update_clients(len(self.client_list))
			self._stats.update_open_fds()

			try:
				readable, writeable, exceptions = select.execute(self.get_in_list(), self.get_out_list())


				self.handle_readable(readable)
				self.handle_writeable(writeable)
				self.handle_exceptions(exceptions)

			except SelectError as e:
				if e.abort_loop:
					log.error('stopping select loop..')
					break

				self.handle_bad_fds(e.bad_fds)


	def handle_readable(self, readable):
		for r in readable:
			if r in self._servers:
				self.handle_incoming_connection(r)
			
			elif r in self.client_list or r in self.telnet_client_list or r in self.in_pipes:
				self.transport_call(r.doRead)
				
			else:
				log.error('bad readable from select')

	
	def handle_writeable(self, writeable):
		for w in writeable:
			if w in self.client_list or w in self.telnet_client_list:
				self.transport_call(w.doWrite)

			else:
				log.error('bad writable from select')


	def transport_call(self, func):
		t = func.im_self

		try:
			func()
		except (HangUp, ConnectionAbort) as e:
			log.error(str(e))

			if not isinstance(e, ConnectionAbort):
				t.abortConnection(raiseException=False)

			if isinstance(t.protocol, WallpServer):
				self._stats.update_client_lifetime(t.get_lifetime())
				self.client_list.remove(t)

			elif isinstance(t.protocol, TelnetServer):
				self.telnet_client_list.remove(t)

			elif isinstance(t, ChildPipe):
				self.in_pipes.remove(t)

			else:
				log.error('should not get here, unknown type of transport was closed')


	def handle_exceptions(self, exceptions):
		if len(exceptions) > 0:
			log.error('select found %d exceptions'%len(exceptions))


	def handle_bad_fds(self, bad_fds):
		if bad_fds is None:
			return

		client_list = self._shared_state.client_list	
		map(client_list.remove, bad_fds)


	def handle_incoming_connection(self, server):
		if self.server_full():
			log.error('connections full')
			return

		if server in self._servers:
			clist = self.client_list

		elif server is self._telnet_server:
			clist = self.telnet_client_list

		else:
			log.error('got an incoming on an unexpected server socket')
			return

		connection, client_address = server.accept()
		log.debug('client connected: ' + str(client_address))

		addr = Address(*client_address)
		protocol = self._server_to_factory[server].buildProtocol(addr)
		transport = TCPConnection(connection, protocol)
		protocol.makeConnection(transport)

		clist.append(transport)


	def server_full(self):
		return self._limits.fds_full(self._stats.open_fds)


	def get_in_list(self):
		wallp_server = [self._server] + self.client_list + self.in_pipes
		if self._config.telnet_enabled:
			telnet_server = [self._telnet_server] + self.telnet_client_list
		else:
			telnet_server = []

		return (wallp_server if not self._pause_server else []) + telnet_server


	def get_out_list(self):
		return (self.client_list if not self._pause_server else []) + self.telnet_client_list


	def get_client_list(self):
		return self._client_list


	def get_telnet_client_list(self):
		return self._telnet_client_list


	def get_in_pipes(self):
		return self._shared_state.in_pipes


	def stop(self):
		self._pause_server = True

		for c in self.client_list:
			self.transport_call(c.abortConnection)
		self._server.close()
		self._server = None


	def hot_start(self):
		self.start_server_socket()
		self._pause_server = False


	def pause(self):
		self._pause_server = True


	def resume(self):
		self.start_select_loop()


	client_list 		= property(get_client_list)
	telnet_client_list 	= property(get_telnet_client_list)
	in_pipes		= property(get_in_pipes)


