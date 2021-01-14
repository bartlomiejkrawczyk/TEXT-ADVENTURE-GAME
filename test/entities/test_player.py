from entities.player import (
    Player,
    PlayerNameError,
    EquipmentSizeError
)
from entities.enemy import Enemy
from entities.equipment import (
    Item,
    Weapon,
    Armor,
    Key,
    Potion
)


import pytest


def test_create():
    player = Player()
    assert player.name() == 'Nameless'
    assert player.health() == 100
    assert player.base_health() == 100
    assert player.strength() == 10
    assert player.weapon() == None
    assert player.armor() == None
    assert player.equipment_size() == 0
    assert player.equipment() == []
    weapon = Weapon()
    armor = Armor()
    key = Key()
    potion = Potion()
    player = Player(
        'Knight',
        200, 200, 20, Weapon(), armor, 2, [key, potion]
    )
    assert player.name() == 'Knight'
    assert player.health() == 200
    assert player.base_health() == 200
    assert player.strength() == 20
    assert player.weapon() == weapon
    assert player.armor() == armor
    assert player.equipment_size() == 2
    assert player.equipment() == [key, potion]


def test_create_invalid():
    with pytest.raises(PlayerNameError):
        _ = Player('')
    with pytest.raises(ValueError):
        _ = Player(health=0)
    with pytest.raises(ValueError):
        _ = Player(base_health=0)
    with pytest.raises(EquipmentSizeError):
        _ = Player(equipment_size=0, equipment=[Item()])


def test_info():
    name = 'Bartłomiej Krawczyk'
    player = Player(name)
    assert str(player) == """PLAYER
Name: Bartłomiej Krawczyk
Health: [===================100/100=====================]
Strength: [===================10/10=====================]
"""


def test_as_dict():
    weapon = Weapon()
    armor = Armor()
    key = Key()
    potion = Potion()
    player = Player(
        'Knight',
        200, 200, 20, Weapon(), armor, 2, [key, potion]
    )
    assert player.as_dict() == {
        'name': 'Knight',
        'base_health': 200,
        'health': 200,
        'strength': 20,
        'weapon': weapon.as_dict(),
        'armor': armor.as_dict(),
        'equipment_size': 2,
        'equipment': [key.as_dict(), potion.as_dict()]
    }


def test_from_dict():
    weapon = Weapon()
    armor = Armor()
    key = Key()
    potion = Potion()
    player = Player(
        'Knight',
        200, 200, 20, Weapon(), armor, 2, [key, potion]
    )
    assert player == Player.from_dict({
        'name': 'Knight',
        'base_health': 200,
        'health': 200,
        'strength': 20,
        'weapon': weapon.as_dict(),
        'armor': armor.as_dict(),
        'equipment_size': 2,
        'equipment': [key.as_dict(), potion.as_dict()]
    })


def test_take_damage():
    armor = Armor(defence=50)
    player = Player(health=200, base_health=200, armor=armor)
    assert player.health() == 200
    player.take_damage(100)
    assert player.health() == 150
    armor._defence = 90
    player.take_damage(100)
    assert player.health() == 140


def test_inflict_damage(monkeypatch):
    weapon = Weapon(base_strength=10, random_strength=0)
    player = Player(strength=10, weapon=weapon)
    enemy = Enemy(base_health=1000, health=1000)
    assert enemy.health() == 1000
    player.inflict_damage(enemy)
    assert enemy.health() == 980

    weapon._random_strength = 10

    def return_random_strength(s, e):
        return e
    monkeypatch.setattr('entities.player.randint', return_random_strength)

    player.inflict_damage(enemy)
    assert enemy.health() == 950


def test_pickup_item():
    weapon = Weapon()
    armor = Armor()
    key = Key()
    potion = Potion()
    player = Player(equipment_size=4, equipment=[])
    assert player.pickup_item(weapon)
    assert player.pickup_item(armor)
    assert player.pickup_item(key)
    assert player.pickup_item(potion)
    assert player.pickup_item(weapon) == False
    assert player.equipment() == [weapon, armor, key, potion]
