from kivy.clock import Clock
import random

# Creation of the game manager that handles most of the game activity
class GameManager:
    def __init__(self):
        self.currently_selected = False
        self.first_card = None
        self.card_count = 0
        self.second_card = None

    # A function that will change the screen to the win screen once the player has matched all the pairs
    def set_to_win_function(self, f):
        self.win_function = f

    # A function that will generate the list of pairs and randomise the order based on the difficulty
    def set_difficulty(self, difficulty):
        # Difficulty values will be 3, 4, 5
        # Generate list of values
        self.difficulty = difficulty
        value_list = []
        for i in range(0, self.difficulty):
            value_list.append(i)
        value_list = 2 * value_list

        random.shuffle(value_list)        
        self.values = value_list
        
    # A function to simply return the list of randomised pair values
    def get_values(self):
        return self.values

    # A function to check the pairs of cards to see if it is a corrct pair or not
    def card_check(self, card):
        if not self.currently_selected:
            self.currently_selected = True
            self.first_card = card
        else:
            self.second_card = card

            # A check to display the 2 cards for a short while if the pair is wrong before 
            # closing the pairs (For the memory part of the game) or add to the pair tally if correct
            if self.first_card.lbl.text != card.lbl.text:
                Clock.schedule_once(self.card_close, 0.5)
                
            else:
                self.first_card = None
                self.second_card = None
                self.currently_selected = False
                self.card_count += 1
        
        # Checks the total number of matched pairs and swaps to the win screen if the player matches all the pairs
        if self.card_count == self.difficulty:
            self.reset()
            self.win_function()

    # A function to reset the cards at the end of the game    
    def reset(self):
        self.values = []
        self.names = []
        self.card_count = 0

    # A function to close the cards if the pairs are wrong
    def card_close(self, dt):
        self.first_card.close()
        self.second_card.close()
        self.first_card = None
        self.second_card = None
        self.currently_selected = False
    
    # A function to prevent more than 1 card from being opened when checking if the first card is the same as the second
    def can_open(self):
        return self.first_card is None or self.second_card is None
            