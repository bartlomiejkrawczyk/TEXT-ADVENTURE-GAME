from utils.format import format_stats
from entities.player import Player

from random import choice, randint
from typing import List, Dict


class EnemyNameError(Exception):
    """
    Indicates that given Enemy's name was empty

    :param Exception: Enemy's name cannot be empty
    :type Exception: Exception
    """
    pass


class Enemy:
    """
    Enemy

    Contains attributes:

    :param name: Name of the enemy, defaults to 'Monster'
    :type name: str, optional

    :param base_health: Base health of the enemy, defaults to 100
    :type base_health: int, optional

    :param health: Current health of the enemy, defaults to 100
    :type health: int, optional

    :param regeneration: Amount of health enemy can regenerate at a time,
                        defaults to 10
    :type regeneration: int, optional

    :param strength: Base value of damage delt to player, defaults to 10
    :type strength: int, optional

    :param random_strength: Random value of damage delt to player,
                            defaults to 10
    :type random_strength: int, optional

    :param shouts: List of texts enemy can shout before fight, defaults to None
    :type shouts: List[str], optional

    :param description: Description of the enemy, defaults to ''
    :type description: str, optional
    """

    def __init__(self,
                 name: str = 'Monster',
                 base_health: int = 100,
                 health: int = 100,
                 regeneration: int = 10,
                 strength: int = 10,
                 random_strength: int = 10,
                 shouts: List[str] = None,
                 description: str = ''
                 ):
        """
        Initialize Enemy

        :param name: Name of the enemy, defaults to 'Monster'
        :type name: str, optional
        :param base_health: Base health of the enemy, defaults to 100
        :type base_health: int, optional
        :param health: Current health of the enemy, defaults to 100
        :type health: int, optional
        :param regeneration: Amount of health enemy can regenerate at a time,
                            defaults to 10
        :type regeneration: int, optional
        :param strength: Base value of damage delt to player, defaults to 10
        :type strength: int, optional
        :param random_strength: Random value of damage delt to player,
                                defaults to 10
        :type random_strength: int, optional
        :param shouts: List of texts enemy can shout before fight,
                        defaults to None
        :type shouts: List[str], optional
        :param description: Description of the enemy, defaults to ''
        :type description: str, optional
        """
        self.set_name(name)
        self.set_base_health(base_health)
        self.set_health(health)
        self.set_regeneration(regeneration)
        self.set_strength(strength)
        self.set_random_strength(random_strength)
        self.set_shouts(shouts),
        self.set_description(description)

    def as_dict(self) -> Dict:
        """
        Get enemy as a dictionary

        :return: Dictionary with enemy's data
        :rtype: Dict
        """
        return {
            'name': self._name,
            'base_health': self._base_health,
            'health': self._health,
            'regeneration': self._regeneration,
            'strength': self._strength,
            'random_strength': self._random_strength,
            'shouts': self._shouts,
            'description': self._description
        }

    @staticmethod
    def from_dict(dictionary: Dict) -> 'Enemy':
        """
        Get new Enemy instance loaded from dictionary

        :param dictionary: Dictionary with enemy's data
        :type dictionary: Dict
        :return: Loaded Enemy
        :rtype: Enemy
        """
        if dictionary:
            return Enemy(
                dictionary.get('name', 'Monster'),
                dictionary.get('base_health', 100),
                dictionary.get('health', 100),
                dictionary.get('regeneration', 10),
                dictionary.get('strength', 10),
                dictionary.get('random_strength', 10),
                dictionary.get('shouts', 10),
                dictionary.get('description', '')
            )

    # Getters and setters

    def name(self) -> str:
        """
        Get enemy's name

        :return: Name of the enemy
        :rtype: str
        """
        return self._name

    def set_name(self, name: str):
        """
        Set enemy's name

        :param name: Name of the enemy
        :type name: str
        :raises EnemyNameError: Indicates that given name is empty
        """
        if not name:
            raise EnemyNameError('Name cannot be empty')
        self._name = name

    def health(self) -> int:
        """
        Get current enemy's health

        :return: Value of enemy's health
        :rtype: int
        """
        return self._health

    def set_health(self, health: int):
        """
        Set player's health

        :param health: Value of enemy's health
        :type health: int
        :raises ValueError: Indicates that given enemy's health was negative
        :raises ValueError: Indicates that given enemy's health was greater
                             than base health
        """
        if health <= 0:
            raise ValueError("Enemy's Health cannot be negative")
        if self._base_health < health:
            raise ValueError('Health cannot be greater than base health')
        self._health = health

    def base_health(self) -> int:
        """
        Get enemy's base value of health

        :return: Base value of enemy's health
        :rtype: int
        """
        return self._base_health

    def set_base_health(self, base_health: int):
        """
        Set enemy's base health value

        :param base_health: Base value of enemy's health
        :type base_health: int
        :raises ValueError: Indicates that given enemy's health was negative
        """
        if base_health <= 0:
            raise ValueError("Enemy's Base Health cannot be negative")
        self._base_health = base_health

    def regeneration(self) -> int:
        """
        Get amount of health enemy can regenerate once a time

        :return: Amount of health
        :rtype: int
        """
        return self._regeneration

    def set_regeneration(self, regeneration: int):
        """
        Set amount of health enemy can regenerate once a time

        :param regeneration: Amount of health
        :type regeneration: int
        :raises ValueError: Indicates that given amount was negative
        """
        if regeneration < 0:
            raise ValueError('Regeneration cannot be negative')
        self._regeneration = regeneration

    def strength(self) -> int:
        """
        Get enemy's base amout of damage delt to player

        :return: Base enemy's strength
        :rtype: int
        """
        return self._strength

    def set_strength(self, strength: int):
        """
        Set enemy's base amout of damage delt to player

        :param strength: Base enemy's strength
        :type strength: int
        :raises ValueError: Indicates that given value was negative
        """
        if strength < 0:
            raise ValueError('Strength cannot be negative')
        self._strength = strength

    def random_strength(self) -> int:
        """
        Get enemy's random amout of damage delt to player

        :return: Random enemy's strength
        :rtype: int
        """
        return self._random_strength

    def set_random_strength(self, random_strength: int):
        """
        Set enemy's random amout of damage delt to player

        :param strength: Random enemy's strength
        :type strength: int
        :raises ValueError: Indicates that given value was negative
        """
        if random_strength < 0:
            raise ValueError('Random strength cannot be negative')
        self._random_strength = random_strength

    def shouts(self) -> List[str]:
        """
        Get list of texts enemy can shout before fight

        :return: List of shouts
        :rtype: List[str]
        """
        return self._shouts

    def set_shouts(self, shouts: List[str]):
        """
        Set list of texts enemy can shout before fight

        :param shouts: List of shouts
        :type shouts: List[str]
        """
        self._shouts = shouts if shouts else ['Die Trash!']

    def description(self) -> str:
        """
        Get enemy's description

        :return: Description
        :rtype: str
        """
        return self._description

    def set_description(self, description: str):
        """
        Set enemy's description

        :param description: Enemy's description
        :type description: str
        """
        self._description = description

    # Custom Methods

    def take_damage(self, damage: int) -> bool:
        """
        Damage enemy by given amount

        :param damage: Amount of damage
        :type damage: int
        :raises ValueError: Indicates that given damage was negative
        :return: Whether enemy is alive
        :rtype: bool
        """
        if damage < 0:
            raise ValueError('Damage cannot be negative')
        self._health -= min(damage, self._health)
        print(f'{self.name()} took {damage} points of damage.')
        return self.is_alive()

    def is_alive(self) -> bool:
        """
        :return: Whether enemy is alive
        :rtype: bool
        """
        return self._health > 0

    def move(self, player: Player) -> bool:
        """
        Decide what to do

        :param player: Player
        :type player: Player

        :return: Whether player is alive after attack
        :rtype: bool
        """
        if self._regeneration == 0 or self._health == self._base_health:
            return self.inflict_damage(player)
        elif (randint(0, 1) or
              (self._regeneration + self._health) > self._base_health):
            return self.inflict_damage(player)
        else:
            return self.regenerate()

    def inflict_damage(self, player: Player) -> bool:
        """
        Attack player

        :param player: Player
        :type player: Player
        :return: Whether player is alive after attack
        :rtype: bool
        """
        damage = self.strength()
        damage += randint(0, self.random_strength())
        print(f'{self.name()} attacked for {damage} points.')
        return player.take_damage(damage)

    def regenerate(self) -> bool:
        """
        Regenerate health

        :return: True - player is alive, no damage delt this time
        :rtype: bool
        """
        self._health = min(
            self._health + self._regeneration, self._base_health)
        print(f'{self.name()} is regenerating.')
        return True

    def shout(self) -> str:
        """
        Generates random fight shouts

        :return: Battle shout
        :rtype: str
        """
        shouts = self._shouts
        return choice(shouts)

    def info(self) -> str:
        """
        Returns basic info about Enemy

        :return: Information about enemy
        :rtype: str
        """
        info = f'Name: {self.name()}\n'
        info += format_stats('Health', self.health(), self.base_health())
        info += format_stats('Strength', self.strength(),
                             self.strength() + self.random_strength())
        return info

    def print_info(self):
        """
        Prints information about enemy
        """
        print(self.info())

    def __str__(self) -> str:
        """
        :return: Basic enemy information
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
        return isinstance(other, Enemy) and self.as_dict() == other.as_dict()
