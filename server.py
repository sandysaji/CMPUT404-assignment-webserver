#  coding: utf-8 
import socketserver, os
# import http.server

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# https://www.tutorialspoint.com/http/http_responses.htm
# https://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python




class MyWebServer(socketserver.BaseRequestHandler):
    
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        #parsing self.data.
        http_request = self.data.split()

        #creating the path and adding item sent from http_request
        if (http_request[0].decode('utf-8') == "GET"):
            infopath = os.path.abspath('www')
            infopath += http_request[1].decode('utf-8')



    #If the path is a file
            if (os.path.isfile(infopath)):
                #Take the path extension.
                ext = os.path.splitext(infopath)
                #if the path extension ends in html.
                if (ext[1] == ".html"):
                    content = "text/html"
                    pageInfo = open(infopath).read()
                    contentlen = len(pageInfo)
                    output = ("HTTP/1.1 200 OK\nContent-Type: " +content+ "\nConnection: Closed\n\n"+pageInfo)
                    self.request.sendall(bytearray(output,'utf-8'))
                
                #if the path extension ends in css.
                elif (ext[1] == ".css"):
                    content = "text/css"
                    pageInfo = open(infopath).read()
                    contentlen = len(pageInfo)
                    output = ("HTTP/1.1 200 OK\nContent-Type: " +content+ "\nContent-Length: " + str(contentlen) + "\nConnection: Closed\n\n"+pageInfo)
                    print(output)
                    self.request.sendall(bytearray(output,'utf-8'))
                else:
                #Path extension ending is not css or html. Raise 404 Page Not Found Error.
                    content = "text/html"
                    output = ("HTTP/1.1 404 Not Found \nContent-Type: " +content+"\nConnection: Closed\n\n"+ "<!DOCTYPE HTML>\n<html>\n<head>\n <title>404 Not Found</title>\n</head>\n<body>\n <h1>Not Found</h1>\n  <p>The requested URL was not found on this server.</p>\n</body></html>")
                    self.request.sendall(bytearray(output,'utf-8'))
            

    #If the path is a directory
            elif (os.path.isdir(infopath)):
                val= http_request[1].decode('utf-8')
                #check if the path has '/' at the end. If not, redirect and add '/' to the end.
                if (val[-1]!= '/'):
                    infopath += "/"
                    redirect_info = "HTTP/1.1 301 Moved Permanently\nLocation: http://127.0.0.1:8080" + val + "/\n\n"
                    self.request.sendall(bytearray(redirect_info,'utf-8'))

                #Add /index.html to the ending of the path
                infopath += "index.html"

               
                content = "text/html"
                pageInfo = open(infopath).read()
                contentlen = len(pageInfo)
                output = ("HTTP/1.1 200 OK\nContent-Type: " +content+ "\nContent-Length: " +  str(contentlen) + "\nConnection: Closed\n\n"+pageInfo)
                print(output)
                self.request.sendall(bytearray(output,'utf-8'))
                

            else:
                #the path is not a file or a directory. Raise 404 error
                content = "text/html"
                output= ("HTTP/1.1 404 Not Found \nContent-Type: " +content+"\nConnection: Closed\n\n"+ "<!DOCTYPE HTML>\n<html>\n<head>\n <title>404 Not Found</title>\n</head>\n<body>\n  <h1>Not Found</h1>\n  <p>The requested URL was not found on this server.</p>\n</body></html>")
                self.request.sendall(bytearray(output,'utf-8'))
        else:
            #The method is not 'GET'. Rasie 405 Error
            output = ("HTTP/1.1 405 Method Not Allowed\nConnection: Closed\n\n")
            self.request.sendall(bytearray(output,'utf-8'))


        

        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    # Handler = http.server.SimpleHTTPRequestHandler

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
