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
            response = self.socket.recv(2048)
            return response.decode("ascii").rstrip("\x00")
        except Exception as e:
            print(e)
            print(f"response: {response}")

    def close(self):
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
            e = self.client.exchange(self.player_grid.get_state())
            self.opponent_grid.set_state(e)
            time.sleep(0.1)

    def terminate(self):
        self.running = False
        self.client.close()
