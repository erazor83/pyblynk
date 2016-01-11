# -*- coding: utf-8 -*-
"""
	commmon helpers
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2016-01-11"
__version__	= "0.2.0"
__credits__	= """Copyright e-design, Alexander Krause <alexander.krause@ed-solutions.de>"""
__license__	= "MIT"

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
	return (buff.decode('ascii')).split("\0")
