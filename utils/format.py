from typing import List


def format_stats(name: str, stat: int, base_stat: int):
    """
    Format Statistics that have base value

    :param name: Name of stat
    :type name: str
    :param stat: Current value
    :type stat: int
    :param base_stat: Base value
    :type base_stat: int
    :raises ValueError:

    :return: Formatted statistic
    :rtype: str
    """
    if stat > base_stat:
        raise ValueError('Statistic cannot be greater than base statistic')
    name = f'{name}: '
    output = '['
    value = int(40 * (stat / base_stat))
    output += '=' * value
    output += '-' * (40 - value)
    output += ']\n'
    stats = f'{stat}/{base_stat}'
    output = output[:20] + stats + output[20:]
    output = name + output
    return output


def print_formatted_list(list_: List):
    """
    Print formatted list of items

    :param list_: List of items
    :type list_: List
    """
    print([item.capitalize() for item in list_])


def print_break():
    """
    Print line that separates actions
    """
    print('')
    print('='*100)


def print_list_with_num(list_: List):
    """
    Print enumerated items from list

    :param list_: List of items
    :type list_: List
    """
    for num, item in enumerate(list_):
        print(f"{num+1}. {item}")
