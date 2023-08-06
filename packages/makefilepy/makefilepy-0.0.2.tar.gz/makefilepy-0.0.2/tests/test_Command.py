import unittest

from makefilepy import Command


class TestCommand(unittest.TestCase):
    def test_init(self):
        target = 'up'
        prerequisites = [
            'docker-compose.yml',
        ]
        recipes = [
            'docker-compose up',
        ]
        phony = True
        command = Command(
            target=target,
            prerequisites=prerequisites,
            recipes=recipes,
            phony=phony,
        )
        self.assertEqual(command.target, target)
        self.assertEqual(command.prerequisites, prerequisites)
        self.assertEqual(command.recipes, recipes)
        self.assertEqual(command.phony, phony)

    def test_make_phony_true(self):
        target = 'test'
        command = Command(
            target=target,
            prerequisites=[],
            recipes=['test'],
            phony=True,
        )
        self.assertEqual(command._make_phony(), f'.PHONY: {target}\n')

    def test_make_phony_false(self):
        target = 'test'
        command = Command(
            target=target,
            prerequisites=[],
            recipes=['test'],
            phony=False,
        )
        self.assertEqual(command._make_phony(), '')

    def test_make_target_with_prerequisites(self):
        target = 'up'
        prerequisites = [
            'docker-compose.yml',
        ]
        command = Command(
            target=target,
            prerequisites=prerequisites,
            recipes=['test'],
            phony=False,
        )
        self.assertEqual(command._make_target(), f'{target}: {prerequisites[0]}\n')

    def test_make_target_without_prerequisites(self):
        target = 'up'
        command = Command(
            target=target,
            prerequisites=[],
            recipes=['test'],
            phony=False,
        )
        self.assertEqual(command._make_target(), f'{target}:\n')

    def test_make_recipe(self):
        target = 'up'
        recipes = [
            'docker-compose up',
        ]
        command = Command(
            target=target,
            prerequisites=[],
            recipes=recipes,
            phony=False,
        )
        self.assertEqual(command._make_recipe(), f'\t{recipes[0]}\n')

    def test_build(self):
        target = 'up'
        prerequisites = [
            'docker-compose.yml',
        ]
        recipes = [
            'docker-compose up',
        ]
        phony = True
        command = Command(
            target=target,
            prerequisites=prerequisites,
            recipes=recipes,
            phony=phony,
        )
        result_expected = f'.PHONY: {target}\n' \
                          + f'{target}: {prerequisites[0]}\n' \
                          + f'\t{recipes[0]}\n'
        self.assertEqual(command.build(), result_expected)
