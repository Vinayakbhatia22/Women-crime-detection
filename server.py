#!/usr/bin/env python3
"""
Localhost Development Server for SafeVision Analytics Dashboard.
-----------------------------------------------------------------
Serves the web dashboard on http://localhost:3000 with CORS headers
and automatically opens your default browser.
"""

import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 3000
HOST = "localhost"

class CustomHandler(SimpleHTTPRequestHandler):
    """Custom request handler with CORS support and clean console logging."""

    def end_headers(self):
        # Enable CORS for local testing
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        # Prevent aggressive caching during development
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def run_server():
    # Ensure working directory is the project root containing index.html
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    server_address = (HOST, PORT)
    try:
        httpd = HTTPServer(server_address, CustomHandler)
    except OSError:
        # Fallback if port 3000 is occupied
        fallback_port = 8080
        server_address = (HOST, fallback_port)
        httpd = HTTPServer(server_address, CustomHandler)

    url = f"http://{server_address[0]}:{server_address[1]}"
    print("=" * 60)
    print(f"🚀 SafeVision Localhost Dashboard Server Running!")
    print(f"👉 Local URL : {url}")
    print(f"📁 Serving   : {project_root}")
    print(f"🛑 Press Ctrl + C to stop the server.")
    print("=" * 60)

    # Automatically open the web browser
    webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server shutting down cleanly. Goodbye!")
        httpd.server_close()
        sys.exit(0)

if __name__ == "__main__":
    run_server()
