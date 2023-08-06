class Makefile:
    def __init__(self):
        self.variables = []
        self.commands = []

    def build(self, filename: str = 'Makefile'):
        variables_str = self._build_variables()
        commands_str = self._build_commands()
        makefile_str = variables_str

        if variables_str and commands_str:
            makefile_str += '\n'

        if commands_str:
            makefile_str += commands_str

        with open(filename, 'w') as makefile_file:
            makefile_file.write(makefile_str)

    def _build_variables(self) -> str:
        if len(self.variables) == 0:
            return ''

        return '# Variables\n' \
               + ''.join([variable.build() + '\n' for variable in self.variables])

    def _build_commands(self) -> str:
        if len(self.commands) == 0:
            return ''

        commands_str = '# Commands\n' \
                       + ''.join([command.build() + '\n' for command in self.commands])

        # Remove last '\n'
        return commands_str[:-1]
