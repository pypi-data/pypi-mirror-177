import unittest

from makefilepy import Variable


class TestVariable(unittest.TestCase):
    def test_init(self):
        key = 'test'
        value = 'testValue'
        variable = Variable(key=key, value=value)
        self.assertEqual(variable.key, key)
        self.assertEqual(variable.value, value)

    def test_build(self):
        key = 'test'
        value = 'testValue'
        variable = Variable(key=key, value=value)
        self.assertEqual(variable.build(), f'{key}={value}')

    def test_reference(self):
        key = 'test'
        value = 'testValue'
        variable = Variable(key=key, value=value)
        self.assertEqual(variable.reference(), '${test}')
