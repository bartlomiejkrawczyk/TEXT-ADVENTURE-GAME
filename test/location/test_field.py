from location.field import Field, GameOverError
from entities.enemy import Enemy
from entities.player import Player
from entities.equipment import Item, Key

import pytest


def test_create():
    field = Field()
    assert field.name() == ''
    assert field.description() == ''
    assert str(field) == ''
    assert field.danger() == 0
    assert field.enemy() is None
    assert field.item() is None
    assert field.enterable() is True
    assert field.seen() is False
    field.set_seen(True)
    assert field.seen() is True
    assert field.gate() is False
    assert field.go_to() == 0

    enemy = Enemy()
    item = Key()
    field = Field('Road', 'Simple Road', -10, enemy, item, True, True, 1)
    assert field.name() == 'Road'
    assert field.description() == 'Simple Road'
    assert str(field) == 'Simple Road'
    assert field.danger() == -10
    assert field.enemy() == enemy
    assert field.item() == item
    assert field.enterable() is True
    assert field.seen() is True
    assert field.gate() is True
    assert field.go_to() == 1


def test_field_type():
    field = Field(
        'Boarder',
        'No one is able to go through me',
        enterable=False,
        seen=True)
    assert field.field_type() == ' X '
    field = Field('Road', 'Simple Road')
    assert field.field_type() == '   '
    field = Field('Road', 'Simple Road', go_to=1)
    field.set_seen(True)
    assert field.field_type() == ' G '
    field = Field('Road', 'Simple Road', enemy=Enemy())
    field.set_seen(True)
    assert field.field_type() == ' M '
    field = Field('Road', 'Simple Road', item=Item())
    field.set_seen(True)
    assert field.field_type() == ' i '
    field = Field('Road', 'Simple Road')
    field.set_seen(True)
    assert field.field_type() == ' o '
    field = Field('Road', 'Simple Road', danger=1)
    field.set_seen(True)
    assert field.field_type() == ' + '
    field = Field('Road', 'Simple Road', danger=-1)
    field.set_seen(True)
    assert field.field_type() == ' - '


def test_as_dict():
    enemy = Enemy()
    item = Key()
    field = Field('Road', 'Simple Road', -10, enemy, item, True, True, 0)
    assert field.as_dict() == {
        'name': 'Road',
        'description': 'Simple Road',
        'danger': -10,
        'enemy': enemy.as_dict(),
        'item': item.as_dict(),
        'enterable': True,
        'seen': True,
        'go_to': 0
    }


def test_from_dict():
    enemy = Enemy()
    item = Key()
    field = Field('Road', 'Simple Road', -10, enemy, item, True, True, False)
    dictionary = {
        'name': 'Road',
        'description': 'Simple Road',
        'danger': -10,
        'enemy': enemy.as_dict(),
        'item': item.as_dict(),
        'enterable': True,
        'seen': True,
        'go_to': 0
    }
    new_field = Field.from_dict(dictionary)
    assert new_field == field


def test_pickup():
    item = Item()
    field = Field(item=item)
    assert field.item() == item
    player = Player(equipment_size=10)
    field.pickup(player)
    assert field.item() is None


def test_attack():
    enemy = Enemy(health=10)
    field = Field(enemy=enemy)
    player = Player(strength=9)
    assert field.enemy() == enemy
    assert field.attack(player)
    assert field.attack(player) is False
    assert field.enemy() is None


def test_entrance():
    field = Field(danger=-10, go_to='WIN')
    player = Player(health=100)
    with pytest.raises(GameOverError):
        field.entrance(player)
    field.set_go_to(0)
    assert player.health() == 100
    field.entrance(player)
    assert player.health() == 90
