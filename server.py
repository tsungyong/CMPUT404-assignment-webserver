import SocketServer
# coding: utf-8
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Tsung Lin Yong
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


class MyWebServer(SocketServer.BaseRequestHandler):
    
    STATUS_OK = "HTTP/1.1 200 OK"
    STATUS_NOT_FOUND = "HTTP/1.1 404 Not Found"

    def handle(self):

        self.data = self.request.recv(1024).strip()

        httpGetLine = self.data.splitlines()[0]

        response = ""

        requestedFilePath = self.getRequestedFilePath(httpGetLine)
        contentType = self.getContentType(requestedFilePath)

        # make sure the path exists and is located in ./www/
        if (self.isPathInDirectory(requestedFilePath,
                                   os.path.join(os.getcwd(), "www")) and
            os.path.exists(requestedFilePath)):

            with open(requestedFilePath) as f:

                response = ("%s\r\n"
                            "Connection: close\r\n"
                            "Content-Type: %s\r\n"
                            "Content-Length: %s\r\n\r\n"
                            "%s" %
                            (self.STATUS_OK, contentType,
                             os.path.getsize(requestedFilePath), f.read()))

        # the path doesn't exist, so return 404 not found
        else:

            response = ("%s\r\n"
                        "Connection: close\r\n"
                        "Content-Type: %s\r\n"
                        "Content-Length: 0" %
                        (self.STATUS_NOT_FOUND, contentType))
                    
        self.request.sendall(response)

    def getRequestedFilePath(self, httpGetLine):

        requestedFile = httpGetLine.split()[1]

        requestedFilePath = os.path.join(os.getcwd(),
                                         "www",
                                         requestedFile[1:])

        # if the requested path is a directory, serve the index file
        if os.path.isdir(requestedFilePath):
            requestedFilePath = os.path.join(requestedFilePath,
                                                     "index.html")

        return requestedFilePath

    def getContentType(self, requestedFile):

        fileName, fileExtension = os.path.splitext(requestedFile)
        return "text/%s" % fileExtension[1:]

    def isPathInDirectory(self, path, directory):

        directoryAbs = os.path.abspath(directory)
        pathAbs = os.path.abspath(path)

        if pathAbs[:len(directoryAbs)] == directoryAbs:
            return True

        return False

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
