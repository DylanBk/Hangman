# IMPORTS
from wonderwords import RandomWord

# VARIABLES
# guesses = 11
# r = RandomWord()
# word = r.word()
# word_dict = {}
# counter = 0
# for i in word:
#     word_dict[counter] = i
#     counter += 1

# SUBROUTINES
def setup():
    """
    ...Sets values for the start of a game.

    Returns:
        guesses (int): How many guesses the user has (11).
        word (str): The word to guess.
        word_dict (dict): A dictionary containing each letter of word(str).
        dupe_keys (lst): An empty list for duplicate letters to populate.
        hidden_word (str): The word with its letters replaced with underscores.
        hidden_word_list (lst): A list of the underscores and spaces.
    """
    guesses = 11
    r = RandomWord()
    word = r.word()
    word_dict = {}
    counter = 0
    for i in word:
        word_dict[counter] = i
        counter += 1

    hidden_word, hidden_word_list, dupe_keys = hide_word(word, word_dict)
    print("test")
    return guesses, word, word_dict, dupe_keys, hidden_word, hidden_word_list

def hide_word(word, word_dict):
    """
    ...Changes the word into a series of underscores.

    Args:
        word (str): The word to be hidden.
        word_dict (dict): A dictionary containing the letters in word(str).

    Returns:
        hidden_word (str): The word with its letters replaced with underscores.
        hidden_word_list (lst): A list of the underscores and spaces.
        dupe_keys (lst): A list of duplicate keys from a flipped dictionary to account for duplicate letters in the word to guess. 
    """
    hidden_word_list = []
    for i in word:
        if i.isalpha():
            hidden_word_list.append("_")
        else:
            hidden_word_list.append(" ")
    hidden_word = "".join(hidden_word_list)

    flipped_dict = {}
    for k, v in word_dict.items():
        if v not in flipped_dict:
            flipped_dict[v] = [k]
        else:
            flipped_dict[v].append(k)

    flipped_lst = []
    for k, v in flipped_dict.items():
        flipped_lst.append(v)
    dupe_keys = get_dupes(flipped_lst)

    return hidden_word, hidden_word_list, dupe_keys

def get_dupes(x):
    """
    ...Gets a list of duplicate values.

    Args:
        x (lst): The list of values to loop through.
    Returns:
        dupe_keys (list): A list of all duplicate values, separated.
    """
    for i in x:
        for r in (("[",""),("]",""),("'",""),(",","")):
            i = str(i).replace(*r) # *r means all arguments in the above line
        i = i.strip()
        if len(i) > 1:
            x = i.split()
            get_dupes(x)
        dupe_keys = x

    return dupe_keys

def guess(user_guess, hidden_word, hidden_word_list, word_dict, dupe_keys, guesses):
    """
    ...Checks if the user's guess is correct.

    Args:
        user_guess (str): The user's guess as a single letter.
        hidden_word (str): The word with its letters replaced with underscores.
        hidden_word_list (lst): A list of the underscores, guessed letters, and spaces.
        word_dict (dict): A dictionary containing the letters in word(str).
        dupe_keys (lst): A list of duplicate keys from a flipped dictionary to account for duplicate letters in the word to guess.
        guesses (int): How many guesses the user has left.

    Returns:
        hidden_word (str): An updated version of hidden_word containing letters, if guessed correctly.
        guesses (int): How many guesses the user has left.
    """
    if user_guess == "":
        print("\nGuess cannot be blank, try again\n")
        main(hidden_word, hidden_word_list, guesses, dupe_keys, word, word_dict)
    elif user_guess.isnumeric():
        print("\nGuess cannot be a numeric value, try again\n")
        main(hidden_word, hidden_word_list, guesses, dupe_keys, word, word_dict)
    elif len(user_guess) > 1:
        print("\nGuess must be a single letter, try again\n")
        main(hidden_word, hidden_word_list, guesses, dupe_keys, word, word_dict)
    elif user_guess in word:
        for key in word_dict.keys():
            x = word_dict[key]
            if x == user_guess:
                guesses = guesses - 1
                hidden_word_list[key] = user_guess

                for k, v in word_dict.items(): #check if user's guess has more than 1 instances in the word
                    for i in dupe_keys:
                        if str(i) == str(k):
                            if v == user_guess:
                                hidden_word_list[int(i)] = user_guess

                hidden_word = "".join(hidden_word_list)
                return hidden_word, guesses
    else:
        print(f"\n{user_guess} is not in the word\n")
        guesses = guesses - 1
        return hidden_word, guesses

def main(hidden_word, hidden_word_list, guesses, dupe_keys, word, word_dict):
    guessed = False
    while guessed == False:
        if "_" not in hidden_word:
            guessed = True
            break

        if guesses == 0 and "_" in hidden_word:
            print(f"\nThe word was {word}. You lost!\n")
            x = input("Play again? [y/n]\n> ").lower()
            if x == "y":
                guesses, word, word_dict, dupe_keys, hidden_word, hidden_word_list = setup()
                main(hidden_word, hidden_word_list, guesses, dupe_keys, word, word_dict)
            else:
                exit()

        print(f"\n{hidden_word}")
        print(f"Guesses Remaining: {guesses}")
        user_guess = input("Enter your guess:> ")
        hidden_word, guesses = guess(user_guess, hidden_word, hidden_word_list, word_dict, dupe_keys, guesses)
    print(hidden_word)
    print("\nYou won!")
    x = input("Play again? [y/n]\n> ").lower()
    if x == "y":
        guesses, word, word_dict, dupe_keys, hidden_word, hidden_word_list = setup()
        main(hidden_word, hidden_word_list, guesses, dupe_keys, word, word_dict)
    else:
        exit()

# MAIN
guesses, word, word_dict, dupe_keys, hidden_word, hidden_word_list = setup()
print("-- Hangman --")
main(hidden_word, hidden_word_list, guesses, dupe_keys, word, word_dict)