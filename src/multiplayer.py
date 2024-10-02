import socket
import struct
import threading
import traceback
import time

from pygame import Surface
from src.game import TetrisGame
from src.gaming_grid import GamingGrid
from src.scoreboard import ScoreBoard
from src.state_screen import StateScreen


class ConnectionStatus:

    def __init__(self):
        self.value = "IDLE"
        self.opponent_result = None


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
                 game: TetrisGame,
                 opponent_grid: GamingGrid,
                 opponent_scoreboard: ScoreBoard,
                 host: str = "localhost",
                 port: int = 8080):
        threading.Thread.__init__(self)
        self.game = game
        self.status = connection_status
        self.client = MultiplayerClient(host, port)
        self.client.connect()
        self.player_grid = self.game.grid
        self.opponent_grid = opponent_grid
        self.opponent_scoreboard = opponent_scoreboard
        self.running = True

    def run(self):
        while self.running:
            print(self.status.value)
            if self.status.value in ["WFP", "WFS", "IDLE"]:
                e = self.client.exchange("ROOM:TESTROOM:PLAYER")
                if self.status.value not in ["READY", "PLAYING"]:
                    self.status.value = e
            elif self.status.value == "READY":
                e = self.client.exchange("READY")
                if e == "GO":
                    self.status.value = "PLAYING"
            elif self.status.value == "PLAYING":
                msg = ("STATE;"
                       + str(self.game.scoreboard.level) + ":"
                       + str(self.game.scoreboard.score) + ";"
                       + self.player_grid.get_state())
                self._process_state_exchange(msg)
            elif self.status.value == "LOSS":
                msg = ("LOSS;"
                       + str(self.game.scoreboard.level) + ":"
                       + str(self.game.scoreboard.score) + ";")
                self._process_state_exchange(msg)
            time.sleep(0.1)

    def _process_state_exchange(self, msg: str):
        e = self.client.exchange(msg)
        if e and e.startswith("STATE;"):
            self.status.opponent_result = None
            split = e.split(";")
            score = split[1].split(":")[1]
            level = split[1].split(":")[0]
            try:
                self.opponent_scoreboard.level = level
                self.opponent_scoreboard.score = score
                self.opponent_grid.set_state(split[2:])
            except Exception:
                traceback.print_exc()
        elif e and e.startswith("LOSS"):
            split = e.split(";")
            self.status.opponent_result = split[1].split(":")[1]

    def terminate(self):
        self.running = False
        self.client.exchange("QUIT")
        self.client.close()


class Multiplayer:

    def __init__(self,
                 game: TetrisGame):
        self.game = game
        self.config = self.game.config
        self.opponent = GamingGrid(
            self.config.GRID_COLS,
            self.config.GRID_ROWS,
            "Black",
            self.config.SQUARE_SIZE)
        self.opponent_score = ScoreBoard(self.config, with_next_figure=False)
        self.active = False
        self.status = ConnectionStatus()
        self.thread = MultiplayerThread(
            self.status, self.game, self.opponent, self.opponent_score)

    def connect_to_room(self):
        if not self.active:
            self.thread.start()
            self.active = True

    def draw(self, screen: Surface):
        if self.status.opponent_result:
            StateScreen.draw_opponent_loss(screen, self.status.opponent_result)
        else:
            self.opponent.draw(screen)
            self.opponent_score.draw(screen)

    def reset(self):
        self.status.value = "PLAYING"

    def set_ready(self):
        self.status.value = "READY"

    def terminate(self):
        self.thread.terminate()
