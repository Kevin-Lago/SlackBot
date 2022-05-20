import re

commands = {}


def add_command(command_name, function):
    commands[re.compile(command_name)] = function