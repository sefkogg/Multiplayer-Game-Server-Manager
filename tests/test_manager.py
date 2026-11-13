import socket
import threading
import unittest
from server_manager import check_server

class ServerTests(unittest.TestCase):
    def test_online(self):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(1)
            port = listener.getsockname()[1]
            t = threading.Thread(target=lambda: listener.accept()[0].close(), daemon=True)
            t.start()
            result = check_server({"name":"test","host":"127.0.0.1","port":port})
            self.assertEqual(result["status"], "online")
            t.join(timeout=2)
    def test_offline(self):
        result = check_server({"name":"test","host":"127.0.0.1","port":0}, timeout=.2)
        self.assertEqual(result["status"], "offline")

if __name__ == "__main__": unittest.main()
