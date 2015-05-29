
from mayserver.protocol.fixed_length_message import FixedLengthMessage

class TestServer(FixedLengthMessage):
	def messageReceived(self, message):
		self.sendMessage('just a test response')


