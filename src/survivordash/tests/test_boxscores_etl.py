import unittest
from survivordash import boxscores_etl
import pandas as pd

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

    def test_rename_challenge_data_columns(self):
        columns = ["Contestant", "MPF*  ChA", "MPF", "ChA"]
        expected_columns = ["name", "ch_score", "ch_finish_avg", "ch_appear"]

        df = pd.DataFrame([], columns=columns)
        boxscores_etl._rename_challenge_data_columns(df)
        print(df.columns.tolist())
        print(expected_columns)
        self.assertListEqual(df.columns.tolist(), expected_columns)



