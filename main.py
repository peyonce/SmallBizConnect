import os

from kivy.config import Config
Config.set("graphics", "width",  "500")
Config.set("graphics", "height", "900")

ASSETS = os.path.join(os.path.dirname(__file__), "assets")
Config.set("kivy", "window_icon", os.path.join(ASSETS, "logo.png"))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.text import LabelBase

from data import BusinessData
from screen import WelcomeScreen, DashboardScreen, HistoryScreen, ToolsScreen

LabelBase.register(
    name="Poppins",
    fn_regular=os.path.join(ASSETS, "Poppins-Regular.ttf"),
    fn_bold=os.path.join(ASSETS, "Poppins-Bold.ttf"),
)

class SmallBizConnectApp(App):
    def build(self):
        self.title = "SmallBizConnect"

        manager = ScreenManager()
        manager.business_data = BusinessData()

        manager.add_widget(WelcomeScreen(name="welcome"))
        manager.add_widget(DashboardScreen(name="dashboard"))
        manager.add_widget(HistoryScreen(name="history"))
        manager.add_widget(ToolsScreen(name="tools"))

        manager.current = "welcome"
        return manager

if __name__ == "__main__":
    SmallBizConnectApp().run()
