# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) 2015-2022 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

"""
Functions suite to prompt for various user inputs in shell.
"""

# BUG: ctrl-c is not taken into account by click...

import click


def getval_yes_no(message, default=True):
    """
    Prompt user with <message>, wait for a Y/N answer.

    Return:
        bool: True for yes, Y, Yes, YES etc.
              False for no, N, No, NO etc.
    """
    return click.confirm(message, default=default)


def getval_name(message, default=None):
    """
    Prompt user for a 'valid name', ie containing letters and "_" chars only.
    ie can be a valid python identifier.
    Return:
        str: user value if correct.
    """

    ans = click.prompt(message, type=click.STRING, default=default)
    while not ans.isidentifier():
        ans = click.prompt(message, type=click.STRING, default=default)

    return ans


def getval_int_range(message, minimum, maximum, default=None):
    """
    Prompt user for an int number in interval [minimum, maximum]

    Return:
        int: user value if correct.
    """
    return click.prompt(message, type=click.IntRange(minimum, maximum), default=default)


def getval_idx_list(choices_list, message=None):
    """
    Return index and string chosen by user in list of N strings.
    Selection is done by index in [1..N].

    Parameters:
        choices_list: list of str
        message: str
    Returns: tuple(int, str)
        Selected index and string.
    """
    print("")
    if message is None:
        message = "Enter number of item:"

    choice_count = len(choices_list)
    for (index, value) in enumerate(choices_list):
        print(f"{index+1} - {value}")

    ans = click.prompt(message, default=1, type=click.IntRange(1, choice_count))

    return (ans, choices_list[ans - 1])


def getval_char_list(char_choice_list_or_dict, message=None):
    """
    Return character and string chosen by user in list of strings.
    Selection is done by letter provided by user.

    Parameters:
        char_choice_list_or_dict: list of tuples (str, str)  or dict
        message: str
    Returns: tuple(str, str)
        * str: single char selected by user
        * str: string selected by user
    """
    print("")

    choices_dict = dict()
    char_list = list()

    if isinstance(char_choice_list_or_dict, list):
        for (char, text) in char_choice_list_or_dict:
            choices_dict[char] = text
            char_list.append(char)
            print(f"{char} - {text}")
    else:
        for (char, text) in char_choice_list_or_dict.items():
            choices_dict[char] = text
            char_list.append(char)
            print(f"{char} - {text}")

    choice_list = click.Choice(char_list)
    ans = click.prompt(message, default=None, type=choice_list, show_choices=True)

    return (ans, choices_dict[ans])
