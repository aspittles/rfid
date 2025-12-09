from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

SECRET_TOKEN = 'my-secret-token'

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Hello from GET')
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_POST(self):
        if self.path == '/open':
            token = self.headers.get('Authorization')
            
            if token != f'Bearer {SECRET_TOKEN}':
                self.send_response(401)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Unauthorized')
                return
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Hello World')
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), Handler)
    
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    
    print('Server running on http://0.0.0.0:8000')
    print('Press Enter to stop...')
    
    input()
    
    server.shutdown()
    print('Server stopped.')

# Testing Curls
#
# GET /status - no token required
# curl http://localhost:8000/status
#
# POST /open - token required
# curl -X POST -H "Authorization: Bearer my-secret-token" http://localhost:8000/open
#
# Invalid paths return 404
# curl http://localhost:8000/other
#
