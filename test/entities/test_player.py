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
    assert player.weapon() is None
    assert player.armor() is None
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
        _ = Player(health=100, base_health=1)
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


def test_regenerate():
    player = Player(
        'Knight',
        200, 100
    )
    assert player == Player.from_dict({
        'name': 'Knight',
        'base_health': 200,
        'health': 100,
        'strength': 10,
        'equipment_size': 0,
        'equipment': []
    })
    player.regenerate(10)
    assert player.health() == 110
    player.regenerate(100)
    assert player.health() == 200


def test_use():
    weapon = Weapon()
    armor = Armor()
    key = Key()
    potion = Potion()
    player = Player(
        'Knight',
        200,
        100,
        20,
        equipment_size=100,
        equipment=[key, potion, potion, weapon, armor]
    )
    assert player == Player.from_dict({
        'name': 'Knight',
        'base_health': 200,
        'health': 100,
        'strength': 20,
        'equipment_size': 100,
        'equipment': [
            key.as_dict(),
            potion.as_dict(),
            potion.as_dict(),
            weapon.as_dict(),
            armor.as_dict()
        ]
    })
    player.use(potion)
    assert player.health() == 200
    player.use(potion)
    assert potion in player.equipment()
    assert player.weapon() is None
    player.use(weapon)
    assert player.weapon() == weapon
    assert weapon not in player.equipment()
    assert player.armor() is None
    player.use(armor)
    assert player.armor() == armor
    assert armor not in player.equipment()
    assert key == player.use(key)


def test_search_for_key():
    key = Key()
    player = Player(
        'Knight',
        200,
        100,
        20,
        equipment_size=100,
        equipment=[key]
    )
    assert key == player.search_for_key(1)


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
    assert player.pickup_item(weapon) is False
    assert player.equipment() == [weapon, armor, key, potion]
