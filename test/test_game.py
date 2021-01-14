from game import Game
from entities.player import Player
from location.location import Location
from location.field import Field


def test_correct():
    assert 2 + 2 == 4


def test_create():
    game = Game(player=Player())
    assert game.player() == Player()
    assert game.game() == 'Dungeons and Dragons'
    assert len(game.locations()) == 1
    assert game.level() == 1

    player = Player('Knight')
    location1 = Location([[Field(go_to=1), Field(go_to=2)]], level=1)
    location2 = Location([[Field(go_to=2)]], level=2)
    game = Game('test', player, [location1, location2], 2)
    assert game.player() == player
    assert game.game() == 'test'
    assert len(game.locations()) == 2
    assert game.level() == 2
    assert game.location() == location2


def test_as_dict():
    player = Player('Knight')
    location1 = Location([[Field(go_to=1), Field(go_to=2)]], level=1)
    location2 = Location([[Field(go_to=2)]], level=2)
    game = Game('test', player, [location1, location2], 2)
    dictionary = game.as_dict()
    assert dictionary['game'] == 'test'
    assert dictionary['level'] == 2
    assert dictionary['player'] == player.as_dict()
    assert dictionary['locations'] == [
        location1.as_dict(), location2.as_dict()]


def test_from_dict():
    player = Player('Knight')
    location1 = Location([[Field(go_to=1), Field(go_to=2)]], level=1)
    location2 = Location([[Field(go_to=2)]], level=2)
    game = Game('test', player, [location1, location2], 2)
    dictionary = game.as_dict()
    game_from_dict = Game.from_dict({
        'game': 'test',
        'player': (player.as_dict()),
        'locations': [location1.as_dict(), location2.as_dict()],
        'level': 2
    })
    assert game == game_from_dict
    assert dictionary == game_from_dict.as_dict()


def test_save(monkeypatch):
    player = Player('Knight')
    location1 = Location([[Field(go_to=1), Field(go_to=2)]], level=1)
    location2 = Location([[Field(go_to=2)]], level=2)
    game = Game('test', player, [location1, location2], 2)

    def return_str(a):
        return 'save_1'
    monkeypatch.setattr('game.player_input', return_str)
    game.save()


def test_load():
    player = Player('Knight')
    location1 = Location([[Field(go_to=1), Field(go_to=2)]], level=1)
    location2 = Location([[Field(go_to=2)]], level=2)
    game = Game('test', player, [location1, location2], 2)
    loaded_game = Game.load('test', 'save_1')

    assert loaded_game == game
