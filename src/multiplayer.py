import socket
import threading
import time

from src.gaming_grid import GamingGrid

from typing import Callable


class MultiplayerClient:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(0.1)
        except Exception as e:
            print(e)

    def exchange(self, state: str):
        if not self.socket:
            print("no connection")
            return
        try:
            self.socket.sendall(state.encode("ascii"))
            response = self.socket.recv(1024)
            print(response.decode('ascii'))
            return response.decode("ascii")
        except Exception as e:
            print(e)

    def close(self):
        print("try close")
        if self.socket:
            self.socket.close()
            print("closed connection")


class MultiplayerThread(threading.Thread):

    def __init__(self,
                 client: MultiplayerClient,
                 player_grid: GamingGrid,
                 opponent_grid: GamingGrid):
        threading.Thread.__init__(self)
        self.client = client
        self.player_grid = player_grid
        self.opponent_grid = opponent_grid
        self.running = True

    def run(self):
        while self.running:
            print("cycle")
            e = self.client.exchange(self.player_grid.get_state())
            self.opponent_grid.set_state(e)
            time.sleep(0.1)

    def terminate(self):
        self.running = False
        self.client.close()
