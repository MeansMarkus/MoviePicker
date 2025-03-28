import unittest
from unittest.mock import patch, mock_open
import pandas as pd
import builtins
import movieFilter

class TestMovieFilter(unittest.TestCase):

    @patch('builtins.input', return_value='Action')
    @patch('pandas.read_csv')
    def test_genre_retrieval(self, mock_read_csv, mock_input):
        # Mock DataFrame
        mock_data = {
            'Title': ['Movie A', 'Movie B'],
            'Genre': ['Action,Comedy', 'Drama,Romance']
        }
        mock_df = pd.DataFrame(mock_data)
        mock_read_csv.return_value = mock_df

        with patch('random.randint', side_effect=[0, 1, 0]):
            # Capture the printed output
            with patch('builtins.print') as mock_print:
                movieFilter.print_random_movie_by_genre()

                # Check that a genre containing the user input was printed
                found_genre_output = any(
                    'Action' in str(call.args[0]) for call in mock_print.call_args_list
                )
                self.assertTrue(found_genre_output)

if __name__ == '__main__':
    unittest.main()
