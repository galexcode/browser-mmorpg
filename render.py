import os
import jinja2


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def game_list(player, games):
  template = jinja_environment.get_template('game_list.htm')
  return template.render(player=player, games=games)

def game(player, game):
  template = jinja_environment.get_template('game.htm')
  return template.render(player=player, game=game)
