# Code to run the Bagels game

from random import *
import time

class Game: 
    def __init__(self, guesserName, responderName,guessesAllowed): 
        self.guessedAllowed = guessesAllowed
        self.guesserName = guesserName
        self.responderName = responderName
    
    def createPlayers(self, guesserName, responderName): # Creates a guesser and responder object for the game
        guesserName = Guesser(guesserName)
        responderName = Responder(responderName)

        return guesserName, responderName

    def gameOver(self, guesses, guessesAllowed, guesserName, guess, answer): # Checks to see if the game is over
        
        if guesses == guessesAllowed:
            return True
        if guesserName.checkGuess(guess, answer) == ['Fermi!']:
            return True

        return False

    def playHumanisGuesser(self, guesserName, responderName, guessesAllowed): # Plays a game where the human is guesser
         
        guess, respond = self.createPlayers(guesserName, responderName) # Initializing some variables
        correctAnswer = respond.createNumber()
        numberList = ['0','1','2','3','4','5','6','7','8','9']
        guesses = 0
        theGuess = 'a'

        while not self.gameOver(guesses, guessesAllowed, guess, theGuess, correctAnswer): # The code that plays the game

            theGuess = input('What is your guess?')
            while not numberTest(theGuess):
                print('That is not a valid attempt! Try again.')
                theGuess = input('What is your guess?')
            
            numberList = guess.getKnownAbsent(numberList, theGuess, correctAnswer)
            print(','.join(guess.checkGuess(theGuess, correctAnswer)))
            if self.gameOver(guesses, guessesAllowed, guess, theGuess, correctAnswer) == False:
                print('The numbers left are:', ','.join(guess.getKnownAbsent(numberList, theGuess, correctAnswer)))
            guesses = 1 + guesses

        print('You won this round of Bagels in', guesses, 'guesses!')

    def playHumanIsResponder(self, guesserName, responderName, guessesAllowed): # Plays a game where human is responder
    
        numberList = ['0','1','2','3','4','5','6','7','8','9'] # Initializing some variables
        previousGuesses = ['']
        guess, respond = self.createPlayers(guesserName, responderName)
        guesses = 0
        theGuess = 'a'
        predCount = 1

        correctAnswer = input('What number do you want to play with?')  # The code that plays the game
        
        while not numberTest(correctAnswer):
            correctAnswer = input('That number is not valid! Try again.')
        
        while not self.gameOver(guesses, guessesAllowed, guess, theGuess, correctAnswer):
            
            theGuess, numberList, predCount, previousGuesses = guess.createGuess(correctAnswer, numberList, predCount, previousGuesses)
            print('Thinking...')
            time.sleep(1)
            print('My guess is', theGuess+ '!')
            print(','.join(guess.checkGuess(theGuess, correctAnswer)))

            guesses += 1
        
        print('I won this round of Bagels in', guesses,'guesses!')

       
class Responder:
    def __init__(self, name): 
        self.name = name
        
    def createNumber(self): # Has the responder create a number
        number = 'a'

        if self.name == 'AI': # Generates a random number if the responder is the computer
            while numberTest(number) == False:
                number = str(randint(12, 987))

                if len(number) == 2: 
                    number = '0' + number
            
            return number

        else: # Has the human create a Bagels number
            number = input('What number do you want to play with?')
            
            while numberTest(number) == False: 
                number = input("That number can't be played in accordance with the games rules. Try again!")
                numberTest(number)
                
            return number

class Guesser:
    def __init__(self, name):
        self.name = name

    def createGuess(self, correctAnswer, numberList, predCount, previousGuesses): # Creates a guess if the guesser is the computer
        aiGuess = ['','','']

        if (predCount <= 4) and (len(self.checkGuess(''.join(previousGuesses[-1]), correctAnswer)) != 3): # For the first 4 guesses, the computer
            if predCount == 1:                                                                    # will try these preset guesses 
                aiGuess = ['0','1','2']
            elif predCount == 2:
                aiGuess = ['3','4','5']
            elif predCount == 3:
                aiGuess = ['6','7','8']
            else:
                aiGuess = ['9','1','4']

            predCount += 1
            numberList, previousGuesses = self.updateList(aiGuess, correctAnswer, numberList, previousGuesses)
            return ''.join(aiGuess), numberList, predCount, previousGuesses

        else: # All other guesses will be decided in some part by randomness, and the previous guessses

            while (not numberTest(''.join(aiGuess))) or (aiGuess in previousGuesses): 
                for x in range(3):
                    randomDigit = randint(0, len(numberList) - 1)
                    aiGuess[x] = numberList[randomDigit]

            numberList, previousGuesses = self.updateList(aiGuess, correctAnswer, numberList, previousGuesses)
            return ''.join(aiGuess), numberList, predCount, previousGuesses        
        
    def updateList(self, guess, correctAnswer, numberList, previousGuesses): 

        # Updates the list of numbers the computer can pick from, and increases the probability of picking numbers more likely to be the correct answer

        if self.checkGuess(guess, correctAnswer) == ['Bagels']: # Removes numbers we know are not present
            for x in guess:
                while x in numberList:
                    numberList.remove(x)

            return numberList, previousGuesses

        elif self.checkGuess(guess, correctAnswer) == ['Fermi!']: # Doesn't do anything

            return numberList, previousGuesses

        else: # Increases the probability of a digit being present in the computer's guess, based on the hints given 
            if len(self.checkGuess(guess, correctAnswer)) == 1: 
                for x in guess:

                    numberList.append(x)
                    numberList.append(x)
                    numberList.append(x)
                previousGuesses.append(guess)

                return numberList, previousGuesses

            elif len(self.checkGuess(guess, correctAnswer)) == 2:
                for x in guess:
                    for digit in range(3):
                        numberList.append(x)

                previousGuesses.append(guess)

                return numberList, previousGuesses

            else:
                while len(numberList) > 0:
                    numberList.pop(0)
                for x in guess:
                    for digit in range(5):
                        numberList.append(x)

                previousGuesses.append(guess)

                return numberList, previousGuesses

    def checkGuess(self, guess, correctAnswer): # Compares a guess to the correct answer and returns hints
        correctAnswer = str(correctAnswer)
        responseList = []
        count = 0

        for number in guess:
            if number in correctAnswer:
                responseList.append('Pico')
            
        for number in guess:        
            if number == correctAnswer[count]:
                responseList.remove('Pico')
                responseList.append('Fermi')
            count += 1

        if responseList == []:
            return ['Bagels']
        elif responseList == ['Fermi', 'Fermi', 'Fermi']:
            return ['Fermi!']
        else:
            return responseList

    def getKnownAbsent(self, numberList, guess, answer): # Returns digits we know could possibly be in the answer
        '''Gets the numbers that we know are not present in the answer'''

        for number in guess:
             if (self.checkGuess(guess, answer) == ['Bagels'] and number in numberList):
                numberList.remove(number)

        return numberList

def numberTest(number): # Makes sure all numbers in this game qualify as Bagels numbers
        '''Tests the number to see if it is valid for this game'''
        try: # If the number is not a number
            int(number)
        except: 
            return False
        
        if len(number) != 3: # If the number doesn't have 3 digits
            return False
        
        digitsInNumber = []
        for i in number: # checks to see if any numbers are repeated
            if i in digitsInNumber:
                return False
            digitsInNumber.append(i)
        return True

def displayRules(): # Displays the rules of the game

    print('In Bagels, there are 2 players: the Guesser and Responder')
    print('The Responder picks a 3 digit number such that no digit is repeated twice.')
    time.sleep(3)
    print('The Guesser has to try and figure out which number it is based on the following hints of the responder:')
    print('Bagels: None of the digits guessed are in the number')
    print('Pico: A digit you guessed is in the number, but not in the right position')
    print('Fermi: A digit you guessed is in the number and in the right position')
    print("And keep in mind: All Picos come before Fermis, so the hints aren't necessarily given in order!")
    time.sleep(3)
    print("For example: if the responder's guess is 123:")
    print("A guess of 456 = Bagels")
    print("A guess of 145 = Pico")
    print("A guess of 137 = Pico, Fermi")
    print("And a guess of 123 wins!")

# Actual game starts here

guesserName = 'AI'
responderName = 'AI'
name = 'AI'
guesses = 9999
gameType = ''
showRules = ''

print('Hello and welcome to this game of Bagels!')

while name == 'AI':
    name = input('What is your name?')
    if name == 'AI':
        print('That name is not valid. Please try again.')

while showRules != 'Yes' and showRules != 'No': 
    showRules = input('Do you want to view the rules? (Input Yes or No)')

    if showRules == 'Yes':
        displayRules()
    elif showRules == 'No':
        break
    else:
        print('Please enter a valid response.')

while gameType != 'Guesser' or gameType != 'Responder':
    gameType = input ('Do you want to be the guesser or responder?(Input Guesser or Responder)')
    if gameType == 'Guesser':
        guesserName = gameType
        bagel = Game(guesserName, responderName, guesses)
        bagel.playHumanisGuesser(guesserName, responderName, guesses)
        break
    elif gameType == 'Responder':
        responderName = gameType
        bagel = bagel = Game(guesserName, responderName, guesses)
        bagel.playHumanIsResponder(guesserName, responderName, guesses)
        break
    else:
        print('That is not a valid response. Please try again.')
    


    

