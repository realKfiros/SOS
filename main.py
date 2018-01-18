import os
import platform
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.app import App
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from game.game import Game
from assets.buttons.back import BackButton
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup


if platform.system() == 'Linux':
    Config.set('graphics', 'width', '1600')
    Config.set('graphics', 'height', '900')
    Config.set('graphics', 'resiable', 0)
else:
    Config.set('graphics', 'fullscreen', 'auto')
Config.write()


class SOS(FloatLayout, App):
    def __init__(self, **kwargs):
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
        self.name1instruction = Label(text='Type player 1 name: ',
                                      pos_hint={'center_x': .5, 'center_y': .75},
                                      font_size=25,
                                      color=(0,0,0,1))
        self.name1input = TextInput(pos_hint={'center_x': .5, 'center_y': .7},
                                    size_hint=(.2, .03),
                                    multiline=False)
        self.name2instruction = Label(text='Type player 2 name: ',
                                      pos_hint={'center_x': .5, 'center_y': .6},
                                      font_size=25,
                                      color=(0, 0, 0, 1))
        self.name2input = TextInput(pos_hint={'center_x': .5, 'center_y': .55},
                                    size_hint=(.2, .03),
                                    multiline=False)
        self.aiplayerinstruction = Label(text='Type player name: ',
                                      pos_hint={'center_x': .5, 'center_y': .75},
                                      font_size=25,
                                      color=(0, 0, 0, 1))
        self.aiplayerinput = TextInput(pos_hint={'center_x': .5, 'center_y': .7},
                                    size_hint=(.2, .03),
                                    multiline=False)
        self.startbtn = Button(text='Start game!',
                               font_size=25,
                               size_hint=(.15, .1),
                               pos_hint={'center_x': .5, 'center_y': .4},
                               on_release=lambda x:self.on_start_pressed())
        self.backbtn = BackButton(source=os.path.abspath('assets/buttons/back.png'),
                                      size_hint=(.05, .05),
                                      pos_hint={'center_x': .9, 'center_y': .9})
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
        self.secretpopup = Popup(title='The secret of this easy game',
                                 content=Label(text='Force your rival'),
                                 size_hint=(None, None),
                                 size=(400, 400))
        self.winningsecret = Button(text='',
                                size_hint=(.1, .1),
                                pos_hint={'center_x': .1, 'center_y': .9},
                                background_color=(0, 0, 0, 0),
                                on_release=lambda x: self.secretpopup.open())
        self.add_widget(self.winningsecret)
        self.fire = AsyncImage(source=os.path.abspath('assets/fire.gif'), pos_hint={'center_x': .5, 'center_y': .5})
        self.black = True
        self.game = 0


    def getclassic(self):
        self.back.source = os.path.abspath('assets/startscrback.jpg')
        self.black = True
        self.gamenametv.color = (0, 0, 0, 1)
        self.name1instruction.color = (0, 0, 0, 1)
        self.name2instruction.color = (0, 0, 0, 1)
        self.aiplayerinstruction.color = (0, 0, 0, 1)

    def getnotclassic(self):
        self.back.source = os.path.abspath('assets/startscrback01.jpg')
        self.black = False
        self.gamenametv.color = (1, 1, 1, 1)
        self.name1instruction.color = (1, 1, 1, 1)
        self.name2instruction.color = (1, 1, 1, 1)
        self.aiplayerinstruction.color = (1, 1, 1, 1)

    def build(self):
        return self

    def on_start_pressed(self):
        self.remove_widget(self.name1instruction)
        self.remove_widget(self.name1input)
        self.remove_widget(self.name2instruction)
        self.remove_widget(self.name2input)
        self.remove_widget(self.startbtn)
        self.game = Game(self.root, self.name1input.text, self.name2input.text, self.black)
        self.add_widget(self.game)

    def two_player_popup(self):
        self.remove_widget(self.gamenametv)
        self.remove_widget(self.start_btn)
        self.remove_widget(self.ai_start_btn)
        self.remove_widget(self.exit_btn)
        self.add_widget(self.name1instruction)
        self.add_widget(self.name1input)
        self.add_widget(self.name2instruction)
        self.add_widget(self.name2input)
        self.add_widget(self.startbtn)
        self.add_widget(self.backbtn)

    def ai_popup(self):
        self.name2input.text = 'CPU'
        self.remove_widget(self.gamenametv)
        self.remove_widget(self.start_btn)
        self.remove_widget(self.ai_start_btn)
        self.remove_widget(self.exit_btn)
        self.add_widget(self.name1instruction)
        self.add_widget(self.name1input)
        self.add_widget(self.startbtn)
        self.name1instruction.text = 'Type player name: '

    def on_exit(self):
        exit()


if __name__ == '__main__':
    g = SOS()
    g.run()