from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window

# Login Screen
class LoginPage(App):
    def build(self):
        self.title = "Login Screen"
        Window.size = (500, 800)
        layout = GridLayout(cols=5, rows=20, padding=10, spacing=10, row_default_height=30)

        usernameinput = TextInput()
        passwordinput = TextInput(password=True)
        usernamelbl = Label(text="Username", size_hint_x=None, width=100)

        passwordlbl = Label(text="Password", size_hint_x=None, width=100)

        layout.add_widget(usernamelbl)
        layout.add_widget(usernameinput)
        layout.add_widget(passwordlbl)
        layout.add_widget(passwordinput)

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        main_layout.add_widget(layout)

        # login button
        loginbutton = Button(text="Login")
        loginbutton.bind(on_press=self.on_button_press)
        main_layout.add_widget(loginbutton)

        return main_layout

    def on_button_press(self, secondarg):
        app.stop()
        app2 = MainMenu()
        app2.run()


class MainMenu(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        self.solution = TextInput(multiline=False, readonly=True, halign="right", font_size=55)
        main_layout.add_widget(self.solution)
        button = Button(text="C",pos_hint={"center_x": 0.5, "center_y": 0.5},)
        button.bind(on_press=self.on_button_press)
        main_layout.add_widget(button)

        equals_button = Button(text="=", pos_hint={"center_x": 0.5, "center_y": 0.5})
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            # Clear the solution widget
            self.solution.text = ""
            #todo kill current app and launch journal
            app.stop()
            app2 = JournalPage()
            app2.run()

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            solution = str(eval(self.solution.text))
            self.solution.text = solution


class JournalPage(App):
    def build(self):
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None
        main_layout = BoxLayout(orientation="vertical")
        self.solution = TextInput(multiline=False, readonly=True, halign="right", font_size=55)
        main_layout.add_widget(self.solution)
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        equals_button = Button(
            text="=", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            # Clear the solution widget
            self.solution.text = ""
        else:
            if current and (
                self.last_was_operator and button_text in self.operators):
                # Don't add two operators right after each other
                return
            elif current == "" and button_text in self.operators:
                # First character cannot be an operator
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_solution(self):
        text = self.solution.text
        if text:
            solution = str(eval(self.solution.text))
            self.solution.text = solution

class TestPage(App):
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


if __name__ == "__main__":
    app = LoginPage()
    app.run()