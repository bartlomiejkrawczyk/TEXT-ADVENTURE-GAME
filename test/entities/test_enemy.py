from entities.enemy import Enemy, EnemyNameError
from entities.player import Player

import pytest


def test_create():
    enemy = Enemy()
    assert enemy.name() == 'Monster'
    assert enemy.base_health() == 100
    assert enemy.health() == 100
    assert enemy.regeneration() == 10
    assert enemy.strength() == 10
    assert enemy.random_strength() == 10
    assert enemy.shouts() == ['Die Trash!']
    assert enemy.description() == ''

    enemy = Enemy('Goblin', 200, 200, 20, 20, 20, ['Die!'], 'Description')
    assert enemy.name() == 'Goblin'
    assert enemy.base_health() == 200
    assert enemy.health() == 200
    assert enemy.regeneration() == 20
    assert enemy.strength() == 20
    assert enemy.random_strength() == 20
    assert enemy.shouts() == ['Die!']
    assert enemy.description() == 'Description'


def test_create_invalid():
    with pytest.raises(EnemyNameError):
        _ = Enemy('')
    with pytest.raises(ValueError):
        _ = Enemy(health=-1)
    with pytest.raises(ValueError):
        _ = Enemy(base_health=-1)
    with pytest.raises(ValueError):
        _ = Enemy(base_health=1, health=2)
    with pytest.raises(ValueError):
        _ = Enemy(regeneration=-1)
    with pytest.raises(ValueError):
        _ = Enemy(strength=-1)
    with pytest.raises(ValueError):
        _ = Enemy(random_strength=-1)


def test_as_dict():
    enemy = Enemy('Goblin', 200, 200, 20, 20, 20, ['Die!'], 'Description')
    assert enemy.as_dict() == {
        'name': 'Goblin',
        'base_health': 200,
        'health': 200,
        'regeneration': 20,
        'strength': 20,
        'random_strength': 20,
        'shouts': ['Die!'],
        'description': 'Description'
    }


def test_from_dict():
    enemy = Enemy('Goblin', 200, 200, 20, 20, 20, ['Die!'], 'Description')
    assert enemy == Enemy.from_dict({
        'name': 'Goblin',
        'base_health': 200,
        'health': 200,
        'regeneration': 20,
        'strength': 20,
        'random_strength': 20,
        'shouts': ['Die!'],
        'description': 'Description'
    })


def test_take_damage():
    enemy = Enemy(health=1000, base_health=1000)
    assert enemy.health() == 1000
    enemy.take_damage(100)
    assert enemy.health() == 900
    enemy.take_damage(1000)
    assert enemy.health() == 0


def test_is_alive():
    enemy = Enemy(health=100)
    assert enemy.health() == 100
    assert enemy.is_alive()
    enemy.take_damage(100)
    assert enemy.health() == 0
    assert enemy.is_alive() == False


def test_inflict_damage(monkeypatch):
    player = Player(health=1000, base_health=1000)
    enemy = Enemy(strength=10, random_strength=0)
    assert player.health() == 1000
    enemy.inflict_damage(player)
    assert player.health() == 990

    def return_ten(s, e):
        return 10
    monkeypatch.setattr('entities.enemy.randint', return_ten)

    enemy = Enemy(strength=0, random_strength=10)
    enemy.inflict_damage(player)
    assert player.health() == 980


def test_regenerate():
    enemy = Enemy(health=10, base_health=100, regeneration=10)
    assert enemy.health() == 10
    enemy.regenerate()
    assert enemy.health() == 20


def test_move(monkeypatch):
    player = Player(health=100, base_health=100)
    enemy = Enemy(base_health=1000, health=1000,
                  strength=10, random_strength=0, regeneration=10)
    assert player.health() == 100
    enemy.move(player)
    assert player.health() == 90

    def return_zero(s, e):
        return 0
    monkeypatch.setattr('entities.enemy.randint', return_zero)
    enemy.take_damage(10)
    assert enemy.health() == 990
    enemy.move(player)
    assert enemy.health() == 1000
    enemy.take_damage(1)
    assert enemy.health() == 999
    enemy.move(player)
    assert enemy.health() == 999


def test_info():
    enemy = Enemy()
    info = """Name: Monster
Health: [===================100/100=====================]
Strength: [===================10/20=--------------------]
"""
    assert str(enemy) == info
    assert enemy.info() == info
