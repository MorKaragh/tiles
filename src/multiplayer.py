import socket
import struct
import threading
import traceback
import time

from src.game import TetrisGame
from src.gaming_grid import GamingGrid


class ConnectionStatus:

    def __init__(self):
        self.value = "IDLE"


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

    def send_message(self, msg: str):
        message = msg.encode("ascii")
        length = len(message)
        header = struct.pack("!I", length)
        self.socket.sendall(header)
        self.socket.sendall(message)

    def receive_message(self):
        header = self.socket.recv(4)
        if not header:
            return None
        message_length = struct.unpack("!I", header)[0]
        message = b''
        while len(message) < message_length:
            chunk = self.socket.recv(message_length - len(message))
            message += chunk
        return message.decode("ascii")

    def exchange(self, state: str):
        if not self.socket:
            print("no connection")
            return
        try:
            self.send_message(state)
            return self.receive_message()
        except Exception as e:
            print(e)

    def close(self):
        if self.socket:
            self.socket.close()
            print("closed connection")


class MultiplayerThread(threading.Thread):

    def __init__(self,
                 connection_status: ConnectionStatus,
                 player_grid: GamingGrid,
                 opponent_grid: GamingGrid,
                 host: str = "localhost",
                 port: int = 8080):
        threading.Thread.__init__(self)
        self.status = connection_status
        self.client = MultiplayerClient(host, port)
        self.client.connect()
        self.player_grid = player_grid
        self.opponent_grid = opponent_grid
        self.running = True

    def run(self):
        while self.running:
            print(self.status.value)
            if self.status.value in ["WFP", "WFS", "IDLE"]:
                e = self.client.exchange("ROOM:TESTROOM:PLAYER")
                self.status.value = e
            elif self.status.value == "READY":
                e = self.client.exchange("READY")
                if e == "GO":
                    self.status.value = "PLAYING"
            elif self.status.value == "PLAYING":
                e = self.client.exchange(self.player_grid.get_state())
                if e:
                    try:
                        self.opponent_grid.set_state(e)
                    except Exception:
                        traceback.print_exc()
            time.sleep(0.1)

    def terminate(self):
        self.running = False
        self.client.exchange("QUIT")
        self.client.close()


class Multiplayer:

    def __init__(self,
                 game: TetrisGame):
        self.game = game
        self.active = False
        self.status = ConnectionStatus()
        self.thread = MultiplayerThread(self.status, game.grid, game.opponent)

    def connect_to_room(self):
        if not self.active:
            self.thread.start()
            self.active = True

    def set_ready(self):
        self.status.value = "READY"
