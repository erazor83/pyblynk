import struct

MSG_RSP				= 0
MSG_LOGIN			= 2
MSG_PING			= 6
MSG_BRIDGE		= 15
MSG_HW				= 20

MSG_STATUS_OK	= 200


ProtocolHeader = struct.Struct("!BHH")

def ArgsToBuffer(*args):
	# Convert params to string and join using \0
	return "\0".join(map(str, args))

def BufferToArgs(buff):
	return buff.split("\0")
