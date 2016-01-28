# -*- coding: utf-8 -*-
"""
	Client connection classes

"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2015-08-08"
__version__	= "0.1.0"
__license__ = "MIT"

def createFromConf(conf,storage=None):
	if conf['type']=='tcp':
		return TCP_Server(conf['conf'],storage)
	
class Server(object):
	conf=None
	Storage=None
	Connections=None
	
	def __init__(self,config,storage):
		self.conf=config
		self.Storage=storage
		self.Connections={}
		
	def run(self):
		pass
	
	def stop(self):
		pass
	
class TCP_Server(Server):
	Server=None
	
	def run(self):
		import SocketServer
		class BlynkUserConnection(SocketServer.BaseRequestHandler):
			def handle(self):
				if not self.client_address[0] in self.Server.Connections:
					self.Server.Connections[self.client_address[0]]={}
				
				if len(self.Server.Connections[self.client_address[0]]) < self.Server.conf['max_user_connections']:
					
					self.Server.Connections[self.client_address[0]][self.client_address[1]]=self
					
					# self.request is the TCP socket connected to the client
					self.data = self.request.recv(1024).strip()
					print "{} wrote:".format(self.client_address[0])
					print self.data
					# just send back the same data, but upper-cased
					self.request.sendall(self.data.upper())
		
			def finish(self):
				if (self.client_address[0] in self.Server.Connections) and \
						(self.client_address[1] in self.Server.Connections[self.client_address[0]]):
							
					del self.Server.Connections[self.client_address[0]][self.client_address[1]]
					
				return SocketServer.BaseRequestHandler.finish(self)
			
			def close(self):
				pass
			
			
		BlynkUserConnection.Server=self
		self.Server=SocketServer.TCPServer(
			(self.conf['net'], self.conf['port']),
			BlynkUserConnection
		)
		self.Server.serve_forever()
		
	def close(self):
		for ip in self.Connections:
			for port in self.Connections[ip]:
				self.Connections[ip][port].close()
        
