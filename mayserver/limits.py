
from mutils.system import *


class GenericLimits():
	max_message_size 		= 10 * 1024 * 1024
	max_messages_in_queue_per_conn 	= 10
	max_line_message_length		= 512


class LinuxLimits(GenericLimits):
	max_select_fds 	= 1024
	max_open_fds 	= 20
	fd_buffer 	= 5


	def fds_full(self, open_fds):
		return open_fds >= (self.max_open_fds - self.fd_buffer)


class WindowsLimits(GenericLimits):
	pass


def get_limits():
	if is_linux():
		return LinuxLimits()
	elif is_windows():
		return WindowsLimits()
	else:
		raise PlatformError('unsupported platform')

