import pickle

from google.appengine.api import users
from google.appengine.ext import db

import mtg_exceptions
import playerboard


STATE_JOIN = 0
STATE_PLAY = 1
STATE_DONE = 2


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
      pboard = playerboard.PlayerBoard(deck, initial_life=initial_life)
      self.boards.append(db.Blob(pickle.dumps(pboard)))

  def iterplayerkeys(self):
    return (p for p in self.players)

  def is_joinable(self):
    """Return True if the game is still accepting players."""
    return self.state == STATE_JOIN

  def is_playable(self):
    """Return True if we are in the playing state."""
    return self.state == STATE_PLAY

  def has_player(self, player_key):
    """Returns whether the player is in the game."""
    return player_key in self.players

  def has_owner(self, player_key):
    """Returns whether the player is the owner of the game."""
    return len(self.players) > 0 and player_key == self.players[0]

  def player_count(self):
    """Returns the number of players in the game."""
    return len(self.players)

  def _set_state(self, state):
    """Set the game state.

    Args:
      state: one of STATE_JOIN, STATE_PLAY, or STATE_DONE.
    """
    assert state in (STATE_JOIN, STATE_PLAY, STATE_DONE)
    self.state = state

  def start(self):
    """Start the game."""
    assert self.player_count() > 1
    self._set_state(STATE_PLAY)

  def do(self, action):
    pass

  def get_playerboard(self, player_key):
    """Get the board for a given player.

    Args:
      player_key: database key associated with the player

    Returns:
      a PlayerBoard instance
    """
    assert player_key in self.players
    return pickle.loads(self.boards[self.players.index(player_key)])

  def set_playerboard(self, board, player_key):
    """Sets the board for a given player.

    Args:
      deck: a PlayerBoard instance
      player_key: database key associated with the player
    """
    assert isinstance(board, playerboard.PlayerBoard)
    assert player_key in self.players
    assert len(self.players) == len(self.boards)
    self.boards[self.players.index(player_key)] = db.Blob(pickle.dumps(board))


