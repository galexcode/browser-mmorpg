import webapp2

from google.appengine.api import users
from google.appengine.ext import db

import game
import mtg_exceptions
import player
import render


def authenticated(func):
  """Decorator forcing a user to authenticate before proceeding."""
  def auth_wrapper(self):
    user = users.get_current_user()
    if user:
      func(self, user)
    else:
      self.redirect(users.create_login_url(self.request.uri))
  return auth_wrapper

def authenticated_player(func):
  """Decorator providing an authenticated player."""
  @authenticated
  def player_wrapper(self, user):
    current_player = player.Player.load_or_create_by_user(user)
    func(self, current_player)
  return player_wrapper

def authenticated_game(func):
  """Decorator providing an authenticated player and game."""
  @authenticated_player
  def game_wrapper(self, current_player):
    game_key = self.request.get('game_key')
    try:
      game_obj = game.Game.load_by_key(db.Key(game_key))
    except mtg_exceptions.ModelNotFoundError:
      self.redirect('/')
      return
    func(self, current_player, game_obj)
  return game_wrapper


class GameListPage(webapp2.RequestHandler):
  """Manage current games."""
  @authenticated_player
  def get(self, current_player):
    """List current games."""
    self.respond(current_player)

  @authenticated_player
  def post(self, current_player):
    """Create a new game."""
    action = self.request.get('action')
    if action == 'new':
      new_game = game.Game.new()
      new_game.put()
      current_player.add_game(new_game.key())
      current_player.put()
    self.respond(current_player)

  def respond(self, current_player):
    """Respond with HTML."""
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(
        render.game_list(current_player, current_player.itergamekeys()))


class GamePage(webapp2.RequestHandler):
  """View a game."""
  @authenticated_game
  def get(self, current_player, game_obj):
    self.respond(current_player, game_obj)

  @authenticated_game
  def post(self, current_player, game_obj):
    action = self.request.get('action')
    # Join game.
    if action == 'join':
      if not current_player.key() in game_obj.iterplayerkeys():
        try:
          game_obj.add_player(current_player.key(),
                              current_player.get_deck(0))
        except RuntimeError:
          pass
        else:
          game_obj.put()
    # Start game.
    elif action == 'start' and game_obj.has_owner(current_player.key()):
      game_obj.start()
      game_obj.put()
    self.respond(current_player, game_obj)

  def respond(self, current_player, game_obj):
    """Respond with HTML."""
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(render.game(current_player, game_obj))


class ActionPage(webapp2.RequestHandler):
  """Perform a game action."""
  @authenticated
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    query = self.request.get('query')
    results = None
    if query is not None and len(query) > 0:
      results = book.search(query)
    self.response.out.write(render.full_search(user, query, results))


app = webapp2.WSGIApplication([('/game/action', ActionPage),
                               ('/game', GamePage),
                               ('/', GameListPage)],
                              debug=True)
