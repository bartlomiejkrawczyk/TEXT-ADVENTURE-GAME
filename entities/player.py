from entities.equipment import Item
from entities.equipment import (
    Weapon,
    Armor,
    Potion,
    Key
)
from utils.format import format_stats, print_list_with_num
from utils.player_input import choose_num_from_list, player_input

from typing import List, Dict
from random import randint
import functools


class PlayerNameError(Exception):
    """
    Indicates that given Player's name was empty

    :param Exception: Player's name cannot be empty
    :type Exception: Exception
    """

    def __init__(self):
        super().__init__("Player's name cannot be empty")


class EquipmentSizeError(ValueError):
    """
    Indicates that equipment size is too small to add another item

    :param ValueError: Equipment size is too small
    :type ValueError: ValueError
    """
    pass


class Player:
    """
        Player

        Contains attributes:

        :param name: Player's name, defaults to 'Nameless'
        :type name: str, optional

        :param base_health: Base health of the player, defaults to 100
        :type base_health: int, optional

        :param health: Current health of the player, defaults to 100
        :type health: int, optional

        :param strength: Strength of the base attack, defaults to 10
        :type strength: int, optional

        :param weapon: Weapon - item that can increase player's
                        attack damage, defaults to None
        :type weapon: Weapon, optional

        :param armor: Armor - item that reduces taken damage, defaults to None
        :type armor: Armor, optional

        :param equipment_size: Number of slots int the equipment, defaults to 0
        :type equipment_size: int, optional

        :param equipment: List of items - current player's equipment,
                            defaults to None
        :type equipment: List[Item], optional
        """

    def __init__(self,
                 name: str = 'Nameless',
                 base_health: int = 100,
                 health: int = 100,
                 strength: int = 10,
                 weapon: Weapon = None,
                 armor: Armor = None,
                 equipment_size: int = 0,
                 equipment: List[Item] = None
                 ):
        """
        Initialize Player

        :param name: Player's name, defaults to 'Nameless'
        :type name: str, optional
        :param base_health: Base health of the player, defaults to 100
        :type base_health: int, optional
        :param health: Current health of the player, defaults to 100
        :type health: int, optional
        :param strength: Strength of the base attack, defaults to 10
        :type strength: int, optional
        :param weapon: Weapon - item that can increase player's attack damage,
                        defaults to None
        :type weapon: Weapon, optional
        :param armor: Armor - item that reduces taken damage, defaults to None
        :type armor: Armor, optional
        :param equipment_size: Number of slots int the equipment, defaults to 0
        :type equipment_size: int, optional
        :param equipment: List of items - current player's equipment,
                            defaults to None
        :type equipment: List[Item], optional
        """
        self.set_name(name)
        self.set_base_health(base_health)
        self.set_health(health)
        self.set_strength(strength)
        self.set_weapon(weapon)
        self.set_armor(armor)
        self.set_equipment_size(equipment_size)
        self.set_equipment(equipment)

    def as_dict(self) -> Dict:
        """
        Get Player as a dictionary

        :return: Dictionary with player's data
        :rtype: Dict
        """
        dictionary = {
            'name': self._name,
            'base_health': self._base_health,
            'health': self._health,
            'strength': self._strength,
            'equipment_size': self._equipment_size,
            'equipment': [item.as_dict() for item in self._equipment]
        }
        if self._weapon:
            dictionary['weapon'] = self._weapon.as_dict()
        if self._armor:
            dictionary['armor'] = self._armor.as_dict()
        return dictionary

    @staticmethod
    def from_dict(dictionary) -> "Player":
        """
        Get new Player instance loaded from dictionary

        :param dictionary: Dictionary with Player's data
        :type dictionary: Dict
        :return: Loaded Player
        :rtype: Player
        """
        return Player(
            dictionary.get('name', 'Nameless'),
            dictionary.get('base_health', 100),
            dictionary.get('health', 100),
            dictionary.get('strength', 10),
            Weapon.from_dict(dictionary.get('weapon', None)),
            Armor.from_dict(dictionary.get('armor', None)),
            dictionary.get('equipment_size', 0),
            [Item.item_from_dict(item)
             for item in dictionary.get('equipment', [])]
        )

    # Getters and Setters

    def name(self) -> str:
        """
        Get player's name

        :return: Name of the player
        :rtype: str
        """
        return self._name

    def set_name(self, name: str):
        """
        Set player's name

        :param name: Name of the player
        :type name: str
        :raises PlayerNameError: Indicates that given name is empty
        """
        if not name:
            raise PlayerNameError()
        self._name = name

    def health(self) -> int:
        """
        Get current player's health

        :return: Value of player's health
        :rtype: int
        """
        return self._health

    def set_health(self, health: int):
        """
        Set player's health

        :param health: Value of player's health
        :type health: int
        :raises ValueError: Indicates that given player's health was negative
        """
        if health <= 0:
            raise ValueError("Player's Health cannot be negative")
        if health > self._base_health:
            raise ValueError(
                "Player's Health cannot be greater than base health")
        self._health = health

    def base_health(self) -> int:
        """
        Get player's base value of health

        :return: Base value of player's health
        :rtype: int
        """
        return self._base_health

    def set_base_health(self, base_health: int):
        """
        Set player's base health value

        :param base_health: Base value of player's health
        :type base_health: int
        :raises ValueError: Indicates that given player's health was negative
        """
        if base_health <= 0:
            raise ValueError("Player's Base Health cannot be negative")
        self._base_health = base_health

    def strength(self) -> int:
        """
        Get base value of player's strength

        :return: Value of player's strength
        :rtype: int
        """
        return self._strength

    def set_strength(self, strength: int):
        """
        Set base value of player's strength

        :param strength: Value of player's strength
        :type strength: int
        :raises ValueError: Indicates that given strength was negative
        """
        if strength < 0:
            raise ValueError('Strength must be positive')
        self._strength = strength

    def weapon(self) -> Weapon:
        """
        Get weapon - item that can increase player's attack damage

        :return: Player's equipped weapon
        :rtype: Weapon
        """
        return self._weapon

    def set_weapon(self, weapon: Weapon):
        """
        Set weapon - item that can increase player's attack damage

        :param weapon: Player's weapon to equip
        :type weapon: Weapon
        """
        self._weapon = weapon

    def armor(self) -> Armor:
        """
        Get armor - item that can decrease player's damage taken

        :return: Player's equipped armor
        :rtype: Armor
        """
        return self._armor

    def set_armor(self, armor: Armor):
        """
        Set armor - item that can decrease player's damage taken

        :param armor: Player's armor to equip
        :type armor: Armor
        """
        self._armor = armor

    def equipment(self) -> List[Item]:
        """
        Get list of player's items from the equipment

        :return: List of player's items
        :rtype: List[Item]
        """
        return self._equipment

    def set_equipment(self, equipment: List[Item]):
        """
        Get list of player's items as the equipment

        :param equipment: List of items
        :type equipment: List[Item]
        :raises ValueError: Indicates that in given list was found item
                            that didn't inherited from Item class
        :raises EquipmentSizeError: Indicates that player couldn't
                            handle such heavy equipment
        """
        if not equipment:
            equipment = []
        for item in equipment:
            if not isinstance(item, Item):
                raise ValueError('Equipment must contain only Items')
        if len(equipment) > self._equipment_size:
            raise EquipmentSizeError('Equipment size is too small')
        self._equipment = equipment

    def equipment_size(self) -> int:
        """
        Get max size of the player's equipment

        :return: Max equipment size
        :rtype: int
        """
        return self._equipment_size

    def set_equipment_size(self, size: int):
        """
        Set max size of the player's equipment

        :param size: Max equipment size
        :type size: int
        :raises ValueError: Indicates that given size was negative
        """
        if size < 0:
            raise ValueError('Equipment size must be positive')
        self._equipment_size = size

    # Custom Methods

    def take_damage(self, amount: int) -> bool:
        """
        Method that decreases player's health by given amount

        :param amount: Amount of the damage given
        :type amount: int
        :raises ValueError: Indicates that given amount was negative
        :return: If player is alive
        :rtype: bool
        """
        if amount < 0:
            raise ValueError('Damage cannot be negative')
        if self.armor():
            amount = amount * (100 - self.armor().defence()) / 100
            amount = int(amount)
        self._health -= min(amount, self._health)
        if amount != 0:
            print('')
            print(f'Ouch! You took {amount} points of damage!')
        return self._health != 0

    def inflict_damage(self, enemy) -> bool:
        """
        Method that calculates the amount of damage player will
        deal to given enemy

        :param enemy: Enemy from field player is standing on
        :type enemy: Enemy
        :return: Whether enemy is alive
        :rtype: bool
        """
        damage = self._strength
        if self._weapon:
            damage += self._weapon.base_strength()
            damage += randint(0, self._weapon.random_strength())
        return enemy.take_damage(damage)

    def regenerate(self, amount: int):
        """
        Method that regenerates player's healt by a given amount
        Player's health cannot be greater than base health

        :param amount: Amount of health to regenerate
        :type amount: int
        :raises ValueError: Indicates that given amount was negative
        """
        if amount < 0:
            raise ValueError('Amount cannot be negative')
        if self._health != self._base_health:
            print('')
            print(f'Player has regenerated {amount} points of health.')
        self._health = min(self._health + amount, self._base_health)

    def use(self, item: Item):
        """
        Method that decides based on given item which action should be called

        :param item: Item from equipment
        :type item: Item
        :return: Called method result
        :rtype: Key, bool
        """
        if isinstance(item, Weapon):
            return self.equip_weapon(item)
        elif isinstance(item, Armor):
            return self.equip_armor(item)
        elif isinstance(item, Key):
            return self.open(item)
        elif isinstance(item, Potion):
            return self.drink(item)

    def drink(self, potion: Potion) -> bool:
        """
        Regenerate player's health and remove potion from inventory

        :param potion: Potion of health
        :type potion: Potion
        :return: Whether potion was drunk or not
        :rtype: bool
        """
        if self._health != self._base_health:
            self._health = min(potion.health() + self._health,
                               self._base_health)
            print('You have drank your potion!')
            self._equipment.remove(potion)
            return True
        print('You have full health already!')
        return False

    def equip_weapon(self, weapon: Weapon):
        """
        Set player's weapon as a choosen one, old weapon hide to inventory

        :param weapon: Weapon to equip
        :type weapon: Weapon
        """
        current_weapon = self._weapon
        num = self._equipment.index(weapon)
        self.set_weapon(weapon)
        print('You have equipped a weapon.')
        if current_weapon:
            self._equipment[num] = current_weapon
            print('Your old weapon is now in the inventory.')
        else:
            self._equipment.remove(weapon)

    def equip_armor(self, armor: Armor):
        """
        Set player's armor as a choosen one, old armor hide to inventory

        :param armor: Armor to equip
        :type armor: Armor
        """
        current_armor = self._armor
        num = self._equipment.index(armor)
        self.set_armor(armor)
        print('You have equipped armor.')
        if current_armor:
            self._equipment[num] = current_armor
            print('Your old armor is now in the inventory.')
        else:
            self._equipment.remove(armor)

    def open(self, key: Key) -> Key:
        """
        Return key used to open location on this field

        :param key: Key to new location
        :type key: Key
        :return: Key to new location
        :rtype: Key
        """
        return key

    def print_equipment(self):
        """
        Print player's equipment as enumerated list
        """
        print('\n')
        print_list_with_num(self._equipment)

    def pickup_item(self, item: Item) -> bool:
        """
        Add item to inventory

        :param item: Item to add
        :type item: Item
        :return: Whether item was added or inventory was full
        :rtype: bool
        """
        if len(self._equipment) != self._equipment_size:
            self._equipment.append(item)
            print('Item added to equipment!')
            return True
        print("You don't have enough space in the inventory!")
        return False

    def drop_item(self) -> Item:
        """
        Remove item chosen by user from inventory

        :return: Item player has chosen
        :rtype: Item
        """
        print('Choose item you want to drop?')
        self.print_equipment()
        print('Enter number:')
        item = player_input(functools.partial(
            choose_num_from_list, self._equipment))
        self._equipment.remove(item)
        return item

    def prepare_use(self):
        """
        Ask player which item he wants to use
        """
        print('Choose item you want to use?')
        self.print_equipment()
        print('Enter number:')
        item = player_input(functools.partial(
            choose_num_from_list, self._equipment))
        return self.use(item)

    def search_for_key(self, level: int) -> Key:
        """
        Search inventory for approptiate key

        :param level: Level of the location key opens
        :type level: int
        :return: Key that opens given level
        :rtype: Key
        """
        for item in self._equipment:
            if isinstance(item, Key) and item.level() == level:
                return item

    def available_methods(self) -> Dict:
        """
        Get player methods available to player during this round

        :return: Dictionary with methods
        :rtype: Dict
        """
        dictionary = {}
        if len(self._equipment):
            dictionary['use item'] = self.prepare_use
        dictionary['player info'] = self.print_info
        if len(self._equipment) != 0:
            dictionary['equipment info'] = self.print_equipment
        return dictionary

    def print_info(self):
        """
        Print information about player
        """
        print('\n')
        print(self)
        print('\n')

    def info(self) -> str:
        """
        :return: Player information
        :rtype: str
        """
        info = 'PLAYER\n'
        info += f'Name: {self.name()}\n'
        info += format_stats('Health', self.health(), self.base_health())
        strength = self.strength()
        base_strength = strength
        if self._weapon:
            strength += self._weapon.base_strength()
            base_strength = strength + self._weapon.random_strength()
        info += format_stats('Strength', strength, base_strength)
        if self._armor:
            info += format_stats('Armor', self._armor.defence(), 100)

        return info

    def __str__(self) -> str:
        """
        :return: Basic player information
        :rtype: str
        """
        return self.info()

    def __eq__(self, other):
        """
        :param other: Checked object
        :type other: Any
        :return: Indicates whether self and other are equal
        :rtype: bool
        """
        return isinstance(other, Player) and self.as_dict() == other.as_dict()
