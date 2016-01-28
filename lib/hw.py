# -*- coding: utf-8 -*-
"""
	hardware class for overloading
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2016-01-11"
__version__	= "0.2.0"
__credits__	= """Copyright e-design, Alexander Krause <alexander.krause@ed-solutions.de>"""
__license__	= "MIT"

from . import common

class Hardware(object):
	_Media=None
	
	def __init__(self,media):
		self._Media=media
		
		
	def manage(self):
		if self._Media:
			#print('manage')
			self._Media.keepConnection()
			rx_frame=self._Media.rxFrame()
			
			if rx_frame:
				print(rx_frame)
				if (rx_frame[0] == common.MSG_HW) or (rx_frame[0] == common.MSG_BRIDGE):
					data = self._Media.rx(rx_frame[2])
					params=common.BufferToArgs(data)
					cmd=params.pop(0)
					self.OnMessage_HW(
						cmd,
						params
					)
					self._Media.txFrame(common.MSG_RSP,common.MSG_STATUS_OK)
				else:
					self.OnMessage_Unknown(rx_frame[0],rx_frame[2])
					
	def OnMessage_HW(self,cmd,params):
		if cmd=='info':
			self.OnHW_info()
		elif cmd=='pm':
			pairs=zip(params[0::2], params[1::2])
			for (pin, mode) in pairs:
				pin=int(pin)
				self.OnPinMode(pin,mode)
		elif cmd=='dw':
			pin = int(params.pop(0))
			val = params.pop(0)
			self.OnDigitalWrite(pin,val)
		elif cmd=='aw':
			pin = int(params.pop(0))
			val = params.pop(0)
			self.OnAnalogWrite(pin,val)
		elif cmd=='dr':
			pin = int(params.pop(0))
			val=self.OnDigitalRead(pin)

			self._Media.txFrameData(
				common.MSG_HW,
				common.ArgsToData(
					'dw',
					pin,
					val
				)
			)
		elif cmd=='ar':
			pin = int(params.pop(0))
			val=self.OnAnalogRead(pin)

			self._Media.txFrameData(
				common.MSG_HW,
				common.ArgsToBuffer(
					'aw',
					pin,
					val
				)
			)
		elif cmd=='vw':
			pin = int(params.pop(0))
			val = params.pop(0)
			self.OnVirtualWrite(pin,val)
		elif cmd=='vr':
			pin = int(params.pop(0))
			val=self.OnVirtualRead(pin)

			self._Media.txFrameData(
				common.MSG_HW,
				common.ArgsToBuffer(
					'vw',
					pin,
					val
				)
			)
		else:
			print("Unknown HW-Command %s"%cmd)
	
	def OnHW_info(self):
		pass
	
	def OnPinMode(self,pin,mode):
		print('OnPinMode',pin,mode)

	def OnDigitalWrite(self,pin,val):
		print('OnDigialWrite',pin,val)

	def OnAnalogWrite(self,pin,val):
		print('OnAnalogWrite',pin,val)

	def OnDigitalRead(self,pin):
		print('OnDigialRead',pin)
		return 0

	def OnAnalogRead(self,pin):
		print('OnAnalogRead',pin)
		return 0
	
	def OnVirtualWrite(self,pin,val):
		print('OnVirtualWrite',pin,val)
		
	def OnVirtualRead(self,pin):
		print('OnVirtualRead',pin)
		return 0
	
	def OnMessage_Unknown(self,msg_type,data):
		pass
	
	def OnMessage_Ping(self,data):
		pass
