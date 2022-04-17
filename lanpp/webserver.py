#!/usr/bin/env python3
 
"""
Powered by "Simple HTTP Server With Upload." 
https://gist.github.com/UniIsland/3346170
"""
 
 
__version__ = "1.0"
__all__ = ["SimpleHTTPRequestHandler"]
__author__ = "bones7456"
__home_page__ = "https://gist.github.com/UniIsland/3346170"
import getpass
import os
import posixpath
import http.server
import socketserver
import urllib.request, urllib.parse, urllib.error
import html
import shutil
import mimetypes
import re
import argparse
import base64
from io import BytesIO
import json

def jsonget(key_name):
   with  open("setting.json") as f:
        json_data = f.read()
   data = json.loads(json_data)
   f.close()
   return data[key_name]
def start():
    theport = int(jsonget('webserverport'))
    os.chdir(jsonget('webserverroot'))
    class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    
        """Simple HTTP request handler with GET/HEAD/POST commands.

        This serves files from the current directory and any of its
        subdirectories.  The MIME type for files is determined by
        calling the .guess_type() method. And can reveive file uploaded
        by client.

        The GET/HEAD/POST requests are identical except that the HEAD
        request omits the actual contents of the file.

        """
    
        server_version = "SimpleHTTPWithUpload/" + __version__
    
        def do_GET(self):
            """Serve a GET request."""
            f = self.send_head()
            if f:
                self.copyfile(f, self.wfile)
                f.close()
    
        def do_HEAD(self):
            """Serve a HEAD request."""
            f = self.send_head()
            if f:
                f.close()
    
        def do_POST(self):
            """Serve a POST request."""
            r, info = self.deal_post_data()
            print((r, info, "by: ", self.client_address))
            f = BytesIO()
            f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
            f.write(b"<html>\n<title>\xe4\xb8\x8a\xe4\xbc\xa0\xe7\xbb\x93\xe6\x9e\x9c\xe9\xa1\xb5\xe9\x9d\xa2</title>\n")
            f.write(b"<body>\n<h2>\xe4\xb8\x8a\xe4\xbc\xa0\xe7\xbb\x93\xe6\x9e\x9c\xe9\xa1\xb5\xe9\x9d\xa2</h2>\n")
            f.write(b"<hr>\n")
            if r:
                f.write(b"<strong>\xe6\x88\x90\xe5\x8a\x9f:</strong>")
            else:
                f.write(b"<strong>\xe5\xa4\xb1\xe8\xb4\xa5:</strong>")
            f.write(info.encode())
            f.write(("<br><a href=\"%s\">返回</a>" % self.headers['referer']).encode())
            f.write(b"<hr><small>\xe4\xbb\xa5LAN++\xe4\xb8\xba\xe9\xa9\xb1\xe5\x8a\xa8 | \xe6\xba\x90\xe4\xbb\xa3\xe7\xa0\x81\xe5\x8f\x96\xe8\x87\xaabones7456")
            f.write(b'<br><a href=\"http://david-ajax.github.io/LANpp/index.html">')
            f.write(b"\xe5\xae\x98\xe6\x96\xb9\xe7\xbd\x91\xe7\xab\x99</a>.</small></body>\n</html>\n")
            length = f.tell()
            f.seek(0)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(length))
            self.end_headers()
            if f:
                self.copyfile(f, self.wfile)
                f.close()
            
        def deal_post_data(self):
            uploaded_files = []
            content_type = self.headers['content-type']
            if not content_type:
                return (False, "内容类型头不含有边界")
            boundary = content_type.split("=")[1].encode()
            remainbytes = int(self.headers['content-length'])
            line = self.rfile.readline()
            remainbytes -= len(line)
            if not boundary in line:
                return (False, "内容没有边界")
            while remainbytes > 0:
                line = self.rfile.readline()
                remainbytes -= len(line)
                fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line.decode())
                if not fn:
                    return (False, "无法获取文件名...")
                path = self.translate_path(self.path)
                fn = os.path.join(path, fn[0])
                line = self.rfile.readline()
                remainbytes -= len(line)
                line = self.rfile.readline()
                remainbytes -= len(line)
                try:
                    out = open(fn, 'wb')
                except IOError:
                    return (False, "无法写入文件<br>您是否以足够的权限运行LAN++及其组件?您是否选择了文件以上传?")
                else:
                    with out:                    
                        preline = self.rfile.readline()
                        remainbytes -= len(preline)
                        while remainbytes > 0:
                            line = self.rfile.readline()
                            remainbytes -= len(line)
                            if boundary in line:
                                preline = preline[0:-1]
                                if preline.endswith(b'\r'):
                                    preline = preline[0:-1]
                                out.write(preline)
                                uploaded_files.append(fn)
                                break
                            else:
                                out.write(preline)
                                preline = line
            return (True, "文件 '%s' 上传成功" % ",".join(uploaded_files))
    
        def send_head(self):
            path = self.translate_path(self.path)
            f = None
            if os.path.isdir(path):
                if not self.path.endswith('/'):
                    # redirect browser - doing basically what apache does
                    self.send_response(301)
                    self.send_header("Location", self.path + "/")
                    self.end_headers()
                    return None
                for index in "index.html", "index.htm":
                    index = os.path.join(path, index)
                    if os.path.exists(index):
                        path = index
                        break
                else:
                    return self.list_directory(path)
            ctype = self.guess_type(path)
            try:
                # Always read in binary mode. Opening files in text mode may cause
                # newline translations, making the actual size of the content
                # transmitted *less* than the content-length!
                f = open(path, 'rb')
            except IOError:
                self.send_error(404, "没有找到文件 错误码:404")
                return None
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
    
        def list_directory(self, path):
            try:
                list = os.listdir(path)
            except os.error:
                self.send_error(404, "No permission to list directory")
                return None
            list.sort(key=lambda a: a.lower())
            f = BytesIO()
            displaypath = html.escape(urllib.parse.unquote(self.path))
            f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
            f.write(("<html>\n<title>此目录下的文件列表: %s</title>\n" % displaypath).encode())
            f.write(b'<style type="text/css">\n')
            f.write(b'a { text-decoration: none; }\n')
            f.write(b'a:link { text-decoration: none; font-weight: bold; color: #0000ff; }\n')
            f.write(b'a:visited { text-decoration: none; font-weight: bold; color: #0000ff; }\n')
            f.write(b'a:active { text-decoration: none; font-weight: bold; color: #0000ff; }\n')
            f.write(b'a:hover { text-decoration: none; font-weight: bold; color: #ff0000; }\n')
            f.write(b'</style>\n')
            f.write(("<body>\n<h2>此目录下的文件列表:" + displaypath + "</2><br/><h5>注意:<br/>1:您当前以[" + getpass.getuser() + "]用户查看文件(您或许对某些文件没有查看权限)<br>2:选择文件上传后,如文件较大,请只点击一次按钮直到页面刷新</h5>").encode())
            f.write(b"<hr>\n")
            f.write(b"<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
            f.write(b"<input name=\"file\" type=\"file\" multiple/>")
            f.write(b"<input type=\"submit\" value=\"\xe4\xb8\x8a\xe4\xbc\xa0\xe9\x80\x89\xe6\x8b\xa9\xe7\x9a\x84\xe6\x96\x87\xe4\xbb\xb6\"/></form>\n")
            f.write(b"<hr>\n")
            f.write(b'<a href="../"><img src="data:image/png;base64,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" alt="[PARENTDIR]" width="24" height="24">&nbsp;&nbsp;&nbsp;\xe8\xbf\x94\xe5\x9b\x9e\xe7\x88\xb6\xe7\x9b\xae\xe5\xbd\x95</a><br />\n')
            for name in list:
                dirimage = 'data:image/png;base64,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BICE5bt8nsfjYdW9qQIgACQ8rM65a4jokvAO0VcCEAAyXUidc78moqOn6xJtNQABINOFM0mS1cz8y+m6RFsNQADI9OFct27dKw4cOFD8BE/Vzxemn7SdDgAEgOglLUmST5WfjawmouV6nTvrBEAAiH74Nm3a9JK9e/ces7S0dJR+d5WOxZmueDjPpAOAAJBJGbH3unOueGoVACm21jknVbYYNytWccnGGADyvH0EIDZCrakCgAAQzTyZ6wVAAIi5UGsKAiAARDNP5noBEABiLtSaggAIANHMk7leAASAmAu1piAAAkA082SuFwABIOZCrSkIgAAQzTyZ6wVAAIi5UGsKAiAARDNP5noBEABiLtSaggAIANHMk7leAASAmAu1piAAAkA082SuFwABIOZCrSkIgAAQzTyZ6wVAAIi5UGsKAiAARDNP5noBEABiLtSaggAIANHMk7leAASAmAu1piAAAkA082SuFwABIOZCrSkIgAAQzTyZ6wVAAIi5UGsKAiAARDNP5noBEABiLtSaggAIANHMk7leAASAmAu1piAAAkA082SuFwABIOZCrSkIgAAQzTyZ6wVAAIi5UGsKAiAARDNP5noBEABiLtSaggAIANHMk7leAASAmAu1piAAAkA082SuFwABIOZCrSkIgAAQzTyZ6wVAAIi5UGsKAiAARDNP5noBEABiLtSaggAIANHMk7leAASAmAu1piAAAkA082SuFwABIOZCrSkIgAAQzTyZ6wVAAIi5UGsKAiAARDNP5noBEABiLtSaggAIANHMk7leAASAmAu1piAAAkA082SuFwABIOZCrSkIgAAQzTyZ6wVAAIi5UGsKAiAARDNP5noBEABiLtSaggAIANHMk7leAASAmAu1piAAAkA082SuFwABIOZCrSkIgAAQzTyZ6wVAAIi5UGsKAiAARDNP5noBEABiLtSaggAIANHMk7leAASAmAu1piAAAkA082SuFwABIOZCrSkIgAAQzTyZ6wVAAIi5UGsKAiAARDNP5noBEABiLtSaggAIANHMk7leAASAmAu1piAAAkA082SuFwABIOZCrSkIgAAQzTyZ6wVAAIi5UGsKAiAARDNP5noBEABiLtSaggAIANHMk7leAASAmAu1piAAAkA082SuFwABIOZCrSkIgAAQzTyZ6wVAAIi5UGsKAiAARDNP5noBEABiLtSaggAIANHMk7leAASAmAu1piAAAkA082SuFwABIOZCrSkIgAAQzTyZ6wVAAIi5UGsKAiAvBOSvRHTkJIOZ+U1pmu6cNA6v998B59y3iGjrJCXMfFGapjdMGqf5Oms2q9LLOfcoEa2ZNJaZz03T9KZJ4/B6/x1wzu0hotdPUiIiZ2VZ9rVJ4zRf7wKQHxHRWyuIeNh7v7HCOAzpsQNJklzAzFXPCid77x9oU24XgFxBRJdXFHmL9/7simMxrIcOOOf2E9HyKktfXFw8bGFh4ekqY7XGtA7I/Pz8hjzPH6ohYLP3/p4a4zG0Bw4Mh8MjROReItpQZbki8o0sy86sMlZzTOuAFIt3zu0mouNqCLk2z/OvjsfjXTVqMDRCB5xzxd8aJxPR52su7zzv/Rdq1kw9vCtALiWiqwJW/xQRFXDtC6hFSfcOvIGIVtVdhogsMPMG7/2f69ZOO74TQFavXv2ylStXPkxEx08rAPX2HWDmS9I0va4LpZ0AUl5mnRdwmu3CI8zZrQM/X7FixYadO3ce6GIZnQFSiE2SZDszn9GFcMzZGwc6fZOmU0DKM8nvieg1vdkuLLQ1B5j5wjRNP9fahP9nos4BKSF5kIjwoWCXSYhv7vO99zd2vawoACkhuYSIrunaEMzfuQO/Y+b3pGm6o/OVEFE0gBRmDIfDLSJSvAV8QgzmYA3tOiAity9btuyTo9HItzvzoWeLCpBimRs3bjxs3759BSTFfzhmw4HiEvta731xV29UR3SAHHQnSZLVzHyqiJxa/D8q17AYDQf+RkR3DQaDO0ej0V0aDZvoES0g/y322GOPPXLlypUvX1paOpKZK93c1oRh6BnuwGAweHL//v1PPPvss0/s2bPnyfBO7VX2BpD2LMFMcOA/DgAQpAEOvIgDAATxgAMABBmAA2EO4AwS5huqZsQBADIjGw2ZYQ4AkDDfUDUjDgCQGdloyAxzAICE+YaqGXEAgMzIRkNmmAMAJMw3VM2IAwBkRjYaMsMc+BeLyV0yKtmxMAAAAABJRU5ErkJggg=='
                fullname = os.path.join(path, name)
                displayname = linkname = name
                # Append / for directories or @ for symbolic links
                if os.path.isdir(fullname):
                    dirimage = 'data:image/png;base64,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'
                    displayname = name + "/"
                    linkname = name + "/"
                if os.path.islink(fullname):
                    dirimage = 'data:image/png;base64,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'
                    displayname = name + "@"
                if name.endswith(('.bmp','.gif','.jpg','.png')):
                    dirimage = 'data:image/png;base64,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'
                if name.endswith(('.avi','.mpg')):
                    dirimage = 'data:image/png;base64,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'
                if name.endswith(('.idx','.srt','.sub')):
                    dirimage = name
                if name.endswith('.iso'):
                    dirimage = name
                # Note: a link to a directory displays with @ and links with /
                f.write(('<a href="%s"><img src="%s" width="24" height="24">&nbsp;&nbsp;&nbsp;%s</a><br />\n'
                        % (urllib.parse.quote(linkname), dirimage , html.escape(displayname))).encode())
            f.write(b"<hr>\n</body>\n</html>\n")
            length = f.tell()
            f.seek(0)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(length))
            self.end_headers()
            return f
    
        def translate_path(self, path):
            """Translate a /-separated PATH to the local filename syntax.
            Components that mean special things to the local file system
            (e.g. drive or directory names) are ignored.  (XXX They should
            probably be diagnosed.)

            """
            # abandon query parameters
            path = path.split('?',1)[0]
            path = path.split('#',1)[0]
            path = posixpath.normpath(urllib.parse.unquote(path))
            words = path.split('/')
            words = [_f for _f in words if _f]
            path = os.getcwd()
            for word in words:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir): continue
                path = os.path.join(path, word)
            return path
    
        def copyfile(self, source, outputfile):
            """Copy all data between two file objects.

            The SOURCE argument is a file object open for reading
            (or anything with a read() method) and the DESTINATION
            argument is a file object open for writing (or
            anything with a write() method).

            The only reason for overriding this would be to change
            the block size or perhaps to replace newlines by CRLF
            -- note however that this the default server uses this
            to copy binary data as well.

            """
            shutil.copyfileobj(source, outputfile)
    
        def guess_type(self, path):
            """Guess the type of a file.

            Argument is a PATH (a filename).

            Return value is a string of the form type/subtype,
            usable for a MIME Content-type header.

            The default implementation looks the file's extension
            up in the table self.extensions_map, using application/octet-stream
            as a default; however it would be permissible (if
            slow) to look inside the data to make a better guess.

            """
    
            base, ext = posixpath.splitext(path)
            if ext in self.extensions_map:
                return self.extensions_map[ext]
            ext = ext.lower()
            if ext in self.extensions_map:
                return self.extensions_map[ext]
            else:
                return self.extensions_map['']
    
        if not mimetypes.inited:
            mimetypes.init() # try to read system mime.types
        extensions_map = mimetypes.types_map.copy()
        extensions_map.update({
            '': 'application/octet-stream', # Default
            '.py': 'text/plain',
            '.c': 'text/plain',
            '.h': 'text/plain',
            })
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', '-b', default='', metavar='ADDRESS',
                            help='Specify alternate bind address '
                                '[default: all interfaces]')
    parser.add_argument('port', action='store',
                            default=theport, type=int,
                            nargs='?',
                            help='Specify alternate port [default:' + str(theport) + ']')
    args = parser.parse_args()

    PORT = args.port
    BIND = args.bind
    HOST = BIND

    if HOST == '':
        HOST = 'localhost'

    Handler = SimpleHTTPRequestHandler

    with socketserver.TCPServer((BIND, PORT), Handler) as httpd:
        serve_message = "[Webserver - 1.0]\nServing HTTP on {host} port {port} (http://{host}:{port}/) ..."
        print(serve_message.format(host=HOST, port=PORT))
        httpd.serve_forever()
if __name__ == "__main__":
    start()