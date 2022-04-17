# -*- coding: utf-8 -*-

from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
import json
def jsonget(key_name):
   with  open("setting.json") as f:
        json_data = f.read()
   data = json.loads(json_data)
   f.close()
   return data[key_name]
def start():
   authorizer = DummyAuthorizer()
   authorizer.add_user(jsonget("ftpserveruser"), jsonget("ftpserverpass"), jsonget("ftpserverroot"), perm='elradfmwM')
   handler = FTPHandler
   handler.authorizer = authorizer
   server = FTPServer(('localhost', int(jsonget("ftpserverport"))), handler)
   server.serve_forever()
if __name__ == '__main__':
   start()