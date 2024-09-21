import socket
import struct
import threading
import traceback
import time

from src.gaming_grid import GamingGrid


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
                 player_grid: GamingGrid,
                 opponent_grid: GamingGrid):
        threading.Thread.__init__(self)
        self.client = MultiplayerClient("localhost", 8080)
        self.client.connect()
        self.player_grid = player_grid
        self.opponent_grid = opponent_grid
        self.running = True
        self.state = "ROOM"

    def run(self):
        while self.running:
            if self.state == "ROOM":
                e = self.client.exchange("ROOM:TESTROOM:PLAYER")
                if e == "WFS":
                    self.state = "PLAYING"
                print(e)
            elif self.state == "PLAYING":
                e = self.client.exchange(self.player_grid.get_state())
                print("received" + str(e))
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
