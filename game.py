from google.appengine.api import users
from google.appengine.ext import db

import mtg_exceptions


STATE_PRE = 0
STATE_CURRENT = 1
STATE_COMPLETE = 2


class Game(db.Model):
  """Implements a game."""
  players = db.ListProperty(db.Key, required=True, default=[],
                            indexed=False)
  state = db.IntegerProperty(required=True, default=STATE_PRE, indexed=False) 
  data = db.TextProperty(indexed=False)

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

  def add_player(self, player_key, deck):
    """Add a player.

    Only works during the STATE_PRE state.

    Args:
      player_key: database key associated with the player
      deck: a CardPile to use as the player's deck
    """
    if not self.state == STATE_PRE:
      raise RuntimeError('Player can\'t join this game because play has begun.')
    if not player_key in self.players:
      self.players.append(player_key)

  def iterplayerkeys(self):
    return (p for p in self.players)

  def is_active(self):
    return self.state == STATE_PRE or self.state == STATE_CURRENT

  def do(self, action):
    pass
