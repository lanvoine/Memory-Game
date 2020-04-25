from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.uix.label import Label

# Creation of the Game Cards
class Card:
    def __init__(self, value, gamemanager):
        self.gamemanager = gamemanager
        self.value = value

        # Layout of Card
        self.layout = BoxLayout()
        self.btn = Button(background_normal = ('cardimage.png'), text = '', font_size = 36)
        self.btn.on_press = self.onClick
        self.lbl = Label(text = '{}'.format(value), font_size = 36)

        # Display button first
        self.layout.add_widget(self.btn)

    # A function to 'Flip' the card over once it is clicked
    def onClick(self, instance=None):
        if self.gamemanager.can_open():
            self.layout.remove_widget(self.btn)
            self.layout.add_widget(self.lbl)
            self.gamemanager.card_check(self)

    # A function to 'Flip' the card back if the player matches the cards wrongly 
    def close(self):
        self.layout.remove_widget(self.lbl)
        self.layout.add_widget(self.btn)