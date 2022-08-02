from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import json
import sys
import requests

# api server
BASE = 'http://192.168.19.139:5000/'
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
        Window.size = (500, 800)
        # returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 1)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        # image widget
        self.window.add_widget(Image(source="logo.png"))

        # label widget
        self.user_label = Label(text= "Username", font_size= 18, color= '#43ccc5')
        self.window.add_widget(self.user_label)

        # text input widget
        self.user = TextInput(multiline=False, padding_y=(20, 20), size_hint=(1, 0.6))
        self.window.add_widget(self.user)

        # label widget
        self.pass_label = Label(text="Password", font_size=18, color='#43ccc5')
        self.window.add_widget(self.pass_label)

        # text input widget
        self.pwd = TextInput(multiline=False, padding_y=(20, 20), size_hint=(1, 0.6))
        self.window.add_widget(self.pwd)

        # label as a spacer
        self.s_label = Label(text=" ", font_size=18, color='#43ccc5')
        self.window.add_widget(self.s_label)

        # button widget
        self.button = Button(text="Login", size_hint=(0.6,0.6), bold=True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)

        return self.window

    def callback(self, instance):
        usr = self.user.text
        pwd = self.pwd.text
        # todo later on make this retrieve from api. For now api key is hard coded so move to next screen
        print(usr + ' ' + pwd)
        app.stop()
        app2 = MainMenu()
        app2.run()


if __name__ == "__main__":
    app = LoginPage()
    app.run()