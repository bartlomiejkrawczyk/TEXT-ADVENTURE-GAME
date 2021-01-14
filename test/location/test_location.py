from location.location import (
    Location,
    DeformedLocationError,
    EmptyLocationError,
    StartingPointNotFoundException,
    InvalidCoordinatesError
)
from location.field import Field
import pytest


def test_create():
    field = Field('Road')
    my_map = [[field]]
    location = Location(my_map, coordinates=(1, 1))
    assert location.field(1, 1) == field
    assert location.field(0, 0).enterable() is False
    assert location.row() == 3
    assert location.column() == 3


def test_create_invalid():
    my_map = [[]]
    with pytest.raises(EmptyLocationError):
        _ = Location(my_map, level=0)
    my_map = []
    with pytest.raises(EmptyLocationError):
        _ = Location(my_map, level=0)
    field = Field('Road')
    my_map = [
        [field, field],
        [field, field, field]
    ]
    with pytest.raises(DeformedLocationError):
        _ = Location(my_map, level=0)
    my_map = [[field]]
    with pytest.raises(StartingPointNotFoundException):
        _ = Location(my_map)
    with pytest.raises(InvalidCoordinatesError):
        _ = Location(my_map, False, coordinates=(1, 1), level=0)


def test_field():
    field1 = Field('Road')
    field2 = Field('Wilderness', danger=-10)
    my_map = [[field1, field2]]
    location = Location(my_map, coordinates=(1, 1))
    assert location.field(1, 1) == field1
    assert location.field(2, 1) == field2


def test_format_map():
    field1 = Field('Road')
    field2 = Field('Road')
    field2.set_seen()
    field3 = Field('Road')
    my_map = [[field1, field2, field3]]
    location = Location(my_map, coordinates=(1, 1))
    assert str(
        location) == " X  X  X  X  X \n X  P  o     X \n X  X  X  X  X \n"


def test_as_dict():
    field = Field('Road')
    my_map = [[field]]
    location = Location(my_map, False, coordinates=(0, 0), level=1)
    assert location.as_dict() == {
        'location': [[field.as_dict()]],
        'coordinates': (0, 0),
        'level': 1
    }


def test_from_dict():
    field = Field('Road')
    my_map = [[field]]
    location = Location(my_map, False, coordinates=(0, 0), level=1)
    new_location = Location.from_dict({
        'location': [[field.as_dict()]],
        'coordinates': (0, 0),
        'level': 1
    })

    assert new_location == location
