from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import requests
import json

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        self.title = MDLabel(text="CWO Transport App", halign='center', font_style='H4')
        self.layout.add_widget(self.title)

        self.code_input = MDTextField(hint_text="Enter Access Code", mode="rectangle")
        self.layout.add_widget(self.code_input)

        self.login_btn = MDRaisedButton(text="Login", on_release=self.login)
        self.layout.add_widget(self.login_btn)

        self.add_widget(self.layout)

    def login(self, instance):
        code = self.code_input.text
        if code == "secret123":  # Replace with actual validation
            self.manager.current = 'menu'
        else:
            self.show_error("Invalid access code")

    def show_error(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[MDFlatButton(text="OK")]
        )
        dialog.open()

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        self.toolbar = MDTopAppBar(title="CWO Transport")
        self.toolbar.left_action_items = [["menu", lambda x: self.show_menu()]]
        self.layout.add_widget(self.toolbar)

        self.menu_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        self.conducteurs_btn = MDRaisedButton(text="Conducteurs", on_release=self.show_conducteurs)
        self.menu_layout.add_widget(self.conducteurs_btn)

        self.investisseurs_btn = MDRaisedButton(text="Investisseurs", on_release=self.show_investisseurs)
        self.menu_layout.add_widget(self.investisseurs_btn)

        self.admin_btn = MDRaisedButton(text="Administration", on_release=self.show_admin)
        self.menu_layout.add_widget(self.admin_btn)

        self.layout.add_widget(self.menu_layout)
        self.add_widget(self.layout)

    def show_menu(self):
        pass  # Implement menu drawer if needed

    def show_conducteurs(self, instance):
        self.manager.current = 'conducteurs'

    def show_investisseurs(self, instance):
        self.manager.current = 'investisseurs'

    def show_admin(self, instance):
        self.manager.current = 'admin'

class ConducteursScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        self.toolbar = MDTopAppBar(title="Conducteurs")
        self.toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        self.layout.add_widget(self.toolbar)

        self.scroll = ScrollView()
        self.list_layout = MDList()
        self.scroll.add_widget(self.list_layout)
        self.layout.add_widget(self.scroll)

        self.add_widget(self.layout)
        self.load_data()

    def go_back(self):
        self.manager.current = 'menu'

    def load_data(self):
        try:
            response = requests.get('http://localhost:5000/api/conducteurs', verify=False)
            if response.status_code == 200:
                conducteurs = response.json()
                for c in conducteurs:
                    item = OneLineListItem(text=f"{c['nom']} - {c['gain']}€ - {c['miles']} miles")
                    self.list_layout.add_widget(item)
            else:
                item = OneLineListItem(text="Failed to load data")
                self.list_layout.add_widget(item)
        except Exception as e:
            item = OneLineListItem(text=f"Error: {str(e)}")
            self.list_layout.add_widget(item)

class InvestisseursScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        self.toolbar = MDTopAppBar(title="Investisseurs")
        self.toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        self.layout.add_widget(self.toolbar)

        self.scroll = ScrollView()
        self.list_layout = MDList()
        self.scroll.add_widget(self.list_layout)
        self.layout.add_widget(self.scroll)

        self.add_widget(self.layout)
        self.load_data()

    def go_back(self):
        self.manager.current = 'menu'

    def load_data(self):
        try:
            response = requests.get('http://localhost:5000/api/investisseurs', verify=False)
            if response.status_code == 200:
                investisseurs = response.json()
                for i in investisseurs:
                    item = OneLineListItem(text=f"{i['nom']} - {i['montant']}€")
                    self.list_layout.add_widget(item)
            else:
                item = OneLineListItem(text="Failed to load data")
                self.list_layout.add_widget(item)
        except Exception as e:
            item = OneLineListItem(text=f"Error: {str(e)}")
            self.list_layout.add_widget(item)

class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        self.toolbar = MDTopAppBar(title="Administration")
        self.toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        self.layout.add_widget(self.toolbar)

        self.admin_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        self.add_conducteur_btn = MDRaisedButton(text="Add Conducteur", on_release=self.add_conducteur)
        self.admin_layout.add_widget(self.add_conducteur_btn)

        self.add_investisseur_btn = MDRaisedButton(text="Add Investisseur", on_release=self.add_investisseur)
        self.admin_layout.add_widget(self.add_investisseur_btn)

        self.layout.add_widget(self.admin_layout)
        self.add_widget(self.layout)

    def go_back(self):
        self.manager.current = 'menu'

    def add_conducteur(self, instance):
        # Implement add conducteur functionality
        pass

    def add_investisseur(self, instance):
        # Implement add investisseur functionality
        pass

class TransportApp(MDApp):
    def build(self):
        self.title = "CWO"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ConducteursScreen(name='conducteurs'))
        sm.add_widget(InvestisseursScreen(name='investisseurs'))
        sm.add_widget(AdminScreen(name='admin'))

        return sm

if __name__ == '__main__':
    TransportApp().run()
