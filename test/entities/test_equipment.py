from entities.equipment import Item, Weapon, Armor, Key, Potion


def test_create_item():
    item = Item('Item')
    assert item.name() == 'Item'
    assert item.description() == ''
    item = Item('Item', 'Description')
    assert item.name() == 'Item'
    assert item.description() == 'Description'


def test_create_weapon():
    weapon = Weapon()
    assert weapon.name() == 'Weapon'
    assert weapon.description() == ''
    assert weapon.base_strength() == 10
    assert weapon.random_strength() == 10
    weapon = Weapon('Sword', 'Description', 20, 20)
    assert weapon.name() == 'Sword'
    assert weapon.description() == 'Description'
    assert weapon.base_strength() == 20
    assert weapon.random_strength() == 20


def test_create_armor():
    armor = Armor()
    assert armor.name() == 'Armor'
    assert armor.description() == ''
    assert armor.defence() == 0
    armor = Armor('Angel Armor', 'Description', 20)
    assert armor.name() == 'Angel Armor'
    assert armor.description() == 'Description'
    assert armor.defence() == 20


def test_create_key():
    key = Key()
    assert key.name() == 'Key'
    assert key.description() == ''
    assert key.location_filename() is None
    assert key.level() == 1
    key = Key('Red Key', 'Description', 'lvl2', 2)
    assert key.name() == 'Red Key'
    assert key.description() == 'Description'
    assert key.location_filename() == 'lvl2'
    assert key.level() == 2


def test_create_potion():
    potion = Potion()
    assert potion.name() == 'Health Potion'
    assert potion.description() == ''
    assert potion.health() == 100
    potion = Potion('Potion', 'Description', 99)
    assert potion.name() == 'Potion'
    assert potion.description() == 'Description'
    assert potion.health() == 99


def test_item_as_dict():
    item = Item('Item')
    assert item.as_dict() == {
        'class': 'Item',
        'name': 'Item',
        'description': ''
    }


def test_weapon_as_dict():
    weapon = Weapon()
    assert weapon.as_dict() == {
        'class': 'Weapon',
        'name': 'Weapon',
        'description': '',
        'base_strength': 10,
        'random_strength': 10
    }


def test_armor_as_dict():
    armor = Armor()
    assert armor.as_dict() == {
        'class': 'Armor',
        'name': 'Armor',
        'description': '',
        'defence': 0
    }


def test_key_as_dict():
    key = Key()
    assert key.as_dict() == {
        'class': 'Key',
        'name': 'Key',
        'description': '',
        'location_filename': None,
        'level': 1
    }


def test_potion_as_dict():
    potion = Potion()
    assert potion.as_dict() == {
        'class': 'Potion',
        'name': 'Health Potion',
        'description': '',
        'health': 100
    }


def test_item_from_dict():
    item = Item('Item')
    assert item == Item.from_dict({
        'name': 'Item',
        'description': ''
    })


def test_weapon_from_dict():
    weapon = Weapon('Sword', 'Description', 20, 20)
    assert weapon == Weapon.from_dict({
        'name': 'Sword',
        'description': 'Description',
        'base_strength': 20,
        'random_strength': 20
    })


def test_armor_from_dict():
    armor = Armor('Angel Armor', 'Description', 20)
    assert armor == Armor.from_dict({
        'name': 'Angel Armor',
        'description': 'Description',
        'defence': 20
    })


def test_key_from_dict():
    key = Key('Red Key', 'Description', 'lvl2', 2)
    assert key == Key.from_dict({
        'name': 'Red Key',
        'description': 'Description',
        'location_filename': 'lvl2',
        'level': 2
    })


def test_potion_from_dict():
    potion = Potion('Potion', 'Description', 99)
    assert potion == Potion.from_dict({
        'name': 'Potion',
        'description': 'Description',
        'health': 99
    })
