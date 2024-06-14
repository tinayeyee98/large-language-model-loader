from http.server import HTTPServer
from handler import ChatRequestHandler
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
host = os.getenv("HOST", "localhost")
port = int(os.getenv("SERVER_PORT", 5000))

def run_server():
    """
    Starts the HTTP server with the specified host and port, and listens for incoming HTTP requests.

    Usage:
        This function is called when the script is executed directly. It will print the server address and
        start the server to handle incoming requests.
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, ChatRequestHandler)
    print(f"Server running at http://{host}:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
