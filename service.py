import threading

import xbmc
import requests

try:
    # Python3
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from socketserver import ThreadingMixIn
except:
    # Python2
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
    from SocketServer import ThreadingMixIn

HOST = '127.0.0.1'
PORT = 9999
REMOVE_IN_HEADERS = ['upgrade', 'host']
REMOVE_OUT_HEADERS = ['date', 'server', 'transfer-encoding', 'keep-alive', 'connection', 'content-length']

class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_POST(self):
        self.send_error(404)

    def do_HEAD(self):
        self.send_error(404)

    def do_GET(self):
        url = self.path.lstrip('/').strip('\\')
        if not url.endswith('.m3u8'):
            self.send_error(404)

        headers = {}
        for key in self.headers:
            if key.lower() not in REMOVE_IN_HEADERS:
                headers[key] = self.headers[key]

        response = requests.get(url, headers=headers)

        self.send_response(response.status_code)

        for key in response.headers:
            if key.lower() not in REMOVE_OUT_HEADERS:
                self.send_header(key, response.headers[key])

        self.end_headers()

        ## Edit the content
        content = response.content.decode('utf8')
        content = content.replace('f08e80da-bf1d-4e3d-8899-f0f6155f6efa', 'https://bitmovin-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa')

        # Output the content
        self.wfile.write(content.encode('utf8'))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

server = ThreadedHTTPServer((HOST, PORT), RequestHandler)
server.allow_reuse_address = True
httpd_thread = threading.Thread(target=server.serve_forever)
httpd_thread.start()

xbmc.Monitor().waitForAbort()

server.shutdown()
server.server_close()
server.socket.close()
httpd_thread.join()
