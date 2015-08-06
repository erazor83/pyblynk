
import sys
import os
sys.path.append(
	os.path.join(
		os.path.dirname(__file__),
		'..'
	)
)
	
TOKEN			= '???'

import lib.hw as blynk_hw
import lib.client as blynk_client


cConnection=blynk_client.TCP_Client()
if not cConnection.connect():
	print('Unable to connect')
	sys.exit(-1)

if not cConnection.auth(TOKEN):
	print('Unable to auth')
	
cHardware=blynk_hw.Hardware(cConnection)

try:
	while True:
		cHardware.manage()
except KeyboardInterrupt:
	raise

