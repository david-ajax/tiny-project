#!/usr/bin/env python
 
# taken from https://gist.github.com/dergachev/7028596
# 
# generate server.xml with the following command:
#   openssl req -new -x509 -keyout https_svr_key.pem -out https_svr_key.pem -days 3650 -nodes
#
# run as follows:
#    python https_svr.py
#
# then in your browser, visit:
#    https://localhost:4443
#
 
import BaseHTTPServer
import SimpleHTTPServer
import os
import socket
import ssl
 
script_home = os.path.dirname(os.path.abspath(__file__))
ip = [(s.connect(('1.1.1.1', 53)), s.getsockname()[0], s.close()) \
      for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
port = 443
 
def main():
    print ("simple https server, address:%s:%d, document root:%s" % (ip, port, script_home))
 
    httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', port), SimpleHTTPServer.SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./https_svr_key.pem', server_side=True)
    httpd.serve_forever()
 
if __name__ == '__main__':
    os.chdir(script_home)
    main()
