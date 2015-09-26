import time
import BaseHTTPServer
import json
from threading import Thread
from random import random
from Queue import Queue
from urlparse import urlparse, parse_qs

testqueue = [123123,231231,23123131,312312312]

hostName = "http://spotapp.com/" #TODO: CHANGE THIS
port = 80
serverDict = {}
workerQueue = Queue(100)
userToServer = {}
rand = random()
serverSongRep = {}


def serverRand(): #XXX: THIS COULD BE REALLY REALLY BAD
    serverid = rand.randint(0,99999)
    while serverDict.get(serverID) != none:
        serverid =rand.randint(0,99999)
    serverDict.add(serverid,[])
    serverSongRep.add(serverid, {})
    return serverid
 
class factory(Thread):
    loop = True
    def run(self):
        queueClearer()
    def queueClearer(self):
        while loop:
            if workerQueue.isEmpty():
                time.sleep(1)
            else:
                (command, x, y) = workerQueue.get()
                #Voat x = songid, y = userid
                if command == pvoat:
                    server = userToServer(y)
                if command == nvoat:
                    server = userToServer(y)
                if command == addsong:
    def stop(self):
        self.loop = False                    

class requestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def removeTilSong(songid,serverid):
        
        
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        if 'currentsong' in self.path:
            serverid = params.get(serverid)
            songid = params.get(songid)
            if serverid == none or songid == none
                self.send_response(200)
                self.send_headers("Content-type", "text")
                self.end_header()
                self.wfile.write("Failure: 389")
                return
            
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
                workerQueue.put(("pvote",songid,userid))
            else:
                workerQueue.put(("nvote",songid,userid))
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
    factory.start()
    run()   
            
                

    







