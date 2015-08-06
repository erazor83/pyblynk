import time
import socket

from . import common

class TCP_Client():
	_Server=None
	_Port=None
	_Socket=None
	_MessageID=None
	_t_lastRX=None
	
	t_Ping=5
	
	def __init__(self,server='cloud.blynk.cc',port=8442):
		self._Server=server
		self._Port=port
		
	def connect(self,timeout=3):
		self.close()
		self._MessageID=0
		self._Socket=socket.create_connection(
			(self._Server,self._Port),
			timeout
		)
		self._Socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		
		return self._Socket
		
	def close(self):
		if self._Socket:
			self._Socket.close()
			
	def tx(self,data):
		if self._Socket:
			self._Socket.sendall(data)
			
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
					return ''
				if not r:
					return ''
				d.append(r)
				l = l + len(r)
			return ''.join(d)
		
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
			)+data
		)
	
	def newMessageID(self):
		self._MessageID=self._MessageID+1
		return self._MessageID
	
	def auth(self,token):
		self.txFrame(common.MSG_LOGIN,len(token))
		self.tx(token)
		response=self.rxFrame()
		if response:
			msg_type, msg_id, msg_status = response

			if (msg_status==common.MSG_STATUS_OK):
				print("Auth successfull")
				return True
		
	def Ping(self):
		#print("Ping...")
		self.txFrame(common.MSG_PING,0)
		rx_frame=self.rxFrame()
		if rx_frame and \
				(rx_frame[0]==common.MSG_RSP)  and \
				(rx_frame[1]==self._MessageID) and \
				(rx_frame[2]==common.MSG_STATUS_OK):
			#print("...Pong")
			return True
		
	def keepConnection(self):
		if (self._t_lastRX+self.t_Ping)<time.time():
			self.Ping()