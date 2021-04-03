
"""
  AUTHOR: KHALED BADRAN 
"""

import random
import string
import time


WORDS_FILENAME = "random_words.txt"      # to open the file of the random words


def load_words():
  """ open the file of the random words and load them. 

  Returns:
    list of strings: list of the random words from the file
  """
  words_file = open(WORDS_FILENAME, 'r') # to read/load the words from the file 
  
  file_content = words_file.read()  # read all the content of the file as a string
  words_list = file_content.split() # words_list: list of the random words (list of strings)

  words_file.close() # to close the file of words that we have opened. 

  return words_list


words_list = load_words() # Load the list of words into the variable words_list
                          # global variable can be accessed from anywhere

def choose_word(words_list):  
  """ choose a random word from the file of the words   

  Arguments:
    words_list (list of strings): list of the random words from the file  

  Returns:
    string: a random word from the file of the words 
  """

  return random.choice(words_list)


def hangman(secret_word):
  """This is the most important function of this game.
     *Start up an interactive game of Hangman.
     *At the start of the game, show the user/player how many 
      letters the secret_word contains and how many guesses and warnings he starts with.
     *Before each round, show the user/player the partially guessed word so far. 
      Show the user the number of guesses and warnings left so far.
      Show the user the letters that have not been guessed yet.
     *After each guess, tell the user if the guess was correct or wrong,
      and show him the partially guessed word so far.
     *in the end, tell the player if he won or lost, reveal the secret word,
      and show him his score.

    Arguments: 
      secret_word (string): the secret, random word that the player should guess
  """
  start_hangman(secret_word) # to print the introductory part of the game.

  available_guesses  = 6     
  available_warnings = 3     
  guessed_letters    = []    # all the valid letters that the player has ever guessed.

  while available_guesses > 0:
    if is_word_guessed(secret_word, guessed_letters):   # if the secret word has already been guessed correctly, break the loop.
      break

    time.sleep(1)     # Just to make the game look a little bit realistic/animated.
    print("--------------------")

    print("The secret word is: " + get_guessed_word(secret_word, guessed_letters))  
    print_hanged_man(available_guesses)
    print("You have "+ str(available_warnings) + " warning(s) left.")
    print("You have "+ str(available_guesses) + " guess(es) left.")
    print("avaliable letters are: " + get_available_letters(guessed_letters))
    player_input = str.lower(input("please guess a letter: "))  # getting the input from the player

    if is_input_valid(player_input):  # if input is valid (only one english letter from a to z or from A to Z).  
      if player_input not in guessed_letters:  # if the player has not entered the same input ounce before. 
        guessed_letters.extend(player_input)   # add the new input to the list of all guesssed_letters.
        if is_letter_guessed_correctly(player_input, secret_word): # if the input is a correct guess.
          print("Good guess: ", end = "") # (end = "") just to avoid adding a new line 
        else: 
          print("Oops! That letter is not in my word: ", end = "" )
          available_guesses -= 1
      else: # if the player has already entered the same input ounce before, he loses one warning or he loses one guess if there are no warnings available anymore
        if available_warnings > 0: 
          available_warnings -= 1
          print("Oops! You've already guessed that letter "+ "(" +str(player_input)+ ")." + 
          " You now have "+ str(available_warnings) + " warning(s).", end = "" )    
        else:  
          available_guesses -= 1
          print("Oops! You've already guessed that letter "+ "(" +str(player_input)+ ")." +
          " You have no warnings left, so you lost one guess. Now you have " + str(available_guesses) +
          " guess(es) left. ", end = "" )
    else:  # if the input is not valid, he loses one warning or he loses one guess if there are no warnings available anymore
      if available_warnings > 0: 
        available_warnings -= 1
        print("Oops! That is not a valid letter. You have " + str(available_warnings) +
        " warning(s) left: ", end = "" )
      else: 
        available_guesses -= 1
        print("Oops! That is not a valid letter. You have no warnings left, so you lost one guess. Now you have " +
              str(available_guesses) + " guess(es) left. ", end = "" )

    print(get_guessed_word(secret_word, guessed_letters))  # to show the player the partially guessed word so far.

  time.sleep(1)  
  print("")
  if is_word_guessed(secret_word, guessed_letters): # if the player has completely guessed the secret word correctly 
    print("Congratulations, you won! :)")
    time.sleep(1)
    print("The secret word is: \"" + secret_word.upper() + "\"") # Uppercase letters are used in this case only to make the secret word easily noticeable
    print("Your total score for this game is: " + str( available_guesses + available_warnings + 1) + "/10") 
    # plus 1 because the maximum possible score without 1 = available_guesses + available_warnings 
    #                                                     =      6            +       3             = 9. 
    # That's why + 1. Just to make it possible to get 10/10
  else:
    print_hanged_man(available_guesses) 
    print("Sorry, you lost because you ran out of guesses.")
    time.sleep(1)
    print("The secret word was: \"" + secret_word.upper() + "\"")
    
    n_guessed_correctly = 0 # number of the correctly guessed letters
    for i in get_guessed_word(secret_word, guessed_letters):
      if i != "*": n_guessed_correctly += 1

    print("Your total score for this game is: " + str(n_guessed_correctly) + "/" + str(len(secret_word)))
    # if the player lost, the score = number of the correctly guessed letters / length of the secret word

def start_hangman(secret_word):
  """ print the introductory part of the game.

  Arguments:
    secret_word (string): the secret, random word that the player should guess
  """
  print("  # WELCOME TO HANGMAN #")
  print("   -------------------")
  print("Loading the random words from the file .....")
  time.sleep(0.50)
  print("  ....") 

  print("  ", len(words_list), "words loaded.") # to show the player how many words are there in the file. 
  print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
  print("You have 6 guesses and 3 warnings to start the game with.")
 

def is_word_guessed(secret_word, guessed_letters):
  """ check whether the secret_word has been completely guessed correctly or not.

  Arguments:
    secret_word (string): the secret, random word that the player should guess
    guessed_letters (list of strings): a list that contains all the valid inputs that the player has ever entered 
  
  Returns:
    boolean: True if the secret_word has been completely guessed; False otherwise.
  """
 
  for i in secret_word:
    found = False 
    for j in guessed_letters:
      if i == j: 
        found = True
    if not found: 
      return False  

  return True  


def get_guessed_word(secret_word, guessed_letters): 
  """ get the secret word with the correctly guessed letters so far.

  Arguments:
    secret_word (string): the secret, random word that the player should guess
    guessed_letters (list of strings): a list that contains all the valid inputs that the player has ever entered 

  Returns:
    string : the secret word with the correctly guessed letters
  """

  guessed_correctly = ""
  for index in range(len(secret_word)):
    found = False 
    for letter in guessed_letters:
      if secret_word[index] == letter:  # if the guessed letter is in the secret word, add it to the string (guessed_correctly)
        guessed_correctly += letter      
        found = True 
    if not found:
      guessed_correctly += "*"    # if the guessed letter is a wrong guess, add "*" to the string (guessed_correctly)
     
  return guessed_correctly      
  

def get_available_letters(guessed_letters = ""):
  """ check which letters have not yet been guessed. 
  the letter is available, if it has not been guessed yet.

  Arguments:
    guessed_letters (list of strings): a list that contains all the valid inputs of all guesses that the player entered 

  Returns:
    string : all the remaining english letters that the player has not entered yet.
  """

  available_letters = ""
  all_letters = string.ascii_lowercase  # all the lower english letters from a to z
  for i in all_letters:
    available = True
    for j in guessed_letters:
      if i == j:
        available = False 
    if available: # if the letter has not yet been guessed, then it is available
      available_letters += " " + i

  return available_letters


def is_letter_guessed_correctly(player_input, secret_word):
  """ check whether the (guessed_letter/ player_input) is in the secret_word

  Arguments:
    player_input (string): the player_input
    secret_word (string): the secret, random word that the player should guess

  Returns:
    boolean: True if the player_input is in the secret_word; False otherwise
  """
  
  for i in secret_word:
    if player_input == i:
      return True

  return False    


def is_input_valid(player_input):
  """check whether the (guessed_letter/ player_input) valid or not.
  The player_input is valid, if it is only one english letter (can be uppercase and lowercase)
  from a to z.  
  
  Arguments:
    player_input (string): the input that the player entered

  Returns:
    boolea: True if the player_input is a valid input; False otherwise
  """

  if len(player_input) == 1 and player_input.isalpha():
    return True

  return False 


def print_hanged_man(available_guesses):
  """print the diagram that is designed to look like a hanging man.
  
  Arguments:
    available_guesses (integer): number of the remaining available guesses 
  """

  if available_guesses == 5:
    print( "   (-_-)" )
  if available_guesses == 4:
    print( "   (-_-)\n" +
           "     |    " )
  if available_guesses == 3:
    print( "   (-_-)\n" +
           "   --|    " )
  if available_guesses == 2:
    print( "   (-_-)\n" +
           "   --|--  " )
  if available_guesses == 1:
    print( "   (-_-)\n" +
           "   --|--\n" +
           "    /     " )
  if available_guesses == 0:
    print( "   (-_-)\n" +
           "   --|--\n" +
           "    / \   " )   


if __name__ == "__main__":

  secret_word = choose_word(words_list)
  hangman(secret_word)
