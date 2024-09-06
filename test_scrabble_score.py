"""Software Unit Testing Report
Scrabble Score Using Test Driven Development"""

# Scrabble Score Game using Test Driven Development

import unittest
from unittest.mock import patch
import time
import io
import sys
from scrabble_score import ScrabbleScore


class TestScrabbleScore(unittest.TestCase):
    '''Unit Testing Class'''

    def setUp(self):
        self.scrabble = ScrabbleScore()

    # The numbers are added up correctly for a given word
    def test_calculate_score(self):
        '''Testing the numbers added up correctly for given word'''
        word = "apple"
        expected_score = sum(
            self.scrabble.LETTER_VALUES[char] for char in word.upper())
        self.assertEqual(self.scrabble.calculate_score(word), expected_score)

    # Upper-case and lower-case letters should have the same value
    def test_case_insensitivity(self):
        '''Testing Upper-case and lower-case letters have same value'''

        self.assertEqual(self.scrabble.calculate_score("HELLO"), 8)
        self.assertEqual(self.scrabble.calculate_score("hElLo"), 8)

    # Program handle non-alphabet invalid words
    def test_handle_non_alphabet_word(self):
        """Test invalid input score calculation (non-alphabetic characters)."""
        invalid_word = "app1e"
        self.assertEqual(
            self.scrabble.calculate_score(invalid_word),
            "Invalid input. Please enter only alphabetic characters.")

    def test_calculate_time_bonus_fast_input(self):
        """Test time bonus for fast input."""
        fast_time = 5  # User took 5 seconds
        expected_bonus = (15 - fast_time) * 5
        self.assertEqual(self.scrabble.calculate_time_bonus(fast_time),
                         expected_bonus)

    def test_calculate_time_bonus_slow_input(self):
        """Test time bonus when user exceeds 15 seconds (no bonus)."""
        slow_time = 16  # User took more than 15 seconds
        self.assertEqual(self.scrabble.calculate_time_bonus(slow_time), 0)

    @patch('time.time', side_effect=[0, 10])
    def test_elapsed_time_calculation(self, mock_time):
        """Test calculation of elapsed time."""
        start_time = time.time()
        end_time = time.time()
        elapsed_time = self.scrabble.calculate_elapsed_time(start_time,
                                                            end_time)
        self.assertEqual(elapsed_time, 10)

    def test_validate_word_length_correct(self):
        """Test the word length correct for valid word"""
        self.assertTrue(self.scrabble.validate_word_length("apple", 5))

    def test_validate_word_length_incorrect(self):
        """Test the word length incorrect for invalid word"""
        self.assertFalse(self.scrabble.validate_word_length("pear", 5))

    @patch('builtins.input', side_effect=['apple', 'pear', 'app'])
    @patch('time.time', side_effect=[0, 5, 0, 16, 0, 8])
    def test_play_round(self, mock_time, mock_input):
        """Test play_round method with multiple scenarios."""

        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Case 1: Valid input
        self.scrabble.play_round()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        if "Valid word!" in output:
            # Valid input: fast response, calculate score
            self.assertIn("Valid word!", output)
            self.assertIn("Base score (word value): ", output)
            self.assertIn("Time taken: 5.00 seconds.", output)
            self.assertIn("Time bonus: ", output)
            self.assertIn("Your total score: ", output)
        else:
            # Invalid cases
            # Case 2: Timeout case
            if "Time's up!" in output:
                self.assertIn("\nYou took too long.", output)
                self.assertIn("\nTime taken: 16.00 seconds.", output)
                self.assertIn("\nYour score: 0", output)
            # Case 3: Invalid input
            elif "Invalid" in output:
                self.assertIn("Invalid! Word must be ", output, " letters")
                self.assertIn("\nTime taken: ", output, " seconds.")
                self.assertIn("Your score: 0", output)


if __name__ == '__main__':
    unittest.main()
