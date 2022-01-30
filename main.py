import glob
import random
from pathlib import Path
from kivy.app import App
from kivy.app import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from  datetime import datetime
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('design.kv')


class LoginScreen(Screen):

    def sign_up(self):
        self.manager.transition.direction = "left"
        self.manager.current = "sign_up_screen"

    def login(self, uname, pword):
        with open('users.json') as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = 'login_screen_success'
        else:
            self.ids.login_wrong.text = "Wrong username and / or password"

    def forgot_pwd(self):
        self.manager.transition.direction = "left"
        self.manager.current = "forgot_pwd_screen"


class RootWidget(ScreenManager):
    pass


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def display_quote(self, feel):
        feel = feel.lower()
        feel_files = glob.glob("quotes/*txt")
        feel_files = [Path(filename).stem for filename in feel_files]
        if feel in feel_files:
            with open(f"quotes/{feel}.txt", encoding='utf-8') as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname,pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pword,
        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"


class SignUpSuccess(Screen):
    def go_login_screen(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class Forgot_pwd_Screen(Screen):
    def reset_pwd(self, uname, n_pwd):
        with open("users.json") as file:
            users = json.load(file)
        users[uname] = {'username': uname, 'password': n_pwd,
                        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "login_screen"


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()