import os
import jinja2


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def game_list(player, games):
  template = jinja_environment.get_template('game_list.htm')
  return template.render(player=player, games=games)

def game(player, game):
  template_file = 'join.htm' if game.is_joinable() else 'game.htm'
  template = jinja_environment.get_template(template_file)
  return template.render(player=player, game=game)
