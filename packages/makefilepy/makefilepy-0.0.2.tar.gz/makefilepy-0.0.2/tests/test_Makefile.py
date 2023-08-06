import unittest

from makefilepy import Command, Makefile, Variable
import pytest


class TestMakefile(unittest.TestCase):
    def test_init(self):
        makefile = Makefile()
        self.assertEqual(makefile.variables, [])
        self.assertEqual(makefile.commands, [])

    @pytest.fixture(autouse=True)
    def initdir(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

    def test_build_with_variables_and_commands(self):
        makefile_path = 'makefile.txt'
        variable = Variable(
            key='test',
            value='test',
        )
        command = Command(
            target='up',
            prerequisites=[
                'docker-compose.yml',
            ],
            recipes=[
                'docker-compose up',
            ],
            phony=True,
        )
        makefile = Makefile()
        makefile.variables.append(variable)
        makefile.commands.append(command)
        makefile.build(filename=makefile_path)

        result_expected = '# Variables\n' \
                          + 'test=test\n\n' \
                          + '# Commands\n' \
                          + '.PHONY: up\n' \
                          + 'up: docker-compose.yml\n' \
                          + '\tdocker-compose up\n'

        with open(makefile_path) as makefile_file:
            self.assertEqual(makefile_file.read(), result_expected)

    def test_build_without_variables_and_commands(self):
        makefile_path = 'makefile.txt'
        makefile = Makefile()
        makefile.build(filename=makefile_path)

        result_expected = ''

        with open(makefile_path) as makefile_file:
            self.assertEqual(makefile_file.read(), result_expected)

    def test_build_with_variables_and_without_commands(self):
        makefile_path = 'makefile.txt'
        variable = Variable(
            key='test',
            value='test',
        )
        makefile = Makefile()
        makefile.variables.append(variable)
        makefile.build(filename=makefile_path)

        result_expected = '# Variables\n' \
                          + 'test=test\n'

        with open(makefile_path) as makefile_file:
            self.assertEqual(makefile_file.read(), result_expected)

    def test_build_without_variables_and_with_commands(self):
        makefile_path = 'makefile.txt'
        command = Command(
            target='up',
            prerequisites=[
                'docker-compose.yml',
            ],
            recipes=[
                'docker-compose up',
            ],
            phony=True,
        )
        makefile = Makefile()
        makefile.commands.append(command)
        makefile.build(filename=makefile_path)

        result_expected = '# Commands\n' \
                          + '.PHONY: up\n' \
                          + 'up: docker-compose.yml\n' \
                          + '\tdocker-compose up\n'

        with open(makefile_path) as makefile_file:
            self.assertEqual(makefile_file.read(), result_expected)
