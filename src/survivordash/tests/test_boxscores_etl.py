import unittest
from survivordash import boxscores_etl

class TestBoxscoresETL(unittest.TestCase):

    def test_fname_last_inital(self):
        input_name = 'Bob Smithy'
        name = boxscores_etl._extract_first_name_last_initial(input_name)
        target = 'Bob Smith'
        self.assertTrue(name, target)

        input_name = 'Sue'
        name = boxscores_etl._extract_first_name_last_initial(input_name)
        target = 'Susan Hawk'
        self.assertTrue(name, target)


