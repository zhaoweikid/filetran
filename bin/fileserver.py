#!/usr/bin/python
# coding:utf-8
import os, sys 
import traceback
import posixpath
import shutil
import urllib, urllib2
import SimpleHTTPServer
import SocketServer
import getopt


class MyHandler (SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        rlen = int(self.headers.get('Content-Length', 0))
        if rlen == 0:
            self.send_response(400, 'size error')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return
        dirname  = os.path.dirname(self.path).strip(os.sep)
        filename = os.path.basename(self.path)
        filename = urllib2.unquote(filename)
        #print 'filename:', filename

        dirpath = os.path.join(BASE_DIR, dirname)
        #print 'dirpath:', dirpath

        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
           
        filepath = os.path.join(dirpath, filename)
        try:
            with open(filepath, 'wb+') as f:
                step = 16384 
                while rlen:
                    if rlen < step:
                        step = rlen
                    #print 'read:', step
                    content = self.rfile.read(step) 
                    f.write(content)
                    rlen -= len(content)
        except Exception, e:
            traceback.print_exc()
            content = 'Error, %s\n' % (str(e))
            self.send_response(500)
        else:
            content = 'OK, Created\n'
            self.send_response(201, 'Created')
       
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content)


    def do_PUT(self):
        return self.do_POST()

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = BASE_DIR
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/' 
        return path

    def list_directory(self, path):
        self.send_response(200, 'OK')
        return ''

def usage():
    print 'usage:'
    print '\tfileserver.py [options]'
    print 'options:'
    print '\t-p port'
    print '\t-d directory'
    sys.exit(-1)

def serve():
    global PORT, BASE_DIR
    try:
        options,args = getopt.getopt(sys.argv[1:],"p:d:",["port=","dir="]) 
        #if not options:
        #    usage()
        opt = dict(options)
        PORT = int(opt.get('-p', 8080))
        BASE_DIR = opt.get('-d', os.getcwd())
        if not os.path.isdir(BASE_DIR):
            print 'directory not exsit:%s, please use "-d dir"' % BASE_DIR
            sys.exit(-1)
    except getopt.GetoptError:
        usage()

    SocketServer.TCPServer.allow_reuse_address = True
    httpd = SocketServer.TCPServer(("", PORT), MyHandler)
    print "http serving at port:%d dir:%s" % (PORT, BASE_DIR)
    httpd.serve_forever()


if __name__ == '__main__':
    serve()

