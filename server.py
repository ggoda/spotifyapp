import time
import BaseHTTPServer
import json
from threading import Thread
import random 
from Queue import Queue
from urlparse import urlparse, parse_qs

testqueue = [123123,231231,23123131,312312312]

hostName = "0.0.0.0" #TODO: CHANGE THIS
port = 80
serverDict = {}
workerQueue = Queue(100)
userToServer = {}
serverSongRep = {}


def serverRand(): #XXX: THIS COULD BE REALLY REALLY BAD
    serverid = random.randint(0,99999)
    while serverDict.get(str(serverid)) != None:
        serverid =rand.randint(0,99999)
    serverDict[str(serverid)] = []
    serverSongRep[str(serverid)] = {}
    return serverid
 
class factory(Thread):
    loop = True

    def queueClearer(self):
        while self.loop:
            if workerQueue.empty():
                time.sleep(1)
            else:
		print("Got Command")
                (command, x, y) = workerQueue.get()
                #Voat x = songid, y = userid
                if command == "pvoat":
                    server = userToServer.get(y)
                if command == "nvoat":
                    server = userToServer.get(y)
                if command == "addsong":
		    server = userToServer.get(y)
		    (serverDict[server]).append(x)
		    
    def run(self):
        self.queueClearer()
    def stop(self):
        self.loop = False                    

class requestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        print("Get Request")
        print(self.path)
	tmp = ""
	if "?" in self.path:
		 path,tmp = self.path.split('?',1) 
	params = parse_qs(tmp)
	print params
        if 'currentsong' in self.path:
            serverid = params.get('serverid')
            songid = params.get('songid')
            if serverid == None or songid == None:
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 389")
                return
            
        if 'queue' in self.path:
            serverid = params.get("serverid")
            if serverid == None:
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 389")
                return
            queuelist = serverDict.get(serverid[0])
            if queuelist == None:   
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 388")
                return
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()
            self.wfile.write(json.dumps(queuelist))  #TODO: Change this to queueList
            return
	if 'update' in self.path:
	    serverid = params.get("serverid")	
	    songid = params.get("songid")	
            if serverid == None:
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 389")
                return
            if serverDict.get(serverid[0]) == None:
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 388")
                return
            if not (songid[0] in serverDict.get(serverid[0])):
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 386")
                return
	    else:
		song = serverDict.get(serverid[0]).pop(0)
		while not songid[0] == song:
		    song = serverDict.get(serverid[0]).pop(0)
                serverDict.get(serverid[0]).insert(0,song) 
		self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Success")
                return  

        if 'connect' in self.path:
            userid = params.get("userid")
            serverid = params.get("serverid")
            if serverid == None or userid == None:
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 389")
                return
            if serverDict.get(serverid[0]) == None:
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 388")
                return
            else: 
                userToServer[userid[0]]=serverid[0]
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Success")
                return  
        if 'addsong' in self.path:
            songid = params.get("songid")
            userid = params.get("userid")
            if songid == None or userid == None:
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 389")
                return
            if userToServer.get(userid[0]) == None:
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 387")
                return
            workerQueue.put(("addsong",songid[0],userid[0]))  
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write("Success")
            return
        if 'voat' in self.path:
            songid = params.get("songid")
            voat = params.get("voat")
            userid = params.get("userid")
            if voat == None or songid == None or userid == None:
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 389")
                return
            if userToServer.get(userid[0]) == None:
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 387")
                return
            if voat == "true":
                workerQueue.put(("pvote",songid[0],userid[0]))
            else:
                workerQueue.put(("nvote",songid[0],userid[0]))
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write("Success")
            return
        if 'createserver' in self.path:
            serverid = serverRand()
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(str(serverid))
            return
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("<html><head><title>invalid request 502</title></head></html>")
            return

def run(factoryn):
    server_class = BaseHTTPServer.HTTPServer
    print("server starting on port 80")
    httpd = server_class((hostName,port),requestHandler)
    print("server started") 
    try:
        httpd.serve_forever()   
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    factoryn.stop()
    print("\nserver closed")

if __name__ == '__main__':
    factoryn = factory()
    factoryn.start()
    run(factoryn)   
            
                

    







