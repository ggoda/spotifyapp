import time
import BaseHTTPServer
import json
from random import random
from Queue import Queue
from urlparse import urlparse, parse_qs

testqueue = [123123,231231,23123131,312312312]

hostName = "" #TODO: CHANGE THIS
port = 80
serverDict = {}
factoryQueue = Queue()
userToServer = {}
rand = random()
def serverRand(): #XXX: THIS COULD BE REALLY REALLY BAD
	serverid = rand.randint(0,99999)
	while serverDict.get(serverID) != none:
		serverid =rand.randint(0,99999)
	serverDict.add(serverid)
	return serverid	
class requestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		params = parse_qs(urlparse(self.path).query)
		if 'queue' in self.path:
			serverid = params.get(serverid)
			if serverid == none:
				self.send_response(200)
				self.send_headers("Content-type", "text")
				self.end_header()
				self.wfile.write("Failure: 389")
				return
			queuelist = serverDict.get(serverid)
			if queuelist == none:	
				self.send_response(200)
				self.send_headers("Content-type", "text")
				self.end_header()
				self.wfile.write("Failure: 388")
				return
			self.send_response(200)
			self.send_headers("Content-type", "text/json")
			self.end_header()
			self.wfile.write(json.dumps(testqueue))  #TODO: Change this to queueList
			return
		if 'connect' in self.path:
			userid = params.get(userid)
			serverid = params.get(serverid)
			if serverid == none or userid == none:
				self.send_response(200)
				self.send_headers("Content-type", "text")
				self.end_header()
				self.wfile.write("Failure: 389")
				return
			if serverDict.get(serverid) == none:
				self.send_response(200)
				self.send_headers("Content-type", "text")
				self.end_header()
				self.wfile.write("Failure: 388")
				return
			else: 
				userToServer.add(userid,serverid)
				self.send_response(200)
				self.send_headers("Content-type", "text")
				self.end_header()
				self.wfile.write("Success")
				return	
		if 'addsong' in self.path:
			songid = params.get(songid)
			userid = params.get(userid)
			if songid == none or userid == none:
				self.send_response(200)
				self.send_headers("Content-type", "text")
				self.end_header()
				self.wfile.write("Failure: 389")
				return
			if userToServer.get(userid) == none:
				self.send_response(200)
				self.send_headers("Content-type", "text")
				self.end_header()
				self.wfile.write("Failure: 387")
				return
			workerQueue.add(("addsong",songid,userid))	
			self.send_response(200)
			self.send_headers("Content-type", "text")
			self.end_header()
			self.wfile.write("Success")
			return
		if 'voat' in self.path:
			songid = params.get(songid)
			voat = params.get(voat)
			userid = params.get(userid)
			if voat == none or songid == none or userid == none:
				self.send_response(200)
				self.send_headers("Content-type", "text")
				self.end_header()
				self.wfile.write("Failure: 389")
				return
			if userToServer.get(userid) == none:
				self.send_response(200)
				self.send_headers("Content-type", "text")
				self.end_header()
				self.wfile.write("Failure: 387")
				return
			if voat == "true":
				workerQueue.add(("pvote",songid,userid))
			else:
				workerQueue.add(("nvote",songid,userid))
			self.send_response(200)
			self.send_headers("Content-type", "text")
			self.end_header()
			self.wfile.write("Success")
			return
		if 'createserver' in self.path:
				
			serverid = serverRand()
			self.send_response(200)
			self.send_headers("Content-type", "text")
			self.end_header()
			self.wfile.write(str(serverid))
			return
		else:
			self.send_response(200)
			self.send_headers("Content-type", "text/html")
			self.end_header()
			self.wfile.write("<html><head><title>invalid request 502</title></head></html>")
			return

def run():
	server_class = BaseHTTPServer.HTTPServer
	print("server starting on port 80")
	httpd = server_class((hostName,port),requestHandler)
	print("server started")	
	try:
		httpd.serve_forever()	
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print("\nserver closed")

if __name__ == '__main__':
	run()	
			
				

	







