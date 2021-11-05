import unittest
from survivordash import wiki_etl

class TestWikiETL(unittest.TestCase):


    def test_season_map(self):
        season_title = 'Survivor: Marquesas'
        expected = 4
        self.assertEqual(wiki_etl._get_season_number(season_title), expected)

    def test_name_between_quotes(self):
        name = 'Bob "Wild Card" Smith'
        expected = 'Wild Card'
        self.assertEqual(wiki_etl._name_between_quotes(name), expected)

        name = 'Kassandra" Kass" McQuillen'
        expected = 'Kass'
        self.assertEqual(wiki_etl._name_between_quotes(name), expected)


    def test_name_between_quotes_null(self):
        name = 'Bob Smith'
        expected = None
        self.assertEqual(wiki_etl._name_between_quotes(name), expected)
    

    def test_name_outside_quotes(self):
        # standard case
        name = 'Bob "Wild Card" Smith'
        expected = 'Bob Smith'
        self.assertEqual(wiki_etl._name_outside_quotes(name), expected)

        # poor spacing case
        name = 'Kassandra" Kass" McQuillen'
        expected = 'Kassandra McQuillen'
        self.assertEqual(wiki_etl._name_outside_quotes(name), expected)
