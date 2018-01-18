from kivy.app import App
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import AsyncImage


class BackButton(ButtonBehavior, AsyncImage):
    def on_release(self):
        pass