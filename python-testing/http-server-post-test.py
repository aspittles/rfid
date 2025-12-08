from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

SECRET_TOKEN = 'my-secret-token'

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
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

if __name__ == '__main__':
    server = HTTPServer(('172.26.182.235', 8000), Handler)

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    print('Server running on http://172.26.182.235:8000')
    print('Press Enter to stop...')

    input()

    server.shutdown()
    print('Server stopped.')
