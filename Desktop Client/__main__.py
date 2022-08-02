from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
import json
import sys
import requests

# api server
BASE = 'http://192.168.19.139:5000/'
API_KEY = '#2AJKLFHW9203NJFC'


class MainMenu(App):
    def build(self):
        Window.size = (500, 800)
        # returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 1)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # image widget
        self.window.add_widget(Image(source="logo.png"))

        # label as a spacer
        self.s_label2 = Label(text=" ", font_size=10, color='#43ccc5')
        self.window.add_widget(self.s_label2)

        # button widget
        self.button = Button(text="Journal", size_hint=(0.2, 0.2), bold=True,
                             background_color='#43CCC5',
                             background_normal="#43CCC5"
                             )
        self.button.bind(on_press=self.on_journal_button_press)
        self.window.add_widget(self.button)

        # label as a spacer
        self.s_label3 = Label(text=" ", font_size=10, color='#43ccc5')
        self.window.add_widget(self.s_label3)

        # button widget
        self.profile_button = Button(text="Profile", size_hint=(0.2, 0.2), bold=True,
                             background_color='#43CCC5',
                             background_normal="#43CCC5"
                             )
        self.profile_button.bind(on_press=self.on_profile_button_press)
        self.window.add_widget(self.profile_button)

        # label as a spacer
        self.s_label4 = Label(text=" ", font_size=10, color='#43ccc5')
        self.window.add_widget(self.s_label4)

        # button widget
        self.contact_manager_button = Button(text="Contacts", size_hint=(0.2, 0.2), bold=True,
                                     background_color='#43CCC5',
                                     background_normal="#43CCC5"
                                     )
        self.contact_manager_button.bind(on_press=self.on_contact_manager_button_press)
        self.window.add_widget(self.contact_manager_button)

        # label as a spacer
        self.s_label5 = Label(text=" ", font_size=10, color='#43ccc5')
        self.window.add_widget(self.s_label5)

        return self.window

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

    def on_contact_manager_button_press(self, instance):
        # kill current app and launch journal
        app.stop()
        app2 = ContactManagerPage()
        app2.run()


class JournalPage(App):
    def build(self):
        Window.size = (500, 800)
        # returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 1)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # label widget
        self.user_label = Label(text="Journal", font_size=40, color='#43ccc5', bold=True)
        self.window.add_widget(self.user_label)

        # entry text input
        self.entry = TextInput(multiline=True, readonly=False, halign="center", font_size=30)
        self.window.add_widget(self.entry)

        # TODO To make a more detailed area using Kivy you just can create another grid and add it back as a widget. Mind blown
        self.subgrid = GridLayout()
        self.subgrid.cols = 2
        # Add checkbox, Label and Widget
        self.subgrid.add_widget(Label(text='Favorite:', font_size=20, color='#43ccc5'))
        self.starred = CheckBox(active=False)
        self.subgrid.add_widget(self.starred)
        self.subgrid.add_widget(Label(text='Conceal Device ID:', font_size=20, color='#43ccc5'))
        self.creation_device = CheckBox(active=False)
        self.subgrid.add_widget(self.creation_device)
        self.window.add_widget(self.subgrid)


        # entry record button
        self.entry_button = Button(text="Record Entry", size_hint=(0.2, 0.2), bold=True,
                             background_color='#43CCC5',
                             background_normal="#43CCC5"
                             )
        self.entry_button.bind(on_press=self.on_entry_button_press)
        self.window.add_widget(self.entry_button)

        # label as a spacer
        self.s_label = Label(text=" ", font_size=10, color='#43ccc5')
        self.window.add_widget(self.s_label)

        # back button
        self.back_button = Button(text="Back", size_hint=(0.2, 0.2), bold=True,
                                   background_color='#43CCC5',
                                   background_normal="#43CCC5"
                                   )
        self.back_button.bind(on_press=self.on_back_button_press)
        self.window.add_widget(self.back_button)


        return self.window

    def on_entry_button_press(self, instance):
        entry = self.entry.text
        # todo api call to save entry
        # todo use try catch for error handling (because believe you me it will throw errors until I fix api calls)
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


class ContactManagerPage(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        # set window size
        #self.window.size_hint = (0.6, 0.7)
        # set window place on screen
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
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
                      background_color ='#43CCC5',
                      background_normal = "#43CCC5"
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