import logging
import threading
from abc import abstractmethod
from typing import Dict

from simple_websocket import Server

from backend.app.managers.entity import Player
from backend.app.managers.game import AGame, SIGame

logger = logging.getLogger(__name__)


class AServerManager:
    # manager responsible for handling all games (if game is active - from memory, if persisted but not active - from storage)

    def __init__(self):
        self.games: Dict[str, AGame] = dict()
        self.player_id_to_game: Dict[str, AGame] = dict()
        self.player_id_to_socket: Dict[str, Server] = dict()


    def register_player(self, player: Player):
        game_id = player.game_id
        game = self.get_game_by_id(game_id)
        if game is None:
            return {'error': f'Game identified by {game_id} not found'}, 400
        game.register_player(player)
        self.player_id_to_game[player.id] = game
        return player

    def unregister_player(self, player: Player):
        game = self.get_game_by_player_id(player.id)
        game.unregister_player(player)
        del self.player_id_to_game[player.id]


    def _check_signals(self):
        for game in self.games.values():
            game.check_signals()

    def check_signals(self, interval: int=5):
        self._check_signals()
        threading.Timer(interval, self.check_signals, [interval]).start()

    @abstractmethod
    def get_game_by_id(self, id: str):
            pass

    @abstractmethod
    def create_game(self, game: AGame) -> Player:
        pass


    @abstractmethod
    def get_game_by_player_id(self, player_id: str):
        pass

    def register_socket(self, user_id: str, socket):
        self.player_id_to_socket[user_id] = socket

    def get_socket_by_player_id(self, player_id: str):
        return self.player_id_to_socket.get(player_id)


class SIServerManager(AServerManager):

    def __init__(self):
        super().__init__()
        self.interval_seconds = 1

        self.check_signals(interval=self.interval_seconds)

        self.game_token_to_id: Dict[str, str] = dict()

    def get_game_by_player_id(self, player_id: str):
        return self.player_id_to_game.get(player_id)

    def get_game_by_id(self, id: str):
        if id in self.game_token_to_id:
            id = self.game_token_to_id[id]
        game = self.games.get(id)
        if game is None:
            # TODO implement fetching persisted game
            pass
        return game

    def create_game(self, host_name=None) -> AGame:
        game = SIGame(self)
        self.games[game.id] = game
        self.game_token_to_id[game.token] = game.id
        host_name = host_name or "Host"
        host = Player(host_name, game.token)
        game.register_host(host)
        return game

