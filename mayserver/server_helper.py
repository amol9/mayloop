

class StartError(Exception):
	pass




'''class ServerSharedState():
	def __init__(self):
		self.in_pipes = []
		self.out_pipes = []

		self.client_list = []
		self.telnet_client_list = []
		self.last_change = None
		self.wp_image = WallpaperImage()
		self.wp_state = WPState.NONE


	def abort_image_producers(self):
		for transport in self.client_list:
			transport.unregisterProducer()'''


