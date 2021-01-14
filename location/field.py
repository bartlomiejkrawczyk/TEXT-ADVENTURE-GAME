from entities.enemy import Enemy
from entities.equipment import Item, Key
from entities.player import Player

from utils.player_input import choose_item_from_dict, player_input
from utils.format import print_formatted_list, print_break


from typing import Dict
import functools


class GameOverError(Exception):
    """
    Indicates that the game should end - player won or lost

    :param Exception: Player won or lost
    :type Exception: Exception
    """
    pass


class Field:
    """
    Field

    Contains attributes:

    :param name: Name of the field, defaults to ''
    :type name: str, optional

    :param description: Description of the field, defaults to ''
    :type description: str, optional

    :param danger: Value of regeneration/damage that is delt to player
                    on entrance, defaults to 0
    :type danger: int, optional

    :param enemy: Monster living on this field, defaults to None
    :type enemy: Enemy, optional

    :param item: Pickup from this field, defaults to None
    :type item: Item, optional

    :param enterable: Whether player can enter this field, defaults to True
    :type enterable: bool, optional

    :param seen: Whether player seen this field - whether field
                should be shown on map, defaults to False
    :type seen: bool, optional

    :param go_to: Value of next location player can go from this field,
                defaults to 0
    :type go_to: int, optional
        """

    def __init__(self,
                 name: str = '',
                 desc: str = '',
                 danger: int = 0,
                 enemy: Enemy = None,
                 item: Item = None,
                 enterable: bool = True,
                 seen: bool = False,
                 go_to: int = 0):
        """
        Initialize Field

        :param name: Name of the field, defaults to ''
        :type name: str, optional
        :param desc: Description of the field, defaults to ''
        :type desc: str, optional
        :param danger: Value of regeneration/damage that is delt to player
                        on entrance, defaults to 0
        :type danger: int, optional
        :param enemy: Monster living on this field, defaults to None
        :type enemy: Enemy, optional
        :param item: Pickup from this field, defaults to None
        :type item: Item, optional
        :param enterable: Whether player can enter this field, defaults to True
        :type enterable: bool, optional
        :param seen: Whether player seen this field - whether field
                    should be shown on map, defaults to False
        :type seen: bool, optional
        :param go_to: Value of next location player can go from this field,
                    defaults to 0
        :type go_to: int, optional
        """
        self.set_name(name)
        self.set_description(desc)
        self.set_danger(danger)
        self.set_enemy(enemy)
        self.set_item(item)
        self.set_enterable(enterable)
        self.set_seen(seen)
        self.set_go_to(go_to)

    def as_dict(self) -> Dict:
        """
        Get Field as a dictionary

        :return: Dictionary with Field's data
        :rtype: Dict
        """
        dictionary = {
            'name': self._name,
            'description': self._description,
            'danger': self._danger,
            'enterable': self._enterable,
            'seen': self._seen,
            'go_to': self._go_to
        }
        if self._enemy:
            dictionary['enemy'] = self._enemy.as_dict()
        if self._item:
            dictionary['item'] = self._item.as_dict()
        return dictionary

    @staticmethod
    def from_dict(dictionary: Dict) -> 'Field':
        """
        Get new Field instance loaded from dictionary

        :param dictionary: Dictionary with Field's data
        :type dictionary: Dict
        :return: Loaded Field
        :rtype: Field
        """
        return Field(
            dictionary.get('name', ''),
            dictionary.get('description', ''),
            dictionary.get('danger', 0),
            Enemy.from_dict(dictionary.get('enemy', None)),
            Item.item_from_dict(dictionary.get('item', None)),
            dictionary.get('enterable', True),
            dictionary.get('seen', False),
            dictionary.get('go_to', 0)
        )

    # Getters and Setters

    def name(self) -> str:
        """
        Get field name

        :return: Name of the field
        :rtype: str
        """
        return self._name

    def set_name(self, name: str):
        """
        Set field name

        :param name: Name of the field
        :type name: str
        """
        self._name = name if name else ''

    def description(self) -> str:
        """
        Get field description

        :return: Description of the field
        :rtype: str
        """
        return self._description

    def set_description(self, desc: str):
        """
        Set field description

        :param desc: Description of the field
        :type desc: str
        """
        self._description = desc if desc else ''

    def danger(self) -> int:
        """
        Get Value of regeneration/damage that is delt to player on entrance

        :return: Value of danger
        :rtype: int
        """
        return self._danger

    def set_danger(self, danger: int):
        """
        Set Value of regeneration/damage that is delt to player on entrance

        :param danger: Value of danger
        :type danger: int
        """
        self._danger = danger

    def enemy(self) -> "Enemy":
        """
        Get enemy living on this field

        :return: Monster from this field
        :rtype: Enemy
        """
        return self._enemy

    def set_enemy(self, enemy: "Enemy"):
        """
        Set enemy on this field

        :param enemy: Monster
        :type enemy: Enemy
        """
        self._enemy = enemy

    def item(self) -> "Item":
        """
        Get pickup from this field

        :return: Pickup
        :rtype: Item
        """
        return self._item

    def set_item(self, item: "Item"):
        """
        Set pickup on this field

        :param item: Pickup
        :type item: Item
        """
        self._item = item

    def enterable(self) -> bool:
        """
        Get Whether player can enter this field

        :return: Enterable
        :rtype: bool
        """
        return self._enterable

    def set_enterable(self, enterable: bool):
        """
        Set whether player can enter this field

        :param enterable: If player can enter this field
        :type enterable: bool
        """
        self._enterable = enterable

    def seen(self) -> bool:
        """
        Whether field should be displayed on the map

        :return: Whether player has been on this field
        :rtype: bool
        """
        return self._seen

    def set_seen(self, seen: bool = True):
        """
        Set whether field should be displayed on the map

        :param seen: Whether player has been on this field, defaults to True
        :type seen: bool, optional
        """
        self._seen = seen

    def gate(self) -> bool:
        """
        Method that indicates if player from this field can travel
        to a different location

        :return: If go_to value is different than 0
        :rtype: bool
        """
        return self._go_to != 0

    def go_to(self) -> int:
        """
        Get go to

        :return: Value of next location player can go from this field
        :rtype: int
        """
        return self._go_to

    def set_go_to(self, go_to: int):
        """
        Set go to

        :param go_to: Value of next location player can go from this field
        :type go_to: int
        """
        self._go_to = go_to

    def field_type(self) -> str:
        """
        Get type of the field

        :return: Icon that will indicate fields position on the map
        :rtype: str
        """
        if not self._seen:
            return '   '
        else:
            if not self._enterable:
                return ' X '
            elif self.gate():
                return ' G '
            elif self._enemy:
                return ' M '
            elif self._item:
                return ' i '
            elif self._danger > 0:
                return ' + '
            elif self._danger == 0:
                return ' o '
            else:
                return ' - '

    def open(self, player: Player, game):
        """
        Method available to player if the field is a gate

        Searches player's inventory for matching key
        and if the key is found loads a new location

        Teleports player to a new location

        :param player: Player instance
        :type player: Player
        :param game: Game instance
        :type game: Game
        """
        print('\n')
        if self._go_to == game.level():
            if self._go_to == 1:
                print('No earlier locations available!')
            else:
                print('You are now leaving previous location!')
                game.set_level(game.level()-1)
                game.location().description()
        elif self._go_to <= len(game.locations()):
            print('Location already open - no need for keys ;P')
            game.set_level(game.level()+1)
            game.location().description()
        else:
            key = player.search_for_key(self._go_to)
            if key:
                print('You have opened a new location!')
                print('\n')
                print('You enter a place you do not know.')
                print('I wonder what might be around the corner?')
                game.add_location(key.location_filename())
                game.set_level(game.level()+1)
                game.location().description()
            else:
                print('None of the available keys match!')
        print('\n')

    def open_with_key(self, key: Key, game):
        """
        Method called if player chooses to use a key from his equipment

        Checks if given key is able to open location

        Teleports player to a new location

        :param key: Choosen key
        :type key: Key
        :param game: Game instance
        :type game: Game
        """
        print('\n')
        if self._go_to == game.level():
            if self._go_to == 1:
                print('No earlier locations available!')
            else:
                msg = 'You are now leaving previous location'
                msg += ' - no need for keys ;P'
                print(msg)
                game.set_level(game.level()-1)
                game.location().description()
        elif self._go_to <= len(game.locations()) and self._go_to != 0:
            print('Location already open - no need for keys ;P')
            game.set_level(game.level()+1)
            game.location().description()
        else:
            if key.level() == self._go_to:
                print('You have opened a new location!')
                print('\n')
                print('You enter a place you do not know.')
                print('I wonder what might be around the corner?')
                game.add_location(key.location_filename())
                game.set_level(game.level()+1)
                game.location().description()
            elif self._go_to == 0:
                print('You cannot use keys on a normal field!')
            else:
                print("That key doesn't match ;P")
        print('\n')

    def pickup(self, player: Player):
        """
        Method available to player if on the field is a item

        Tries to add item to players inventory

        :param player: Player instance
        :type player: Player
        """
        if self._item:
            if player.pickup_item(self._item):
                self._item = None

    def drop(self, player: Player):
        """
        Method available to player if on the field aren't any items

        :param player: Player instance
        :type player: Player
        """
        if not self._item:
            item = player.drop_item()
            self._item = item

    def fight(self, player: Player):
        """
        Method called upon player entry if on the field is currently a enemy

        :param player: Player instance
        :type player: Player
        :raises GameOverError: Indicates that player's health is equal to 0
        """
        enemy = self._enemy
        print('\n')
        print("Let's begin the fight!!!")
        print('')
        print(enemy.shout())
        print('\n')
        enemy.print_info()
        print(player)
        print('')
        available_moves = {
            'attack': self.attack,
            'hide': self.hide
        }
        print_formatted_list(available_moves.keys())
        while player_input(
                functools.partial(choose_item_from_dict,
                                  available_moves))(player):
            if not enemy.inflict_damage(player):
                raise GameOverError(
                    f'Game Over :(\n{enemy.name()} has defeated you...')
            print_break()
            enemy.print_info()
            print(player)
            print('')
            print_formatted_list(available_moves.keys())

    def attack(self, player: Player) -> bool:
        """
        Command given by player - he chooses to attack enemy

        :param player: Player instance
        :type player: Player
        :return: Whether enemy is alive after attack
        :rtype: bool
        """

        if player.inflict_damage(self._enemy):
            return True
        else:
            print('You Won. Enemy has died !!!')
            self._enemy = None
            return False

    def hide(self, player: Player) -> bool:
        """
        Command given by player - he chooses to hide from the enemy
        This command ends a fight till another time player enters the field

        :param player: Player instance
        :type player: Player
        :return: False - indicates that fight should end
        :rtype: bool
        """
        print('\n')
        print("You'd better get out of this field")
        return False

    def entrance(self, player: Player):
        """
        Method called when player enters the field

        :param player: Player instance
        :type player: Player
        :raises GameOverError: Field you entered was a final stage
                                of the game - you won
        :raises GameOverError: Indicates that player has no health
        """
        if self._go_to == 'WIN':
            raise GameOverError('\nYou Won!\n\nCongratulations :O')
        if self._danger < 0:
            if not player.take_damage(-self._danger):
                msg = 'Game Over: (\nYou died from hunger.\n'
                msg += 'The field you were standing on had no water '
                raise GameOverError(msg)
        elif self._danger != 0:
            player.regenerate(self._danger)

        if self._enemy:
            self.fight(player)

    def __str__(self) -> str:
        """
        :return: Field description
        :rtype: str
        """
        return self.description()

    def __eq__(self, other) -> bool:
        """
        :param other: Checked object
        :type other: Any
        :return: Indicates whether self and other are equal
        :rtype: bool
        """
        return isinstance(other, Field) and self.as_dict() == other.as_dict()

    def available_methods(self, player: Player, game) -> Dict:
        """
        Get location methods available to player during this round

        :param player: Player instance
        :type player: Player
        :param game: Game instance
        :type game: Game
        :return: Dictionary with methods
        :rtype: Dict
        """
        dictionary = {}
        eq_size = len(player.equipment())
        if self._enemy:
            dictionary['enemy info'] = self._enemy.print_info
        if self._item:
            dictionary['item info'] = self._item.print_info
        if eq_size != 0 and not self._item:
            dictionary['drop item'] = functools.partial(self.drop, player)
        if eq_size != player.equipment_size and self._item and not self._enemy:
            dictionary['pickup item'] = functools.partial(self.pickup, player)
        if self._go_to != 0:
            dictionary['open'] = functools.partial(self.open, player, game)
        return dictionary
