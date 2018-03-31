import os
import platform
import webbrowser
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.app import App
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
import sos

if platform.system() == 'Linux':
    Config.set('graphics', 'width', '1600')
    Config.set('graphics', 'height', '900')
    Config.set('graphics', 'resiable', 0)
else:
    Config.set('graphics', 'fullscreen', 'auto')
Config.write()


class SOS(FloatLayout, App):
    """
    The class for the SOS game start screen
    """
    def __init__(self, **kwargs):
        """
        The constructor.
        """
        FloatLayout.__init__(self)
        self.back = AsyncImage(source=os.path.abspath('assets/startscrback.jpg'))
        self.back.allow_stretch = True
        self.back.keep_ratio = False
        self.add_widget(self.back)
        self.me = Label(text='@realKfiros',
                        font_size=50,
                        pos_hint={'center_x': .91, 'center_y': .05},
                        color=(0.207, 0.635, 0.423, 0.9))
        self.gamenametv = Label(text='SOS!',
                                font_size=100,
                                pos_hint={'center_x': .5, 'center_y': .9},
                                color=(0, 0, 0, 1))
        self.start_btn = Button(text='2 players game',
                                size_hint=(.15, .1),
                                pos_hint={'center_x': .5, 'center_y': .5},
                                on_release=lambda x: self.two_player_popup())
        self.ai_start_btn = Button(text='Game against the computer',
                                size_hint=(.15, .1),
                                pos_hint={'center_x': .5, 'center_y': .375},
                                on_release=lambda x: self.ai_popup())
        self.exit_btn = Button(text='Exit',
                                size_hint=(.15, .1),
                                pos_hint={'center_x': .5, 'center_y': .25},
                                on_release=lambda x: self.on_exit())
        self.add_widget(self.me)
        self.add_widget(self.gamenametv)
        self.add_widget(self.start_btn)
        self.add_widget(self.ai_start_btn)
        self.add_widget(self.exit_btn)
        self.edition = DropDown()
        self.classic = Button(text='Classic edition', size_hint_y=None, height=20, width=70)
        self.classic.bind(on_release=lambda x:self.getclassic())
        self.edition.add_widget(self.classic)
        self.notclassic = Button(text='Not classic edition', size_hint_y=None, height=20, width=70)
        self.notclassic.bind(on_release=lambda x:self.getnotclassic())
        self.edition.add_widget(self.notclassic)
        self.eastereggbtn = Button(text='', size_hint=(.1, .1), pos_hint={'center_x': .9, 'center_y': .9}, background_color = (0, 0, 0, 0))
        self.eastereggbtn.bind(on_release=self.edition.open)
        self.edition.bind(on_select=lambda instance, x:setattr(self.eastereggbtn, '', x))
        self.add_widget(self.eastereggbtn)
        self.rules_btn = Button(text='Rules',
                                size_hint=(.1, .1),
                                pos_hint={'center_x': .1, 'center_y': .9},
                                on_release=self.rules)
        self.popup_content = BoxLayout(orientation = 'vertical')
        self.creategamecontent = CreateGameLayout()
        self.start = Button(text='Start game!!!',
                            size_hint=(None, None),
                            size=(552,100),
                            on_release=self.on_start_pressed)
        self.popup_content.add_widget(self.creategamecontent)
        self.creategamecontent.player1.size_hint = (None, None)
        self.creategamecontent.player1.size = (552,50)
        self.creategamecontent.player2.size_hint = (None, None)
        self.creategamecontent.player2.size = (552, 50)
        self.popup_content.add_widget(self.start)
        self.creategamepopup = Popup(title='Start a game!',
                                     content=self.popup_content,
                                     size_hint=(None, None),
                                     size=(600,325))
        self.add_widget(self.rules_btn)
        self.fire = AsyncImage(source=os.path.abspath('assets/fire.gif'), pos_hint={'center_x': .5, 'center_y': .5})
        self.black = True
        self.game = 0

    def getclassic(self):
        """
        :return: classic theme of the game
        """
        self.back.source = os.path.abspath('assets/startscrback.jpg')
        self.black = True
        self.gamenametv.color = (0, 0, 0, 1)

    def getnotclassic(self):
        """
        :return: The Beatles w/ Patrick Starr theme of the game
        """
        self.back.source = os.path.abspath('assets/startscrback01.jpg')
        self.black = False
        self.gamenametv.color = (1, 1, 1, 1)

    def rules(self, instance):
        """
        :param instance: for the on_release/on_click function
        :return: opens the default browser and shows the html file with the rules
        """
        path = os.path.abspath('gamedocs/site/index.html')
        webbrowser.open('file://{path}'.format(**locals()))

    def build(self):
        """
        :return: builds the graphic screen
        """
        return self

    def on_start_pressed(self, instance):
        """
        called when the button in the popup is pressed
        :param instance: for the on_release/on_click function
        :return: starts the game, applying the settings from the popup
        """
        self.remove_widget(self.gamenametv)
        self.remove_widget(self.start_btn)
        self.remove_widget(self.ai_start_btn)
        self.remove_widget(self.exit_btn)
        self.remove_widget(self.rules_btn)
        self.game = sos.Game(self.root, self.creategamecontent.name1input.text, self.creategamecontent.name2input.text, self.black, self.creategamecontent.n, self.creategamecontent.n)
        self.creategamepopup.dismiss()
        self.add_widget(self.game)

    def two_player_popup(self):
        """
        :return: opens a game creation popup
        """
        self.creategamepopup.open()

    def ai_popup(self):
        """
        :return: opens a game creation popup, but with the second player called CPU, which means that the game is against the computer
        """
        self.creategamecontent.name2input.text = 'CPU'
        self.creategamecontent.name2input.disabled = True
        self.creategamepopup.open()

    def on_exit(self):
        """
        :return: exits the graphics and stops the program
        """
        exit()


class CreateGameLayout(BoxLayout):
    """
    The class for the game creation popup
    """
    def __init__(self, **kwargs):
        """
        the constructor.
        """
        BoxLayout.__init__(self)
        self.orientation = 'vertical'
        self.n = 9
        self.player1 = BoxLayout(orientation='horizontal')
        self.player2 = BoxLayout(orientation='horizontal')
        self.name1instruction = Label(text='Type player 1 name: ',
                                      font_size=25,
                                      color=(1, 1, 1, 1))
        self.name1input = TextInput(multiline=False)
        self.player1.add_widget(self.name1instruction)
        self.player1.add_widget(self.name1input)
        self.add_widget(self.player1)
        self.name2instruction = Label(text='Type player 2 name: ',
                                      font_size=25,
                                      color=(1, 1, 1, 1))
        self.name2input = TextInput(multiline=False)
        self.player2.add_widget(self.name2instruction)
        self.player2.add_widget(self.name2input)
        self.add_widget(self.player2)


if __name__ == '__main__':
    g = SOS()
    g.run()