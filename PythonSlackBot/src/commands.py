import re

commands = {}


class Command:
    def __init__(self, command_pattern, command_name, command_description, flags=0):
        self.command_pattern = command_pattern
        self.command_name = command_name
        self.command_description = command_description
        self.flags = flags

    def __call__(self, function):
        self.function = function
        commands[re.compile(self.command_pattern, self.flags)] = self

    def run(self, *args, **kwargs):
        self.function(*args, **kwargs)


@Command(command_pattern="/test", command_name="Test Command", command_description="Handle File Upload")
def test_command(req):
    print(req)
