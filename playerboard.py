import cardpile
import mtgexceptions


class PlayerBoard(object):
  """Implements a player's portion of a game board."""
  def __init__(self, deck, initial_life=20):
    """Initialize the PlayerBoard.

    Args:
      deck: a CardPile of the player's deck.
      initial_life: player's starting life as an integer
    """
    self.deck = deck
    self.library = cardpile.CardPile()
    self.graveyard = cardpile.CardPile()
    self.battlefield = cardpile.CardPile()
    self.exile = cardpile.CardPile()
