# Game starts with the main menu, after user chooses 'play' game starts.
# The hidden word is chosen from the list and is presented to the user using dashes.
# User inputs 1 letter at a time and has 8 lives.
# Input is checked for its validity (lower ascii char),
# if the letter is in the hidden word, it's shown to the user.
# Every mistake (no such letter) costs one life. Non-valid input doesn't cost lives.
# When game ends, user is back in the main menu


import random
from string import ascii_lowercase


# checks input for its validity (lower ascii char, one char, not typed before)
def check(a):
    if len(a) > 1 or len(a) == 0:
        print('You should input a single letter')
        return False
    elif a not in ascii_lowercase:
        print('It is not an ASCII lowercase letter')
        return False
    elif a in guessed_letters_history:
        print('You already typed this letter')
        return False
    else:
        return True


print('H A N G M A N')
# main menu loop
while True:
    main_menu = input('Type "play" to play the game, "exit" to quit: ')
    if main_menu == 'exit':
        break
    # game starts
    elif main_menu == 'play':
        words = ['python', 'java', 'kotlin', 'javascript']
        word = random.choice(words)
        printed_word = list('-' * len(word))
        letters = set(word)
        lives = 8
        guessed_letters = set()
        guessed_letters_history = set()
        blanks = True
        while lives > 0:
            # prompts user for a letter, checks input validity
            print('')
            print(''.join(printed_word))
            if not blanks:
                print('You guessed the word!')
                lives = 0
                continue
            user_guessed_letter = input(f'Input a letter: ')

            # if input is valid, checks the word letters
            valid = check(user_guessed_letter)
            if valid:
                guessed_letters_history.add(user_guessed_letter)
                if user_guessed_letter in letters:
                    guessed_letters.add(user_guessed_letter)
                    counter = 0
                    for j in word:
                        if j == user_guessed_letter:
                            printed_word[counter] = user_guessed_letter
                        counter += 1
                        if '-' not in printed_word:
                            blanks = False
                else:
                    print('No such letter in the word')
                    lives -= 1
        # overall results
        print('You are hanged!\n' if blanks else 'You survived!\n')
    else:
        continue
