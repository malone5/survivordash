import unittest
from survivordash import utility

class TestUtility(unittest.TestCase):

    def test_player_name_hash(self):
        name = 'Bob Smith'
        expected = 'c54fb'
        self.assertEqual(utility._hash_player_name(name), expected)
