from typing import Dict


class Item:
    """
    Item - base class for pickups

    Contains attributes:

    :param name: Name of the item, defaults to 'Item'
    :type name: str, optional

    :param descritpiton: Description of the item, defaults to ''
    :type descritpiton: str, optional
    """

    def __init__(self, name: str = 'Item', descritpiton: str = ''):
        """
        Initialize item

        :param name: Name of the item, defaults to 'Item'
        :type name: str, optional
        :param descritpiton: Description of the item, defaults to ''
        :type descritpiton: str, optional
        :raises ValueError: Indicates that given name was empty
        """
        if not name:
            raise ValueError('Item must have a name')
        self._name = name
        self._description = descritpiton

    def name(self) -> str:
        """
        Get name

        :return: Name of the item
        :rtype: str
        """
        return self._name

    def description(self) -> str:
        """
        Get description

        :return: Item's description
        :rtype: str
        """
        return self._description

    def as_dict(self) -> Dict:
        """
        Get Item as a dictionary

        :return: Dictionary with item's data
        :rtype: Dict
        """
        return {
            'class': self.__class__.__name__,
            'name': self._name,
            'description': self._description
        }

    def print_info(self):
        """
        Print information about item
        """
        desc = (self.description()
                if self.description()
                else 'No description found :(')
        print(f"\nName: {self.name()}\nDescription: {desc}\n")

    @staticmethod
    def item_from_dict(dictionary: Dict) -> 'Item':
        """
        Get new Pickup instance loaded from dictionary

        :param dictionary: Dictionary with item's data
        :type dictionary: Dict
        :return: Item from proper class
        :rtype: Item
        """
        if dictionary:
            item_class = Item.get_item_class(dictionary['class'])
            return item_class.from_dict(dictionary)

    @staticmethod
    def from_dict(dictionary: Dict) -> 'Item':
        """
        Get new Item instance loaded from dictionary

        :param dictionary: Dictionary with item's data
        :type dictionary: Dict
        :return: Item
        :rtype: Item
        """
        if dictionary:
            return Item(
                dictionary.get('name', ''),
                dictionary.get('description', '')
            )

    @staticmethod
    def get_item_class(class_name: str):
        """
        Get class based on class name

        :param class_name: Name of class
        :type class_name: str
        :return: Class with given name
        :rtype: class
        """
        classes = {
            'Item': Item,
            'Weapon': Weapon,
            'Armor': Armor,
            'Key': Key,
            'Potion': Potion,
        }
        return classes.get(class_name, Item)

    def __str__(self) -> str:
        """
        Returns string value of the item - it's name

        :return: Name of the item
        :rtype: str
        """
        return self._name

    def __eq__(self, other):
        """
        :param other: Checked object
        :type other: Any
        :return: Indicates whether self and other are equal
        :rtype: bool
        """
        return isinstance(other, Item) and other.as_dict() == self.as_dict()


class Weapon(Item):
    """
    Weapon

    Inherited attributes:

    :param name: Name of the item, defaults to 'Weapon'
    :type name: str, optional

    :param descritpiton: Description of the item, defaults to ''
    :type descritpiton: str, optional

    Contains attributes:

    :param base_strength: Base strength of the weapon, defaults to 10
    :type base_strength: int

    :param random_strength: Random strength of the weapon, defaults to 10
    :type random_strength: int
    """

    def __init__(
            self,
            name: str = 'Weapon',
            description: str = '',
            base_strength: int = 10,
            random_strength: int = 10):
        super().__init__(name, description)
        """
        Initialize weapon

        :raises ValueError: Indicates that given base strength was negative
        :raises ValueError: Indicates that given random strength was negative
        """
        if base_strength < 0:
            raise ValueError("Weapon's base strength cannot be negative")
        if random_strength < 0:
            raise ValueError("Weapon's random strength cannot be negative")
        self._base_strength = base_strength
        self._random_strength = random_strength

    def base_strength(self) -> int:
        """
        Get base strength

        :return: Value of weapon's base strength
        :rtype: int
        """
        return self._base_strength

    def random_strength(self) -> int:
        """
        Get random strength

        :return: Value of weapon's random strength
        :rtype: int
        """
        return self._random_strength

    def as_dict(self) -> Dict:
        """
        Get weapon as a dictionary

        :return: Dictionary with weapon's data
        :rtype: Dict
        """
        dictionary = super().as_dict()
        dictionary['base_strength'] = self._base_strength
        dictionary['random_strength'] = self._random_strength
        return dictionary

    @staticmethod
    def from_dict(dictionary: Dict) -> 'Weapon':
        """
        Get new Weapon instance loaded from dictionary

        :param dictionary: Dictionary with weapon's data
        :type dictionary: Dict
        :return: Weapon loaded from dictionary
        :rtype: Weapon
        """
        if dictionary:
            return Weapon(
                dictionary.get('name', 'Weapon'),
                dictionary.get('description', ''),
                dictionary.get('base_strength', 10),
                dictionary.get('random_strength', 10)
            )

    def __eq__(self, other) -> bool:
        """
        :param other: Checked object
        :type other: Any
        :return: Indicates whether self and other are equal
        :rtype: bool
        """
        return super().__eq__(other) and isinstance(other, Weapon)


class Armor(Item):
    """
    Armor

    Inherited attributes:

    :param name: Name of the item, defaults to 'Armor'
    :type name: str, optional

    :param descritpiton: Description of the item, defaults to ''
    :type descritpiton: str, optional

    Contains attributes:

    :param defence: Value of armor's defence in percentage, defaults to 0
    :type defence: int
    """

    def __init__(self,
                 name: str = 'Armor',
                 descritpiton: str = '',
                 defence: int = 0):
        super().__init__(name, descritpiton)
        self._defence = defence

    def defence(self) -> int:
        """
        Get defence

        :return: Value of armor's defence in percentage
        :rtype: int
        """
        return self._defence

    def as_dict(self) -> Dict:
        """
        Get armor as a dictionary

        :return: Dictionary with armor's data
        :rtype: Dict
        """
        dictionary = super().as_dict()
        dictionary['defence'] = self._defence
        return dictionary

    @staticmethod
    def from_dict(dictionary: Dict) -> 'Armor':
        """
        Get new Armor instance loaded from dictionary

        :param dictionary: Dictionary with Armor's data
        :type dictionary: Dict
        :return: Armor loaded from dictionary
        :rtype: Armor
        """
        if dictionary:
            return Armor(
                dictionary.get('name', 'Armor'),
                dictionary.get('description', ''),
                dictionary.get('defence', 0)
            )

    def __eq__(self, other):
        """
        :param other: Checked object
        :type other: Any
        :return: Indicates whether self and other are equal
        :rtype: bool
        """
        return super().__eq__(other) and isinstance(other, Armor)


class Key(Item):
    """
    Key

    Inherited attributes:

    :param name: Name of the item, defaults to 'Key'
    :type name: str, optional

    :param descritpiton: Description of the item, defaults to ''
    :type descritpiton: str, optional

    Contains attributes:

    :param location_filename: Location filename from config, defaults to None
    :type location_filename: str

    :param level: Number of level this key opens, defaults to 1
    :type level: int
    """

    def __init__(self,
                 name: str = 'Key',
                 descritpiton: str = '',
                 location_filename: str = None,
                 level: int = 1):
        super().__init__(name, descritpiton)
        self._location_filename = location_filename
        self._level = level

    def location_filename(self) -> str:
        """
        Get location filename

        :return: File name of location from config
        :rtype: str
        """
        return self._location_filename

    def level(self) -> int:
        """
        Get level

        :return: Number of level this key opens
        :rtype: int
        """
        return self._level

    def as_dict(self):
        """
        Get key as a dictionary

        :return: Dictionary with key's data
        :rtype: Dict
        """
        dictionary = super().as_dict()
        dictionary['location_filename'] = self._location_filename
        dictionary['level'] = self._level
        return dictionary

    @staticmethod
    def from_dict(dictionary: Dict) -> 'Key':
        """
        Get new Key instance loaded from dictionary

        :param dictionary: Dictionary with Key's data
        :type dictionary: Dict
        :return: Key loaded from dictionary
        :rtype: Key
        """
        if dictionary:
            return Key(
                dictionary.get('name', 'Key'),
                dictionary.get('description', ''),
                dictionary.get('location_filename', None),
                dictionary.get('level', 1)
            )

    def __eq__(self, other):
        """
        :param other: Checked object
        :type other: Any
        :return: Indicates whether self and other are equal
        :rtype: bool
        """
        return super().__eq__(other) and isinstance(other, Key)


class Potion(Item):
    """
    Potion

    Inherited attributes:

    :param name: Name of the item, defaults to 'Health Potion'
    :type name: str, optional

    :param descritpiton: Description of the item, defaults to ''
    :type descritpiton: str, optional

    Contains attributes:

    :param health: Health this potion regenerates, defaults to 100
    :type health: int
    """

    def __init__(self,
                 name: str = 'Health Potion',
                 descritpiton: str = '',
                 health: int = 100):
        super().__init__(name, descritpiton)
        self._health = health

    def health(self) -> int:
        """
        Get health

        :return: Health this potion regenerates
        :rtype: int
        """
        return self._health

    def as_dict(self):
        """
        Get potion as a dictionary

        :return: Dictionary with potion's data
        :rtype: Dict
        """
        dictionary = super().as_dict()
        dictionary['health'] = self._health
        return dictionary

    @staticmethod
    def from_dict(dictionary: Dict) -> 'Potion':
        """
        Get new Potion instance loaded from dictionary

        :param dictionary: Dictionary with Potion's data
        :type dictionary: Dict
        :return: Potion loaded from dictionary
        :rtype: Potion
        """
        if dictionary:
            return Potion(
                dictionary.get('name', 'Health Potion'),
                dictionary.get('description', ''),
                dictionary.get('health', None)
            )

    def __eq__(self, other):
        """
        :param other: Checked object
        :type other: Any
        :return: Indicates whether self and other are equal
        :rtype: bool
        """
        return super().__eq__(other) and isinstance(other, Potion)
