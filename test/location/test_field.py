from location.field import Field
from entities.enemy import Enemy
from entities.equipment import Item, Key, Potion, Weapon, Armor


def test_create():
    field = Field()
    assert field.name() == ''
    assert field.description() == ''
    assert str(field) == ''
    assert field.danger() == 0
    assert field.enemy() == None
    assert field.item() == None
    assert field.enterable() == True
    assert field.seen() == False
    field.set_seen(True)
    assert field.seen() == True
    assert field.gate() == False
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
    assert field.enterable() == True
    assert field.seen() == True
    assert field.gate() == True
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
