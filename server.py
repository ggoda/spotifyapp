import time
import BaseHTTPServer
import json
from threading import Thread
import random 
from Queue import Queue
from urlparse import urlparse, parse_qs

hostName = "0.0.0.0" #TODO: CHANGE THIS
port = 80
serverDict = {}
workerQueue = Queue(100)
userToServer = {}
serverSongRep = {}
userRep = {}
songToUser = {}

def serverRand(): #XXX: THIS COULD BE REALLY REALLY BAD
    serverid = random.randint(10000,99999)
    while serverDict.get(str(serverid)) != None:
        serverid =rand.randint(10000,99999)
    serverDict[str(serverid)] = []
    serverSongRep[str(serverid)] = {}
    print ("New Server:" + str(serverid))
    return serverid
def update(serverid,songid):
	song = serverDict.get(serverid).pop(0)
	while not songid == song:
	   song = serverDict.get(serverid[0]).pop(0)
        serverDict.get(serverid[0]).insert(0,song)
	
     
class factory(Thread):
    loop = True

    def queueClearer(self):
        while self.loop:
            if workerQueue.empty():
                time.sleep(1)
            else:
                (command, x, y) = workerQueue.get()
                #Voat x = songid, y = userid
                if command == "pvote":
                    server = userToServer.get(y)
		    userRep[songToUser[y]] += 1
		    serverSongRep[y] +=5 
                if command == "nvote":
                    server = userToServer.get(y)
		    userRep[songToUser[y]] -= 1
		    serverSongRep[y] -=5 
                if command == "addsong":
		    server = userToServer.get(y)
		    if not x in serverDict[server]: 
			(serverDict[server]).append(x)
			songToUser[x] = y
		    
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
                self.wfile.write("Failure: 389: missing params")
                return
            
        if 'queue' in self.path:
            serverid = params.get("serverid")
            userid = params.get("userid")
            if serverid == None and userid == None:
                self.send_response(389)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 389: missing params")
                return
	    if serverid == None:
		queuelist = serverDict.get(userToServer(userid[0]))	
	    else:
               	queuelist = serverDict.get(serverid[0])
            if queuelist == None:   
                self.send_response(388)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 388: Server does not exist")
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
                self.send_response(389)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 389: missing params")
                return
            if serverDict.get(serverid[0]) == None:
                self.send_response(388)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 388: server does not exist")
                return
            if not (songid[0] in serverDict.get(serverid[0])):
                self.send_response(386)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 386: song not in queue")
                return
	    else:
		update(serverid[0],songid[0])
		self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Success")
                return  

        if 'connect' in self.path:
            userid = params.get("userid")
            serverid = params.get("serverid")
            if serverid == None or userid == None:
                self.send_response(389)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 389: missing params")
                return
            if serverDict.get(serverid[0]) == None:
                self.send_response(388)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 388: Server does not exist")
                return
            else:
		if userRep[userid[0]] == None:
		   userRep[userid[0]] = 0
                
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
                self.send_response(389)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 389: missing params")
                return
            if userToServer.get(userid[0]) == None:
                self.send_response(200)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 387: user not connected to server")
                return
            workerQueue.put(("addsong",songid[0],userid[0]))  
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write("Success")
            return
        if 'vote' in self.path:
            songid = params.get("songid")
            vote = params.get("vote")
            userid = params.get("userid")
            if vote == None or songid == None or userid == None:
                self.send_response(389)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 389: missing params")
                return
            if userToServer.get(userid[0]) == None:
                self.send_response(387)
                self.send_header("Content-type", "text")
                self.end_headers()
                self.wfile.write("Failure: 387: User not connected to server")
                return
            if vote == "true":
                workerQueue.put(("pvote",songid[0],userid[0]))
            else:
                workerQueue.put(("nvote",songid[0],userid[0]))
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write("Success")
            return
        if 'createserver' in self.path:
            userid = params.get("userid")
            serverid = serverRand()
            if not userid == None:
	    	if userRep.get(userid[0]) == None:
	    	    userRep[userid[0]] = 0
	    	
            userToServer[userid[0]]=serverid
            
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
            
                

    







