'''
Description:
        You must create a Hangman game that allows the user to play and guess a secret word.  
        See the assignment description for details.
    
@author: Sayuka Urakami su45
'''


import random

def handleUserInputDifficulty():
    '''
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the 
    corresponding number of misses allowed for the game. 
    '''
    # first printing the statement for asking the difficulty
    print("How many misses do you want? Hard has 8 and Easy has 12")
    # make input
    dif = input("(h)ard or (e)asy> ")
    # if the input is h return 8, e return 12
    if dif is "h":
        return 8
    if dif is "e":
        return 12


def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''
    # create displayString(guessedletters(str),missesLeft,hangmanWord(str))
    lettersRemain = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for ch in lettersGuessed:
        ind = lettersRemain.index(ch)
        lettersRemain[ind] = ' '

    displayString =str( "letters not yet guessed: " + "".join(lettersRemain) + "\n" + "misses remaining = " + str(missesLeft) + "\n"+ " ".join(hangmanWord))
    return displayString

def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''

    # print displayString
    print(displayString)
    # make input
    guessedLetter = str(input("letter>"))

    # search guessedLetter is already guessed or not
    # if it is already guessed, continue to ask another guessedLetter
    while guessedLetter in lettersGuessed:
        print("you already guessed that")
        guessedLetter = str(input("letter>"))
    # if it is new, append it to letterGuessed
    else:
        lettersGuessed.append(guessedLetter)

    return guessedLetter


def handleUserInputDebugMode():
    """
    make a input to ask the mode to the user
    if the input is d, return true
    """
    mode = input("Which mode do you want: (d)ebug of (p)lay: ")
    if mode is "d":
        return True
    else:
        return False


def handleUserInputWordLength():
    """
    ask the length of the word to the user
    return int
    """
    length = input("How many letters in the word you'll guess: ")
    return int(length)


def createTemplate(currTemplate, letterGuess, word):
    """
    create a new template fir secret word that the user will see
    """
    currTemplate = [w for w in currTemplate]
    for i in range(len(word)):
        # if guessedLetter is in secretWord, the ch is revealed
        if word[i] is letterGuess:
            currTemplate[i] = letterGuess
    return "".join(currTemplate)


def getNewWordList(currTemplate, letterGuess, wordList, debug):
    """
    create a dictionary, key=strings and value=list
    according to the user's guess, pick up the new secret word from the longest value
    if the length is tie, return which has more "_"
    return tuple
    """
    d = {}
    count = 0
    for word in wordList:
        if len(word) == len(currTemplate):
            template = createTemplate(currTemplate,letterGuess, word)
            if template not in d:
                d[template] =[]
            d[template].append(word)
            count += 1

        new = sorted(d.items())
        underscore = sorted(new, key=lambda x: x[0].count("_"),reverse=True)
        maxWords = max(underscore,key=lambda x: len(x[1]))

    if debug is True:
        print("(word is "+random.choice(maxWords[1])+")")
        print("# possible words:" + str(count))
        for (k, v) in new:
            print(k + " : "+ str(len(v)))
        print("# keys = " + str(len(d)))
    return maxWords


def processUserGuessClever(guessedLetter, hangmanWord, missesLeft):
    """
    return the number of misses left
    and bool if the user guessed a letter in the word
    """
    process = []
    if guessedLetter in hangmanWord:
        process.append(missesLeft)
        process.append(True)
    if guessedLetter not in hangmanWord:
        missesLeft -= 1
        process.append(missesLeft)
        process.append(False)
    return process


def runGame(filename):
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    '''

    # open file
    f = open(filename)
    # make list
    words = []
    # append all line to words
    for line in f:
        words.append(line.strip())
    f.close()

    debug = handleUserInputDebugMode()
    # choose length by user's input
    length = handleUserInputWordLength()
    # choose secretWord by calling getWord
    # decide the #s of misses by calling handleUserInputDifficulty

    missesLeft = handleUserInputDifficulty()


    # make the list that has length's #s of "_"
    hangmanWord = []
    for i in range(length):
        hangmanWord.append("_")

    currTemplate = "".join(hangmanWord)

    # make empty list and int for accumulation
    lettersGuessed = []
    misses = 0

    wordList = [w for w in words if len(w)==length]
    secretWord = random.choice(wordList)

    # while loop only not if player won or lost
    while "".join(hangmanWord) != secretWord and missesLeft != 0:
        # call functions
        displayString = createDisplayString(lettersGuessed,missesLeft,hangmanWord)

        guessedLetter = handleUserInputLetterGuess(lettersGuessed,displayString)
        letterGuess = guessedLetter


        new = getNewWordList(currTemplate, letterGuess, wordList, debug)
        wordList = new[1]
        hangmanWord = new[0]

        for word in wordList:
            currTemplate = createTemplate(currTemplate,letterGuess,word)
        secretWord = random.choice(wordList)
        process = processUserGuessClever(guessedLetter, hangmanWord, missesLeft)
        missesLeft = process[0]

        # if guessedletter is not in secretword, it is miss
        if process[1] is False:
            misses += 1
            print("you missed:",guessedLetter,"not in word")

    # if there is no "_", player won, return true
    ncount = hangmanWord.count("_")
    if ncount == 0:
        print("you guessed the word:", secretWord)
        print("you made", len(lettersGuessed), "guesses with", misses, "misses")
        return True

    # if missesLeft became 0, player lost
    if missesLeft == 0:
        print("you are hung!!")
        print("word is", secretWord)
        print("you made", len(lettersGuessed), "guesses with",misses,"misses")
        return False


if __name__ == "__main__":
    '''
    Running CleverHangman.py should start the game, which is done by calling runGame, therefore, we have provided you this code below.
    '''
    # define filename
    filename = 'lowerwords.txt'
    # call runGame and define it
    TorF = runGame(filename)
    # make input and define it
    again = input("Do you want to play again? y or n>")
    lost = 0
    won = 0

    # make int for counting won and loss
    if TorF is False:
        lost += 1
        won += 0

    if TorF is True:
        won += 1
        lost += 0

    # if player chose y, play it again
    while again is "y":
        TorF = runGame('lowerwords.txt')
        if TorF is False:
            lost += 1
        if TorF is True:
            won += 1
        again = input("Do you want to play again? y or n>")
    # when finishing the game, print the session
    else:
        print("You won", won, "game(s) and lost", lost)
