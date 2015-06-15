from zope.interface import implementer
import struct

from ..imported.twisted.internet_interfaces import IPullProducer
from ..limits import get_limits


@implementer(IPullProducer)
class ImageChunkProducer:

	def __init__(self, transport, wp_image):
		self._transport = transport
		self._chunk_no = 0
		self.producing = True


	def stopProducing(self):
		self.producing = False


	def resumeProducing(self):
			#get a chunk and send it
			#message = response.SerializeToString()
			#message = struct.pack('>i', len(message)) + message

			#self._transport.write(message)

			#self._chunk_no += 1
		#else:
			#self.stopProducing()
			pass		

