'''
Created on Oct 10, 2018

@author: ming
'''

import random

def readWords(fname):
    """
    return a list of all strings
    stored in file whose path is fname
    format of file: one string per line
    """
    f = open(fname)
    data = []
    for line in f:
        data.append(line.strip())
    f.close()
    return data

def matches(template,word,skips):
    """
    template and word are both lists
    of the same length, skips is a list
    of single-character letters.
    return True if these parameters "match"
    match defined by template[i] = word[i]
    whenever template[i] != "_"
    TODO: return False when 
    template[i] = "_" and word[i] in skips
    """
    if len(template) != len(word):
        return False
    for dex in range(len(template)):
        if template[dex] != "_":
            if template[dex] != word[dex]:
                return False
            elif word[dex] in skips:
                return False

    return True

def allMatches(allwords,guessTemplate,skips):
    """
    allwords is a list of strings
    guessTemplate is a list representing
    a "guess" in hangman, consisting
    of letters or "_" for unguessed letters
    returns a list of strings from allwords that
    match guessTemplate
    """
    ret = []
    for word in allwords:
        if matches(guessTemplate,list(word),skips):
            ret.append(word)
    return ret

def mostfrequent(wordlist,skips):
    """
    return letter NOT in skips that occurs most often
    in strings in wordlist
    """
    mxletter = ''
    mxcount = 0
    for char in "abcdefghijklmnopqrstuvwxyz":
        if char in skips:
            continue
        c = 0
        for word in wordlist:
            c += word.count(char)
        if c > mxcount:
            mxcount = c
            mxletter = char
    return mxletter
 
def makeTemplate(length):
    """
    length is an int
    return ["_","_",..."_"] with length "_" occurrences
    """
    ret = []
    for _ in range(length):
        ret.append("_")
    return ret           

def play(wordlist):
    wordLength = input("how many letters> ")
    wordLength = int(wordLength)
    template = makeTemplate(wordLength)
    
    guessedList = []    # list of all characters computer has guessed
    misses = 0          # misses in guessing user's word
    while True:
 
        guesses = allMatches(wordlist,template,guessedList)
        print("# misses = %d, # words = %d" % (misses,len(guesses)))
        if len(guesses) == 0:
            print("I give up")
            break
        print("word so far:",template)
        letter = mostfrequent(guesses,guessedList)
        print("my guess is: ",letter)
        guessedList.append(letter)
        ucount = template.count("_")
        template = input("enter template as string: ")
        template = list(template)
        nucount = template.count("_")
        if len(template) != wordLength:
            print("your template isn't right")
            print("it has",len(template),"letters")
            break
        
        if nucount == 0:
            print("I guessed your word")
            break
        if nucount == ucount:
            misses += 1

if __name__ == '__main__':

    wordlist = readWords("data/lowerwords.txt")
    #print("number of words:",len(wordlist))
    print(type(play(wordlist)))
