import socket


class MultiplayerClient:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
        except Exception as e:
            print(e)

    def exchange(self, state: str):
        if not self.socket:
            print("no connection")
            return

        try:
            self.socket.sendall(state.encode("ascii"))
            response = self.socket.recv(1024)
            while response:
                print(response.decode("ascii"))
                response = self.recv(1024)
        except Exception as e:
            print(e)

    def close(self):
        if self.socket:
            self.socket.close()
            print("closed connection")
