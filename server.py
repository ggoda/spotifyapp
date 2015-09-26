import time
import BaseHTTPServer
from urlparse import urlparse, parse_qs

hostName = "" #TODO: CHANGE THIS
port = 80

class requestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_header()

	def do_GET(self):
		params = parse_qs(urlparse(self.path).query)
		self.send_response(200)
		self.send_headers("Content-type", "text/html")
		self.end_header()
		self.wfile.write("<html><head><title>Fuck yall</title></head>")
		self.wfile.write("<body><p>Test</p></body></html>")		

if __name__ == '__main__':
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((hostName,port),requestHandler)
	try:
		httpd.serve_forever()	
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	
			
				

	







