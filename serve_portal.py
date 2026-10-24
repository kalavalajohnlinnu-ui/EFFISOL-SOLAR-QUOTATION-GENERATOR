import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080

class SecureCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Exact headers matching Netlify to trigger 'Content unavailable. Resource was not cached' in Chrome DevTools
        self.send_header('Cache-Control', 'public, max-age=0, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()

    def log_message(self, format, *args):
        # Silent logger to prevent any console leakage
        pass

def run():
    # Change directory to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Try port 8080, if busy try 8081, 8082, etc.
    global PORT
    while PORT < 8090:
        try:
            httpd = socketserver.TCPServer(("", PORT), SecureCacheHandler)
            break
        except OSError:
            PORT += 1

    url = f"http://localhost:{PORT}/index.html"
    print("=" * 60)
    print("  EffiSol Proposal Studio - Secure Local Server Active")
    print(f"  URL: {url}")
    print("  Security: Strict Cache Invalidation (DevTools Source-Proof)")
    print("=" * 60)
    print("Press Ctrl+C to stop the server.")
    
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == '__main__':
    run()
