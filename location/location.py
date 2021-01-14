from location.field import Field
from entities.player import Player

from typing import List, Dict, Tuple


class EmptyLocationError(Exception):
    """
    Indicates that given List of fields was empty

    :param Exception: List of fields cannot be empty
    :type Exception: Exception
    """
    pass


class DeformedLocationError(Exception):
    """
    Indicates that given List of fields wasn't a rectangle

    :param Exception: List of fields must be a rectangle
    :type Exception: Exception
    """
    pass


class StartingPointNotFoundException(Exception):
    """
    Indicates that given Location didn't have a starting point

    :param Exception: Location must have a starting point
    :type Exception: Exception
    """
    pass


class InvalidCoordinatesError(Exception):
    """
    Indicates that given coordinates are out of range

    :param Exception: Invalid coordinates
    :type Exception: Exception
    """
    pass


class Location:
    """
    Location

    Contains attributes:

    :param location: Matrix of fields
    :type location: List[List[Field]]

    :param coordinates: Player's coordinates, defaults to None
    :type coordinates: Tuple[int, int], optional

    :param level: Location level, defaults to 1
    :type level: int, optional
    """

    def __init__(self,
                 location: List[List[Field]],
                 set_boarders: bool = True,
                 coordinates: Tuple[int, int] = None,
                 level: int = 1):
        """
        Initialize Location

        :param location: Matrix of fields
        :type location: List[List[Field]]
        :param set_boarders: Whether location needs boarders, defaults to True
        :type set_boarders: bool, optional
        :param coordinates: Player's coordinates, defaults to None
        :type coordinates: Tuple[int, int], optional
        :param level: Location level, defaults to 1
        :type level: int, optional
        """
        if set_boarders:
            self.set_location(location)
        else:
            self.set_location_already_with_boarders(location)
        self.set_level(level)
        if coordinates:
            self.set_coordinates(coordinates)
        else:
            self.set_starting_coordinates(level)

    def as_dict(self) -> Dict:
        """
        Get Location as a dictionary

        :return: Dictionary with location's data
        :rtype: Dict
        """
        return {
            'location': [[field.as_dict() for field in row]
                         for row in self._location],
            'coordinates': self._coordinates,
            'level': self._level
        }

    @staticmethod
    def from_dict(dictionary: Dict) -> 'Location':
        """
        Get new Location instance loaded from dictionary

        :param dictionary: Dictionary with Location's data
        :type dictionary: Dict
        :return: Loaded Location
        :rtype: Location
        """
        return Location(
            [[Field().from_dict(field) for field in row]
             for row in dictionary['location']],
            False,
            dictionary.get('coordinates', None),
            dictionary.get('level', 1))

    # Getters and Setters

    def location(self) -> List[List[Field]]:
        """
        Get location

        :return: Matrix of fields
        :rtype: List[List[Field]]
        """
        return self._location

    def set_location(self, location: List[List[Field]]):
        """
        Set location and add boarders around it

        :param location: Matrix of fields
        :type location: List[List[Field]]
        """
        self._location = self.create_boarder(location)

    def set_location_already_with_boarders(self, location: List[List[Field]]):
        """
        Set location without adding boarders

        :param location: Matrix of fields
        :type location: List[List[Field]]
        """
        self._location = location if location else [[]]

    def level(self) -> int:
        """
        Get location level

        :return: Level of the location
        :rtype: int
        """
        return self._level

    def set_level(self, level: int):
        """
        Set location level

        :param level: Level of the location
        :type level: int
        """
        self._level = level

    def coordinates(self) -> Tuple[int, int]:
        """
        Get coordinates

        :return: (x, y)
        :rtype: Tuple[int, int]
        """
        self._coordinates

    def set_coordinates(self, coordinates: Tuple[int, int]):
        """
        Set coordinates

        :param coordinates: (x, y)
        :type coordinates: Tuple[int, int]
        :raises InvalidCoordinatesError: Indicates that coordinates are
                                        out of range
        """
        x, y = coordinates
        if not (0 <= x < self.row() and 0 <= y < self.column()):
            raise InvalidCoordinatesError()
        self._coordinates = (x, y)

    def set_starting_coordinates(self, level: int):
        """
        Set starting coordinates

        :param level: Location level
        :type level: int
        """
        self.set_coordinates(self.get_starting_coordinates(level))

    def get_starting_coordinates(self, level: int) -> Tuple[int, int]:
        """
        Get field coordinates with go_to parameter equal to location level

        :param level: Location level
        :type level: int
        :raises StartingPointNotFoundException: Indicates that given Location
                                                didn't have a starting point
        :return: Starting coordinates - (x, y)
        :rtype: Tuple[int, int]
        """
        for y, row in enumerate(self._location):
            for x, field in enumerate(row):
                if field.go_to() == level:
                    return x, y
        raise StartingPointNotFoundException()

    def get_boarder_field(self) -> Field:
        """
        Get boarder field

        :return: Boarder field
        :rtype: Field
        """
        return Field(
            'Boarder',
            'No one is able to go through me!',
            enterable=False,
            seen=True
        )

    def boarder_row(self, row_len: int) -> List[Field]:
        """
        Get boarder row with given length

        :param row_len: Length of the row
        :type row_len: int
        :return: List of boarder fields
        :rtype: List[Field]
        """
        row = []
        for _ in range(row_len + 2):
            row.append(self.get_boarder_field())
        return row

    def create_boarder(self, location: List[List[Field]]) -> List[List[Field]]:
        """
        Generate boarder around location fields

        :param location: Matrix of fields without boarder
        :type location: List[List[Field]]
        :raises EmptyLocationError: Indicates that given List of fields
                                    was empty
        :raises DeformedLocationError: Indicates that given List of fields
                                        wasn't a rectangle
        :return: [description]
        :rtype: List[List[Field]]
        """
        column_len = len(location)
        if column_len != 0:
            row_len = len(location[0])
        if column_len == 0 or row_len == 0:
            raise EmptyLocationError('Given Location was empty')

        for row in location:
            if len(row) != row_len:
                raise DeformedLocationError("Given Matrix wasn't a rectangle")

        new_location = [self.boarder_row(row_len)]

        for y, row in enumerate(location):
            new_location.append([])
            new_location[y+1].append(self.get_boarder_field())
            for f in row:
                new_location[y+1].append(f)
            new_location[y+1].append(self.get_boarder_field())

        new_location.append(self.boarder_row(row_len))
        return new_location

    def field(self, x: int, y: int) -> Field:
        """
        Get fields with given coordinates

        :param x: Coordinate - x
        :type x: int
        :param y: Coordinate - y
        :type y: int
        :return: Field with given coordinates
        :rtype: Field
        """
        return self._location[y][x]

    def current_field(self) -> Field:
        """
        Get field player is standing on

        :return: Field player is standing on
        :rtype: Field
        """
        x, y = self._coordinates
        return self._location[y][x]

    def column(self) -> int:
        """
        Get fields column count

        :return: Coulum count
        :rtype: int
        """
        return len(self._location)

    def row(self) -> int:
        """
        Get fields row count

        :return: Row count
        :rtype: int
        """
        if len(self._location) != 0:
            return len(self._location[0])
        else:
            return 0

    def format_map(self) -> str:
        """
        Format map based on fields

        :return: Formatted map
        :rtype: str
        """
        p_x, p_y = self._coordinates
        output = ''
        for y, row in enumerate(self._location):
            for x, field in enumerate(row):
                if p_x != x or p_y != y:
                    output += field.field_type()
                else:
                    output += ' P '
            output += '\n'
        return output

    def is_enterable(self, south: int = 0, east: int = 0) -> bool:
        """
        Whether location distant from player is enterable

        :param south: Distance south, defaults to 0
        :type south: int, optional
        :param east: Distance east, defaults to 0
        :type east: int, optional
        :return: Whether field is enterable
        :rtype: bool
        """
        x, y = self._coordinates
        x = x+south
        y = y+east
        return self.field(x, y).enterable()

    def go(self, player: Player, south: int = 0, east: int = 0):
        """
        Method that allows player to move

        :param player: Player
        :type player: Player
        :param south: Distance south, defaults to 0
        :type south: int, optional
        :param east: Distance east, defaults to 0
        :type east: int, optional
        """
        x, y = self._coordinates
        x = x + east
        y = y + south
        if self.field(x, y).enterable():
            self._coordinates = (x, y)
            self.current_field().set_seen()
            self.description()
            self.current_field().entrance(player)

    def go_north(self, player: Player):
        """
        Moves player north

        :param player: Player
        :type player: Player
        """
        self.go(player, south=-1)

    def go_south(self, player: Player):
        """
        Moves player south

        :param player: Player
        :type player: Player
        """
        self.go(player, south=1)

    def go_east(self, player: Player):
        """
        Moves player east

        :param player: Player
        :type player: Player
        """
        self.go(player, east=1)

    def go_west(self, player: Player):
        """
        Moves player west

        :param player: Player
        :type player: Player
        """
        self.go(player, east=-1)

    def wait(self, player: Player):
        """
        Calls current field entry function

        :param player: Player
        :type player: Player
        """
        self.current_field().set_seen()
        self.current_field().entrance(player)

    def description(self, _=None):
        """
        Get location description

        :param _: None, defaults to None
        :type _: Any, optional
        """
        self.print_map()
        print('')
        if self._coordinates:
            x, y = self._coordinates
        else:
            self.set_starting_coordinates(self._level)
            x, y = self._coordinates
        print(f"NORTH: {self.field(x, y-1).name()}")
        print(f"SOUTH: {self.field(x, y+1).name()}")
        print(f"EAST: {self.field(x+1, y).name()}")
        print(f"WEST: {self.field(x-1, y).name()}")
        print('')
        field = self.current_field()
        print(f"CURRENT: {field.name()}")
        print(self.current_field().description())
        if field.enemy():
            print('')
            print(f'ENEMY: {field.enemy().name()}')
            print(field.enemy().description())
        if field.item():
            print('')
            print(f'ITEM: {field.item().name()}')
            print(field.item().description())

    def __str__(self) -> str:
        """
        :return: Map of the location
        :rtype: str
        """
        return self.format_map()

    def print_map(self, _=None):
        """
        Print map of the location

        :param _: None, defaults to None
        :type _: Any, optional
        """
        print('\n')
        print(self)

    def __eq__(self, other) -> bool:
        """
        :param other: Checked object
        :type other: Any
        :return: Indicates whether self and other are equal
        :rtype: bool
        """
        return (isinstance(other, Location) and
                self.as_dict() == other.as_dict())

    def available_methods(self) -> Dict:
        """
        Get location methods available to player during this round

        :return: Dictionary with methods
        :rtype: Dict
        """
        x, y = self._coordinates
        dictionary = {'map': self.print_map, 'location info': self.description}
        if self.field(x, y - 1).enterable():
            dictionary['go north'] = self.go_north
        if self.field(x, y + 1).enterable():
            dictionary['go south'] = self.go_south
        if self.field(x + 1, y).enterable():
            dictionary['go east'] = self.go_east
        if self.field(x - 1, y).enterable():
            dictionary['go west'] = self.go_west
        dictionary['wait'] = self.wait
        return dictionary
