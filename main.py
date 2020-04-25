from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button 
from kivy.uix.label import Label
from kivy.app import App
from kivy.core.window import Window
from card import Card
from game_manager import GameManager
from functools import partial
from kivy.graphics import Color, Rectangle

# Code for the Menu Screen (Will the first screen that opens up to the player)
class MenuScreen(Screen):
    def __init__(self, gamemanager, gamescreen, **kwargs):
        Screen.__init__(self, **kwargs)
        self.gamemanager = gamemanager
        self.gamescreen = gamescreen
        self.layout = BoxLayout(orientation = 'vertical', padding = (300,20))
        
        intro_lbl = Label(text = "Memory Maestro 3000", font_size = 36)
        self.layout.add_widget(intro_lbl)
        empty_lbl = Label(text = "", font_size = 36)
        self.layout.add_widget(empty_lbl)

        # A list of the various difficulties and the number of sets that the player will have to make for each difficulty
        difficulty_list = (('Easy', 3), ('Medium', 4), ('Hard', 5))

        # Adding the difficulty buttons to the game
        for i in difficulty_list:
            btn_game = Button(text = i[0], on_press = partial(self.change_to_game, i[1]), font_size = 36)
            self.layout.add_widget(btn_game)
        
        # A quit button to quit the game
        btn_quit = Button(text = "Quit", on_press = self.quit_app, font_size = 36)
        self.layout.add_widget(btn_quit)
        self.add_widget(self.layout)

    # A function to transition to the game based on the difficulty of the game (Ties in with the difficulty buttons)
    def change_to_game(self, value, diff):
        self.manager.transition.direction = 'left'
        # modify the current screen to a different "name"
        self.gamemanager.set_difficulty(value)
        self.gamescreen.create_game(value)
        self.manager.current = 'game'
    
    # A function to quit the game (Ties in with the quit button)
    def quit_app(self, value):
        App.get_running_app().stop()
        Window.close()

# The game screen which will be seen by the players upon choosing their difficulty
class GameScreen(Screen):
    def __init__(self, gamemanager, **kwargs):
        Screen.__init__(self, **kwargs)
        self.gamemanager = gamemanager
        
    # Function that creates the game based on the difficulty given, where the number of columns equals 
    # to the number of sets such that the cards are distributed evenly on the screen
    def create_game(self, difficulty):
        self.clear_widgets()
        self.layout = GridLayout(cols=difficulty)
        self.add_widget(self.layout)  
        cardlist = []

        # Creation of the cards and appending them to a list
        for i in range(0, 2*difficulty):
            c = Card(self.gamemanager.get_values()[i], self.gamemanager)
            cardlist.append(c)

        # Adding the cards in the list to the game screen
        for j in range(len(cardlist)):
            self.layout.add_widget(cardlist[j].layout)

    # A function to transition to the Win Screen once the player has matched all the pairs correctly    
    def change_to_win(self):
        self.manager.transition.direction = 'right'
        # modify the current screen to a different "name"
        self.manager.current = 'win'

# The Win Screen which will be seen by players upon winning the game
class WinScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout(orientation = 'vertical', padding = (200,200))
        # Add your code below to add the label and the button
        lbl_setting = Label(text = "You Win", font_size = 36)
        self.layout.add_widget(lbl_setting)
        btn_menu = Button(text = "Back To Menu", font_size = 36, on_press = self.change_to_menu)
        self.layout.add_widget(btn_menu)
        self.add_widget(self.layout)
    
    # A function to take the player back to the main menu (Ties in with the "Back To Menu" button)
    def change_to_menu(self, value):
        self.manager.transition.direction = 'right'
        # modify the current screen to a different "name"
        self.manager.current = 'menu'

# The main code for the app with the different screens and the Game Manager
class GameApp(App):
    def build(self):
            gamemanager = GameManager()
            sm = ScreenManager()
            gt = GameScreen(gamemanager, name='game')
            ms = MenuScreen(gamemanager, gt, name='menu')
            win = WinScreen(name='win')
            gamemanager.set_to_win_function(gt.change_to_win)
            sm.add_widget(ms)
            sm.add_widget(gt)
            sm.add_widget(win)
            sm.current = 'menu'
            return sm


GameApp().run()