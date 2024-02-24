from http.server import BaseHTTPRequestHandler, HTTPServer
hostName = "0.0.0.0"
serverPort = 8180

import moon_new
import json

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            i = self.path.index ( "?" ) + 1
            params = dict ( [ tuple ( p.split("=") ) for p in self.path[i:].split ( "&" ) ] )
            if params['lat'] and params['lon']:
                do_moon(self, params)
        except Exception as e:
            self.send_response(501)
            self.send_header("Server", "yes")
            self.end_headers()

def do_moon(self, params):
    self.send_response(200)
    self.send_header("Server", "moon")
    self.send_header("Content-type", "application/json")
    self.end_headers()
    moon_data = moon_new.get_moon_data(params['lat'], params['lon'])
    alt, phase, percent = moon_data
    seven_seg = moon_new.format7seg(moon_data)
    json_str = json.dumps( { "alt": alt, "phase": phase, "percent": percent, "seven_seg": seven_seg } )
    print(json_str)
    self.wfile.write(bytes(json_str, "utf-8"))

def create_server():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    webServer.serve_forever()

import threading
threading.Thread(target=create_server).start()
