# -*- coding: utf-8 -*-
"""
	client helpers
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2016-07-05"
__version__	= "0.2.1"
__credits__	= """Copyright e-design, Alexander Krause <alexander.krause@ed-solutions.de>"""
__license__	= "MIT"

import time
import socket

from . import common

class TCP_Client(object):
	_Server=None
	_Port=None
	_Socket=None
	_MessageID=None
	_t_lastRX=None
	_lastToken=None
	
	t_Ping=5
	connected=False
	
	def __init__(self,server='blynk-cloud.com',port=8442):
		self._Server=server
		self._Port=port
		
	def connect(self,timeout=3):
		print('connected')
		self.close()
		self._MessageID=0
		self._Socket=socket.create_connection(
			(self._Server,self._Port),
			timeout
		)
		self._Socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		
		if self._Socket:
			self.connected=True
		return self._Socket
		
	def close(self):
		if self._Socket:
			self._Socket.close()
		self.connected=False

			
	def tx(self,data):
		#print('tx',data)
		if self._Socket:
			try:
				self._Socket.sendall(data)
			except Exception:
				self.connected=False
			
	def rx(self,length):
		if self._Socket:
			d = []
			l = 0
			while l < length:
				r = ''
				try:
					r = self._Socket.recv(length-l)
					self._t_lastRX=time.time()
				except socket.timeout:
					#print('rx-timeout')
					return ''
				except Exception as e:
					print('rx exception',str(e))
					self.connected=False
					return ''
				if not r:
					self.connected=False
					return ''
				d.append(r)
				#print(d)
				l = l + len(r)
				
			ret=bytes()
			for cluster in d:
				ret=ret+cluster
			return ret
		
	def rxFrame(self):
		response=self.rx(common.ProtocolHeader.size)
		if response:
			return common.ProtocolHeader.unpack(response)
		
	def txFrame(self,msg_type,data):
		self.tx(
			common.ProtocolHeader.pack(
				msg_type,
				self.newMessageID(),
				data
			)
		)
	def txFrameData(self,msg_type,data):
		self.tx(
			common.ProtocolHeader.pack(
				msg_type,
				self.newMessageID(),
				len(data)
			)+data.encode('ascii')
		)
	
	def newMessageID(self):
		self._MessageID=self._MessageID+1
		return self._MessageID
	
	def auth(self,token=None):
		if not token and self._lastToken:
			token=self._lastToken
		elif token:
			self._lastToken=token
		else:
			return False
		
		self.txFrame(common.MSG_LOGIN,len(token))
		self.tx(str(token).encode('ascii'))
		response=self.rxFrame()
		if response:
			msg_type, msg_id, msg_status = response

			if (msg_status==common.MSG_STATUS_OK):
				print("Auth successfull")
				return True
		
	def Ping(self):
		print("Ping...")
		self.txFrame(common.MSG_PING,0)
		rx_frame=self.rxFrame()
		if rx_frame and \
				(rx_frame[0]==common.MSG_RSP)  and \
				(rx_frame[1]==self._MessageID) and \
				(rx_frame[2]==common.MSG_STATUS_OK):
			print("...Pong")
			return True
		
	def keepConnection(self):
		if not self.connected:
			if self.connect() and self.auth():
				return True
			else:
				time.sleep(1)
				return False
		if (self._t_lastRX+self.t_Ping)<time.time():
			self.Ping()
			
			
		
