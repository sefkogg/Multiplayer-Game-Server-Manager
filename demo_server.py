import argparse
import socketserver

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall(b"DEMO GAME SERVER\n")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8765)
    args = p.parse_args()
    with socketserver.ThreadingTCPServer(("127.0.0.1", args.port), Handler) as server:
        server.allow_reuse_address = True
        print(f"Demo TCP server listening on 127.0.0.1:{args.port}")
        server.serve_forever()
