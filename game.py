import pickle

from google.appengine.api import users
from google.appengine.ext import db

import mtg_exceptions
import playerboard


STATE_JOIN = 0
STATE_PLAY = 1
STATE_COMPLETE = 2


class Game(db.Model):
  """Implements a game."""
  players = db.ListProperty(db.Key, required=True, default=[],
                            indexed=False)
  state = db.IntegerProperty(required=True, default=STATE_JOIN, indexed=False) 
  boards = db.ListProperty(db.Blob, required=True, default=[], indexed=False)

  @staticmethod
  def new():
    """Returns a new Game."""
    return Game()

  @staticmethod
  def load_by_key(key):
    """Returns a game loaded from the database."""
    model = Game.get(key)
    if not model:
      raise mtg_exceptions.ModelNotFoundError
    return model

  def add_player(self, player_key, deck, initial_life=20):
    """Add a player.

    Only works before the game starts (state == STATE_JOIN).

    Args:
      player_key: database key associated with the player
      deck: a CardPile to use as the player's deck
    """
    if not self.state == STATE_JOIN:
      raise RuntimeError('Player can\'t join this game because play has begun.')
    if not player_key in self.players:
      assert len(self.players) == len(self.boards)
      self.players.append(player_key)
      self.boards.append(
          playerboard.PlayerBoard(deck, initial_life=initial_life))

  def iterplayerkeys(self):
    return (p for p in self.players)

  def is_active(self):
    return self.state == STATE_JOIN or self.state == STATE_PLAY

  def do(self, action):
    pass

  def get_playerboard(self, player_key):
    """Get the board for a given player.

    Args:
      player_key: database key associated with the player

    Returns:
      a PlayerBoard instance
    """
    return pickle.loads(self.boards.index(player_key))

  def set_playerboard(self, board, player_key):
    """Sets the board for a given player.

    Args:
      deck: a PlayerBoard instance
      player_key: database key associated with the player
    """
    if not isinstance(board, playerboard.PlayerBoard):
      raise TypeError('deck must be an instance of PlayerBoard.')
    self.boards[self.boards.index(player_key)] = db.Blob(pickle.dumps(board))


