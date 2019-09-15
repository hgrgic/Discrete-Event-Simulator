import http.server
import socketserver


class TcpServer:

    def __init__(self, server_port=8080):
        self.server_port = server_port

    def start_server(self):
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", self.server_port), handler) as httpd:
            print("Server started on port", self.server_port)
            httpd.serve_forever()
