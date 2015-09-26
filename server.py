import time
import BaseHTTPServer
import json
from urlparse import urlparse, parse_qs

testqueue = [123123,231231,23123131,312312312]

hostName = "" #TODO: CHANGE THIS
port = 80

class requestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_header()

	def do_GET(self):
		params = parse_qs(urlparse(self.path).query)
		if 'queue' in self.path:
			serverid = params.get(server.id)
			self.send_response(200)
			self.send_headers("Content-type", "text/json")
			self.end_header()
			self.wfile.write(json.dumps(testqueue))
		if 'connect' in self.path:
			print("connect")
		if 'addsong' in self.path:
			print("addsong")
		if 'voat' in self.path:
			print("voat")
		if 'createserver' in self.path:
			print("createserver")
		else:
			self.send_response(200)
			self.send_headers("Content-type", "text/html")
			self.end_header()
			self.wfile.write("<html><head><title>invalid request 404</title></head></html>")


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
			
				

	







