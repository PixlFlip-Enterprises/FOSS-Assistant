from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
import json
import sys
import requests

# api server
BASE = 'http://127.0.0.1:5000/'
API_KEY = '#2AJKLFHW9203NJFC'


class MainMenu(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        button = Button(text="Journal",pos_hint={"center_x": 0.5, "center_y": 0.5},)
        button.bind(on_press=self.on_journal_button_press)
        main_layout.add_widget(button)

        equals_button = Button(text="Profile", pos_hint={"center_x": 0.5, "center_y": 0.5})
        equals_button.bind(on_press=self.on_profile_button_press)
        main_layout.add_widget(equals_button)

        return main_layout

    def on_journal_button_press(self, instance):
        # kill current app and launch journal
        app.stop()
        app2 = JournalPage()
        app2.run()

    def on_profile_button_press(self, instance):
        # kill current app and launch journal
        app.stop()
        app2 = ProfilePage()
        app2.run()


class JournalPage(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        # entry text input
        self.entry = TextInput(multiline=False, readonly=False, halign="center", font_size=50)
        main_layout.add_widget(self.entry)
        # entry record button
        entry_button = Button(text="Record Entry", pos_hint={"center_x": 0.5, "center_y": 0.5}, )
        entry_button.bind(on_press=self.on_entry_button_press)
        main_layout.add_widget(entry_button)
        # back button
        back_button = Button(text="Back", pos_hint={"center_x": 0.5, "center_y": 0.5}, )
        back_button.bind(on_press=self.on_back_button_press)
        main_layout.add_widget(back_button)
        return main_layout

    def on_entry_button_press(self, instance):
        entry = self.entry.text
        # todo api call to save entry
        response = requests.put(BASE + "journal",
                                json={'session_token': API_KEY, 'date': '2022-07-16', 'entry': entry,
                                      'creation_device': 'Kivy Desktop Client', 'starred': 'false', 'time_zone': 'EST'})
        reply = response.json()
        print(reply['status'])
        app.stop()
        app2 = MainMenu()
        app2.run()

    def on_back_button_press(self, instance):
        app.stop()
        app2 = MainMenu()
        app2.run()

class ProfilePage(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        # set window size
        #self.window.size_hint = (0.6, 0.7)
        # set window place on screen
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        # create image widget
        background = Image(source="testbackground.jpg")
        # add image to window
        self.window.add_widget(background)
        # add widgets to window


        return self.window


class LoginPage(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        # username text input
        self.username = TextInput(multiline=False, readonly=False, halign="center", font_size=50)
        main_layout.add_widget(self.username)
        # password text input
        self.password = TextInput(multiline=False, readonly=False, halign="center", font_size=50)
        main_layout.add_widget(self.password)
        # login button
        button = Button(text="Login", pos_hint={"center_x": 0.5, "center_y": 0.5}, )
        button.bind(on_press=self.on_button_press)
        main_layout.add_widget(button)

        return main_layout

    def on_button_press(self, instance):
        usr = self.username.text
        pwd = self.password.text
        # todo later on make this retrieve from api. For now api key is hard coded so move to next screen
        print(usr + ' ' + pwd)
        app.stop()
        app2 = MainMenu()
        app2.run()



if __name__ == "__main__":
    app = LoginPage()
    app.run()