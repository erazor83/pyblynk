# -*- coding: utf-8 -*-
"""
	example hardware
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2016-01-11"
__version__	= "0.2.0"
__credits__	= """Copyright e-design, Alexander Krause <alexander.krause@ed-solutions.de>"""
__license__	= "MIT"


import sys
import os
sys.path.append(
	os.path.join(
		os.path.dirname(__file__),
		'..'
	)
)
	
TOKEN			= '<TOKEN>'

import lib.hw as blynk_hw
import lib.client as blynk_client

class myHardware(blynk_hw.Hardware):
	"""
		you'll probably have to overload the On* calls,
		see lib/hw.py
	"""
	pass

cConnection=blynk_client.TCP_Client()
if not cConnection.connect():
	print('Unable to connect')
	sys.exit(-1)

if not cConnection.auth(TOKEN):
	print('Unable to auth')
	
cHardware=myHardware(cConnection)

try:
	while True:
		cHardware.manage()
except KeyboardInterrupt:
	raise

