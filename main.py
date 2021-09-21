import os

from threading import Thread
from time import sleep
os.environ['DISPLAY'] = ":0.0"
os.environ['KIVY_WINDOW'] = 'sdl2'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.uix.slider import Slider
from datetime import datetime
import pygame
from pidev.Joystick import Joystick
import spidev
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers


# kivy starting stuff
SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'


spi = spidev.SpiDev()

class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER

Window.clearcolor = (1, 1, 1, 1)  # White
btn_state = True


Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()