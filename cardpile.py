import mtgapi

import random


class CardPile(object):
  def __init__(self, cards=[]):
    self._cards = list(cards)

  def iterimages(self):
    return (mtgapi.image_url(mid) for mid in self._cards)

  def itermultiverseids(self):
    return (mid for mid in self._cards)

  def pop(self, card):
    """Remove a card from the top of the pile.

    Returns:
      The removed card.
    """
    return self._cards.pop()

  def push(self, card):
    """Places a card on the top of the pile."""
    self._cards.append(card)

  def push_bottom(self, card):
    """Places a card on the bottom of the pile."""
    self._cards.insert(0, card)

  def shuffle(self):
    """Shuffles the pile randomly."""
    random.shuffle(self._cards)

  def size(self):
    """Returns the number of cards in the pile."""
    return len(self._cards)
