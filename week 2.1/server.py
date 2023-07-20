import socketserver
from http.server import  SimpleHTTPRequestHandler as Simplehandler
import pandas as pd # unused import (it would have been bad if you actually used pandas in this class)
from networkclient import NetworkClient
from provider import Provider

class ServerHandler(Simplehandler):

    def do_GET(self):
        if not self.path.startswith("/data"):
            self.send_error(404)
            return
        
        info = [data for data in self.path.split("/") if data]
        try:
            if info[1] == "all":
                # Why not make the Provider in the initializer of this class?
                # Now you make new object for every request, even though it 
                # is basically immutable.
                # Also, you are making the same object independent of the enclosing 
                # `if`-statement, so you could have done that before the `if`
                prov = Provider() 
                json_data = prov.return_all()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json_data.encode("UTF-8"))

            year_1 = int(info[1])

            if len(info) == 3:
                year_2 = int(info[2])
                prov = Provider()
                json_data = prov.return_year(year_1,year_2)
                # Why are you creating a NetworkClient here (and in the other route)
                # (and not doing anything with the returned object)?
                # That object processes the data... I think this
                # displays a fundamental misunderstanding of how
                # network operations work...
                NetworkClient(self.path)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json_data.encode("UTF-8"))

            else:
                prov = Provider()
                json_data = prov.return_year(year_1)
                NetworkClient(self.path)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json_data.encode("UTF-8"))

        except ValueError:
            self.send_error(400)


        
# In this architecture it is imperative that you encapsulate the actual running within
# the main-scope.

port= 9000
socketserver.TCPServer.allow_reuse_address= True
http = socketserver.TCPServer(("localhost",port),ServerHandler)
print(f"serving on port {port}")
http.serve_forever()
