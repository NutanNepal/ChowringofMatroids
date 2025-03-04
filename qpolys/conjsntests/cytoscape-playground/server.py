import os, json
from http.server import SimpleHTTPRequestHandler, HTTPServer

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/list-files':
            # List all JSON files in the 'data' folder
            files = [f for f in os.listdir('data') if f.endswith('.json')]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(files).encode())
        else:
            # Serve files normally
            super().do_GET()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, CustomHandler)
    print("Server running at http://localhost:8000")
    httpd.serve_forever()