import pickle

from google.appengine.ext import db

import cardpile
import mtg_exceptions


class Player(db.Model):
  """Implements a user."""
  user = db.UserProperty(required=True, indexed=True)
  games = db.ListProperty(db.Key, required=True, default=[], indexed=False)
  decks = db.ListProperty(db.Blob, required=True, default=[], indexed=False)

  @staticmethod
  def load_or_create_by_user(user):
    """Returns a Player, creating it if it doesn't exist."""
    try:
      return Player.load_by_user(user)
    except mtg_exceptions.ModelNotFoundError:
      player = Player.new(user)
      player.put()
      return player

  @staticmethod
  def new(user):
    """Returns a new Player."""
    # Hack to add an initial deck
    #return Player(user=user)
    p = Player(user=user)
    p.set_deck(cardpile.CardPile([0, 1, 2]))

  @staticmethod
  def load_by_key(key):
    """Returns a Player loaded from the database."""
    model = Player.get(key)
    if not model:
      raise mtg_exceptions.ModelNotFoundError
    return model

  @staticmethod
  def load_by_user(user):
    """Returns a Player loaded from the database."""
    model = Player.all().filter('user =', user).get()
    if not model:
      raise mtg_exceptions.ModelNotFoundError
    return model

  @staticmethod
  def key_for_user(user):
    """Returns the player Key associated wth user in the database."""
    key = Player.all(keys_only=True).filter('user =', user).get()
    if not key:
      raise mtg_exceptions.ModelNotFoundError

  def add_game(self, gamekey):
    """Add a game for this player."""
    if gamekey not in self.games:
      self.games.append(gamekey)

  def get_deck(self, id):
    """Get the deck at a given id.

    Args:
      id: an integer deck id

    Returns:
      a CardPile instance
    """
    return pickle.loads(self.decks[id])

  def set_deck(self, deck, id=None):
    """Sets the deck at a given id.

    Args:
      deck: a CardPile instance
      id: the integer id of the deck to set; defaults to adding a new deck.

    Returns:
      the id of the deck
    """
    if not isinstance(deck, cardpile.CardPile):
      raise TypeError('deck must be an instance of CardPile.')
    if id is None:
      id = len(self.decks)
    self.decks[id] = db.Blob(pickle.dumps(deck))
    return id

  def itergamekeys(self):
    """Get all current games for this player."""
    return (g for g in self.games)
