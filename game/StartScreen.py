import os
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
import webbrowser
import game


Config.set('graphics', 'width', '1600')
Config.set('graphics', 'height', '900')
Config.set('graphics', 'resizable', 0)
Config.write()


class StartScreen(FloatLayout, App):
    def __init__(self, root, **kwargs):
        FloatLayout.__init__(self)
        self.root = root
        self.back = AsyncImage(source=os.path.abspath(os.path.join('/assets/startscrback.jpg', os.pardir)))
        self.back.allow_stretch = True
        self.back.keep_ratio = False
        self.add_widget(self.back)
        self.gamenametv = Label(text='SOS!',font_size=100,pos_hint={'center_x': .5, 'center_y': .9}, color=(0,0,0,1))
        self.start_btn = Builder.load_string('''
Button:
    text: 'Start game'
    size_hint: .15, .1
    pos_hint: {'center_x': .5, 'center_y': .5}
    on_release: app.two_player_popup()
''')
        self.ai_start_btn = Builder.load_string('''
Button:
    text: 'Start game againt the computer'
    size_hint: .15, .1
    pos_hint: {'center_x': .5, 'center_y': .375}
    on_release: app.ai_popup()        
''')
        self.exit_btn = Builder.load_string('''
Button:
    text: 'Exit'
    size_hint: .15, .1
    pos_hint: {'center_x': .5, 'center_y': .25}
    on_release: app.on_exit()
''')
        '''
        self.mygithub = MyGithubBtn(pos_hint={'center_x': .9, 'center_y': .1},
                                       size_hint=(.1, .1),
                                       source=self.root.abspath('assets/github.png'),
                                       on_release=lambda x:webbrowser.open('https://github.com/realKfiros'))
        self.add_widget(self.mygithub)
        '''
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


    def build(self):
        return self

    def on_start_pressed(self):
        self.remove_widget(self.name1instruction)
        self.remove_widget(self.name1input)
        self.remove_widget(self.name2instruction)
        self.remove_widget(self.name2input)
        self.remove_widget(self.startbtn)
        game.SOSApp(self.root, self.name1input.text, self.name2input.text).run()

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


class MyGithubBtn(ButtonBehavior, AsyncImage):
    def on_release(self):
        webbrowser.open('https://github.com/realKfiros')