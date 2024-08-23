import random
import display_utility
from words import *


def check_word(secret, guess):
    """
    This function takes in two parameters which are the secret word and the clues and returns a list of length 5
    containing the string "grey","yellow", and "green" which represent the letter color.
    :param secret:
    :param guess:
    :return: a list of length 5 containing strings.
    """
    # Initially assigning the clues list with all grey values which is a default value
    clues_list = ["grey", "grey", "grey", "grey", "grey"]
    # Identifying and adding all green matches that occur between secret and guess
    # Prioritizing green hint first compared to yellow
    for i in range(len(clues_list)):
        if secret[i] == guess[i]:
            clues_list[i] = "green"

    # Creating a dictionary to store every character and its respective positions as a list
    letter_counts_dict = {}
    for i in range(len(clues_list)):
        letter_key = secret[i]
        letter_pos = []  # List to add the position of specific characters
        if letter_key not in letter_counts_dict:
            letter_pos.append(i)
            letter_counts_dict[
                letter_key] = letter_pos  # Adding a key pair value with a character and its respective position
        else:
            letter_counts_dict[letter_key].append(i)  # Appending the new index position for characters already present

    # To identify and assign yellow clues to the positions which are not green in the clues_list
    # Creating a position set that will keep track of the positions present in secret which have already been assigned green colour

    green_position_set = set()
    for i in range(len(clues_list)):
        if clues_list[i] == "green":
            green_position_set.add(i)  # Adding the index position of green letters to the set
        elif guess[i] in letter_counts_dict:
            position_index_list = letter_counts_dict[
                guess[i]]  # Retrieving the list of positions if guess[i] is in the letter count dictionary
            # Traversing through every position where the letter appears in the secret string
            for position in position_index_list:
                # Checking if position is already assigned green and ensuring that guess and secret characters at a specific position are not the same
                if guess[position] != secret[position] and position not in green_position_set:
                    clues_list[i] = "yellow"  # Assigning the specific position with yellow
                    green_position_set.add(position)  # Adding the specific green psoition set
                    break  # breaking the loop in order to find the next non green psoition in the clues_list

    return clues_list


def known_word(clues):
    """
    This function takes in a single parameter which is a list containing a record of guesses and clues and return a
    string where positions that do not have a green clue are given out as '_' and the known letters (green) are revealed.
    :param clues:
    :return: String ( it contains underscores and known letters)
    """
    # Creating a underscore list with all its position assigned to underscore which states that initially we assume that there are no green clues letters that are identified
    underscore_list = ['_', '_', '_', '_', '_']
    known_string = ''
    for guess, clue in clues:  # Traversing through every guess and clue present in clues list
        for i in range(len(clue)):
            clue_letter = clue[i]
            if clue_letter == 'green':
                # Update the known letters at the position indicated by the green clue
                underscore_list[i] = guess[i]

    # Converting the list back to the string containing the green letter clues and underscore
    for char in underscore_list:
        known_string += char + ''

    # Return the known word as a string
    return known_string


def no_letters(clues):
    """
    This function takes in a single parameter which is a list containing a record of guesses and clues and returns
    a string which indicate the letters that are not in the word according to the grey hints
    :param clues:
    :return: A string ( letters that are not in the word according to grey hints)
    """
    required_clues = {} # dictionary to keep count of letters that are part of the word
    res_str = '' # the final result string
    letter_count = {} # dictionary to keep the count of letters

    for guess, clue in clues:
        for char in guess:
            if char not in letter_count:
                letter_count[char] = 0
            letter_count[char] += 1 # incrementing the count of a letter
        for i in range(len(clue)):
            if clue[i] == 'green' or clue[i] == 'yellow':
                required_clues[guess[i]] = 1 # to identify the green and yellow clue letters
            letter_count[guess[i]] -= 1   # subtracting in a way to indicate that these are correct guess letters

    for char in letter_count:
        if char not in required_clues and letter_count[char] == 0:
            res_str += char

    res_str = ''.join(sorted(set(res_str)))
    return res_str.upper()


def yes_letters(clues):
    """
    This function takes in a single parameter which is a list containing a record of guesses and clues and returns
    a string which indicate the letters that are counted as green and yellow hints.
    :param clues:
    :return: A string (it contains green and yellow hinted letters)
    """
    # Creating a set to sore all the correctly identified letter which belong to both green and yellow
    correct_letters = set()
    result_string = ''
    for clue in clues:
        guess = clue[0]  # assigning every guess using first index
        clue = clue[1]  # assigning every clue using the second index
        for i in range(len(guess)):  # iterating over every guess
            if clue[i] == 'green' or clue[i] == 'yellow':  # checking if the corresponding guess clue is green or yellow
                upper_letter = guess[i].upper()
                correct_letters.add(upper_letter)  # adding the correct set of clues to the set

    sorted_set = sorted(correct_letters)
    for char in sorted_set:
        result_string += char

    return result_string


# the following functions are helper function which are written to implement in the main program part

def valid_guess(guess, word_list):
    """
    This functon takes in the guess and word_list and return a boolean value by checking the length and the existence
    of the guess in word_list
    :param guess:
    :param word_list:
    :return: boolean value
    """
    return len(guess) == 5 and guess.lower() in word_list  # checking if length is 5 and guess exists in the list


def get_guess():
    """
    This function runs until a valid guess is entered and validates through the use valid_guess() and returns the
    upper case of the guess word if it is in valid format
    :return: upper case of guess word
    """
    while True:
        guess = input("> ").lower()
        if valid_guess(guess, words):
            return guess.upper()


def wordle_game():
    """
    This function implements the runnable wordle game
    :return: does not return anything
    """
    secret_word = "lered" #random.choice(words)
    secret_word = secret_word.upper()
    clues = []
    guess_left = 6

    while guess_left > 0:
        print("Known word:", known_word(clues))
        print("Green/Yellow Letters:", yes_letters(clues))
        print("Grey Letters:", no_letters(clues))
        guess = get_guess()

        clues_list = check_word(secret_word, guess)
        clues.append((guess, clues_list))
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

        if known_word(clues) == secret_word:
            print("ANSWER:", secret_word)
            break
        guess_left = guess_left - 1

        if guess_left == 0:
            print("Secret word is: ", secret_word)


if __name__ == "__main__":
    wordle_game()

