"""Software Unit Testing Report
Scrabble Score Game Using Test Driven Development"""


import time
import random
import threading


class ScrabbleScore:
    '''Scrabble Score Class'''

    # Letter values
    LETTER_VALUES = {
        **dict.fromkeys('AEIOULNRST', 1),
        **dict.fromkeys('DG', 2),
        **dict.fromkeys('BCMP', 3),
        **dict.fromkeys('FHVWY', 4),
        **dict.fromkeys('K', 5),
        **dict.fromkeys('JX', 8),
        **dict.fromkeys('QZ', 10)
    }

    # A sample dictionary of valid words
    VALID_WORDS_DICTIONARY = {"apple", "pear", "orange", "banana", "grape"}

    def __init__(self):
        self.total_score = 0
        self.time_up = False
        self.rounds_played = 0

    def calculate_score(self, word):
        '''Calculate Score function'''

        if not word.isalpha():
            return "Invalid input. Please enter only alphabetic characters."

        word = word.upper()
        score = sum(self.LETTER_VALUES.get(char, 0) for char in word)
        return score

    def validate_word_in_dictionary(self, word):
        """Ensure the word is a valid word from the dictionary."""
        return word.lower() in self.VALID_WORDS_DICTIONARY

    # A 15-second timer is shown.
    # The user is asked to input a word of a certain length.
    # The number of alphabets required in the word is randomly generated.
    # The program will check to ensure that
    # the correct word length is entered before generating the score.
    # The score will be higher if less time is used to enter valid word.

    def generate_random_word_length(self):
        """Generate a random word length between 3 and 10."""
        return random.randint(3, 10)

    def calculate_elapsed_time(self, start, end):
        """Calculate the time taken between start and end."""
        return end - start

    def validate_word_length(self, word, required_length):
        """Check if the word has the required number of characters."""
        return len(word) == required_length

    def calculate_time_bonus(self, time_taken):
        '''Calculate the score based on time'''
        max_time = 15  # Max time to complete the task is 15 seconds

        if time_taken > max_time:
            return 0  # No bonus if time exceeds 15 seconds

        return (max_time - time_taken) * 5  # Bonus decreases as time increases

    def countdown_timer(self):
        """Countdown timer that runs in a separate thread."""
        self.time_up = False
        for _ in range(15, 0, -1):
            if self.time_up:
                return  # Stop the timer if the game is over
            time.sleep(1)
        self.time_up = True  # Signal that time is up
        # Notify the user when time is up
        print("\nTime's up!Please Enter to proceed")

    def get_user_input(self):
        """Get user input, but stop the timer if input is given."""
        user_word = ""
        try:
            user_word = input("\nYour word: ")
        except Exception:
            pass
        return user_word.strip().lower()

    def play_round(self):
        '''Play round function'''
        total_score = 0
        # Generate a random required word length,
        # But right now fixing to 5 for writing test cases
        required_length = 5  # self.generate_random_word_length()
        print(f"Please enter valid word with exactly {required_length} length")

        # Start the timer in a separate thread
        timer_thread = threading.Thread(target=self.countdown_timer)
        timer_thread.start()

        start_time = time.time()

        user_word = ""
        valid_word = False

        while not self.time_up:  # Loop until time runs out
            # Get the user input in a way that respects the timer
            user_word = self.get_user_input()

            # Check if the word is valid in dictionary
            if not self.validate_word_in_dictionary(user_word):
                print("Invalid! Please enter a a valid dictionary word.")
            elif len(user_word) != required_length:
                print(f"Invalid! Word must be {required_length} letters")
            else:
                valid_word = True
                self.time_up = True
                break  # If valid, break out of the loop

        # Join the timer thread
        timer_thread.join()

        # If time has expired, print the time-up message
        elapsed_time = time.time() - start_time
        if self.time_up and elapsed_time > 15:
            print("\nTime's up! You took too long.")
            print(f"Time taken: {elapsed_time:.2f} seconds.")
            print("Your score: 0")
            return 0  # End the game if time is up

        # If a valid word was entered in time,
        # calculate the score and time bonus
        if valid_word:
            print("Valid word!")
            base_score = self.calculate_score(user_word)
            time_bonus = self.calculate_time_bonus(elapsed_time)
            total_score = base_score + time_bonus
            print(f"Base score (word value): {base_score}")
            print(f"Time taken: {elapsed_time:.2f} seconds.")
            print(f"Time bonus: {time_bonus}")
            print(f"Your total score: {total_score}")

        return total_score

    def play_game(self):
        """Main game with 10 rounds or until the player quits."""
        self.total_score = 0
        self.rounds_played = 0

        while self.rounds_played < 10:
            print(f"\nRound {self.rounds_played + 1} of 10")

            round_score = self.play_round()

            self.total_score += round_score
            self.rounds_played += 1

            if self.rounds_played == 10:
                print("\nYou've completed 10 rounds!")
                print(f"Your total score is {self.total_score}.")
                break


def main():
    '''main method'''
    scrabble = ScrabbleScore()
    scrabble.play_game()


if __name__ == "__main__":
    main()
