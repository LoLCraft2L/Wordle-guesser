#Importings 
import random
import json

#Base Code
class word:
    
    def __init__(self):
        self.known = ["","","","",""]
        self.unknown = {}
        self.invalid = []
        self.guess = ""
        self.random_guess = ""
        #Load Json
        with open('words.json','r') as f:
          self.answers = json.load(f)
    
    #Gray Words in Wordle
    def remove_words(self, letters):
       if letters == []:
          return 
       for i in letters:
          self.invalid.append(i)
          if (i in self.answers.keys()) and (i not in self.known):
             del self.answers[i]
    

    #Green words in Wordle
    def check_known(self, output):
       for pos, letters in enumerate(output):
           if self.known[pos] == "":
                continue
           elif self.known[pos] != letters:
                if output in self.answers[output[0]]:
                   self.answers[output[0]].remove(output)
                return False
       return True
    
    #Yellow words in wordle
    def check_unknown(self, output):
       for position in self.unknown:
          if len(set(self.unknown[position]).intersection(set(output))) != len(self.unknown[position]):
             return False             
       for pos, letters in enumerate(output):
          if pos in self.unknown.keys():
             if letters in self.unknown[pos]:
                if output in self.answers[output[0]]:
                   self.answers[output[0]].remove(output)
                return False
       return True
   
   #Gray words in wordle
    def check_gray(self, output):
     for i in output:
        if i in self.invalid:
           if output in self.answers[output[0]]:
               self.answers[output[0]].remove(output)
           return False
     return True
          
    #Give a random output that satisfies all the condition
    def guesser(self):
      alphabet = random.choice(list(self.answers.keys()))
      while (self.answers[alphabet] == []):
         alphabet = random.choice(list(self.answers.keys()))
      self.random_guess = random.choice(self.answers[alphabet])



   
   #Take string and separate yellow green and gray
    def process(self, guess, yellow, green):
      

       #For Green
       if green != "":
          green = green.lower().split(" ")
          for pos, letters in enumerate(guess[:]):
             if (letters in green) or (str(pos) in green):
                self.known[pos] = letters
                green.remove(letters) if (letters in green) else green.remove(str(pos))
                guess = guess[:pos] + guess[pos+1:]
             
         
       #For Yellow
       if yellow != "":
          yellow = yellow.lower().split(" ")
          for pos, letters in enumerate(guess[:]):
             if (letters in yellow) or (str(pos) in yellow):
                if pos not in self.unknown.keys():
                   self.unknown[pos] = []
                self.unknown[pos].append(letters)
                yellow.remove(letters) if (letters in yellow) else yellow.remove(str(pos))
                guess = guess[:pos] + guess[pos+1:]
      
       if guess != "":
         self.remove_words(guess)
      
       self.guesser()
       while (self.check_unknown(self.random_guess) + self.check_known(self.random_guess) + self.check_gray(self.random_guess)!= 3):
          self.guesser()
       
          
          
wordle_guesser = word() 

for i in range(5):
   guess = input("Enter your guess: ")
   yellow = input("Enter Yellows: ")
   green = input("Enter Green: ")
   wordle_guesser.process(guess, yellow ,green)
   print(wordle_guesser.random_guess)

with open("possible_answers.json", "w") as f:
   json.dump(wordle_guesser.answers, f, indent=4)