
from mayserver.protocol.fixed_length_message import FixedLengthMessage
from mayserver.imported.twisted.internet_protocol import Protocol

class TestServer(FixedLengthMessage):
	def messageReceived(self, message):
		self.sendMessage('just a test response')


class RawData(Protocol):
	def dataReceived(self, data):
		print(data)

