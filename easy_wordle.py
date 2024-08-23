import random
from words import words
from wordle import check_word
import display_utility


def filter_word_list(words, clues):
    """
    This function takes in a list of words along with the clues and returns a new word list containing those words
    in the input word list which could be the secret word.
    :param words:
    :param clues:
    :return: a list of words
    """
    # Creating a filter words list to store all the filtered words that will be obtained from words.py file
    filter_words = []
    for name in words:
        clue_match = True  # setting the variable clue_match to True assuming that the current word matches the clues
        for word, clue in clues:
            every_word = name.upper()
            clue_checker = check_word(every_word, word)  # calling check_word function
            clue_checker_str = []
            for i in clue_checker:
                clue_checker_str.append(str(i))
            # convert the list of letters to a list of strings
            if clue != clue_checker_str:  # checking if the clues doesn't match with the expected number of clues
                clue_match = False  # setting it to false indicating that the word does not match with the clues
                break
        if clue_match:
            filter_words.append(name)  # appending the word if the clue_matches (if it remains True)
    return filter_words


if __name__ == '__main__':
    secret_word = "peris" #random.choice(words) # selecting a random word from words list
    secret_word = secret_word.upper()
    print()
    clues = []
    guess_list = []
    guess_count = 0
    while True:
        guess = input("> ").upper()
        if len(guess) != 5 and guess not in words:
            continue

        clues = [(guess, check_word(secret_word, guess))]
        guess_count += 1

        pos_word = filter_word_list(words, clues)
        num_possible_words = len(pos_word)

        # to print the previous guesses in the color format
        if guess_count > 1:
            for old_guess, old_clue in guess_list:
                color_index = 0
                for letter in old_guess:
                    if old_clue[color_index] == "green":
                        display_utility.green(letter)
                    elif old_clue[color_index] == "yellow":
                        display_utility.yellow(letter)
                    else:
                        display_utility.grey(letter)
                    color_index += 1
                print()

        guess_list.append(clues[-1])

        # to print the present guess in the color format
        for guess, clue in clues:
            color_index = 0
            for letter in guess:
                if clue[color_index] == "green":
                    display_utility.green(letter)
                elif clue[color_index] == "yellow":
                    display_utility.yellow(letter)
                else:
                    display_utility.grey(letter)
                color_index += 1
        print()

        if guess == secret_word:
            # if the correct word is same as guess then the program prints the secret word and breaks
            print(num_possible_words, "words possible:", end=" ")
            print()
            print(secret_word)
            print("ANSWER:", secret_word)
            break
        elif guess_count == 6:
            # if the user finishes all 6 guesses th program breaks
            break
        else:
            print(num_possible_words, "words possible:", end=" ")
            print()

            if num_possible_words <= 5:
                for word in pos_word:
                    print(word)
            else:
                store_word = random.sample(pos_word, 5) # selects a sample of 5 words from the possible words list
                for word in store_word:
                    print(word)
