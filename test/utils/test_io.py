from utils.io import (
    load_configuration_from_json,
    load_configuration_from_string,
    load_location_from_configuration,
    write_save_as_json,
    load_save_from_json
)

from entities.player import Player
from entities.enemy import Enemy
from entities.equipment import Key
from location.location import (
    Location,
    DeformedLocationError,
    EmptyLocationError,
    StartingPointNotFoundException
)
from location.field import Field
from game import Game

import pytest


def test_load_configuration_from_json():
    player = load_configuration_from_json(
        'test', 'player', Player)
    assert player.as_dict() == {
        "name": "Nameless",
        "base_health": 100,
        "health": 100,
        "strength": 10,
        "equipment_size": 0,
        "equipment": []
    }


def test_load_configuration_from_string():
    string = load_configuration_from_string('test', 'introduction')
    assert string == """Intro
...
test"""


def test_load_location_from_configuration():
    location = load_location_from_configuration('test', 'correct', 1)
    assert str(
        location) == " X  X  X  X \n X  P     X \n X        X \n X  X  X  X \n"


def test_load_location_from_configuration_invalid():
    with pytest.raises(FileNotFoundError):
        _ = load_location_from_configuration('test', 'not_found', 1)
    with pytest.raises(DeformedLocationError):
        _ = load_location_from_configuration('test', 'deformed', 1)
    with pytest.raises(EmptyLocationError):
        _ = load_location_from_configuration('test', 'empty', 1)
    with pytest.raises(StartingPointNotFoundException):
        _ = load_location_from_configuration('test', 'without_start', 1)


def test_write_save_as_json():
    enemy = Enemy()
    item = Key()
    player = Player()
    field = Field('Road', 'Simple Road', -10, enemy, item, True, True, 1)
    location1 = Location([[field, Field(go_to=2)]], level=1)
    location2 = Location([[Field(go_to=2)]], level=2)
    game = Game('test', player, [location1, location2], 2)
    write_save_as_json('test', 'test', game)


def test_load_save_from_json():
    enemy = Enemy()
    item = Key()
    player = Player()
    field = Field('Road', 'Simple Road', -10, enemy, item, True, True, 1)
    location1 = Location([[field, Field(go_to=2)]], level=1)
    location2 = Location([[Field(go_to=2)]], level=2)
    game = Game('test', player, [location1, location2], 2)
    loaded_game = load_save_from_json('test', 'test', Game)
    assert game == loaded_game
