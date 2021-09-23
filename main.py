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
from kivy.core.window import Window
Window.fullscreen = True
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus


# kivy starting stuff
SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'


spi = spidev.SpiDev()

def up(status): # turns magnet on or off
    if not status:
        cyprus.set_pwm_values(1, period_value=100000, compare_value=50000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)

    else:
        cyprus.set_pwm_values(1, period_value=100000, compare_value=0,
                              compare_mode=cyprus.LESS_THAN_OR_EQUAL)  # Motor OFF



def magon(status): # turns magnet on or off
    if status:
        cyprus.set_servo_position(2, 1)

    else:
        cyprus.set_servo_position(2, 0.5)


s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
                     steps_per_unit=200, speed=8)
class MainScreen(Screen):

    magstat = False #status of the magnet
    opfreeze = False
    ifup = True
    position = 1
    """
    Class to handle the main screen and its associated touch events
    """
    def start(self):
        print("******************************************starting******************************************************")

        cyprus.initialize()
        cyprus.setup_servo(1)  # sets up P4 on the RPiMIB as a RC servo style output
        cyprus.setup_servo(2)  # sets up P5 on the RPiMIB as a RC servo motor controller style output


        print("homing")
        s0.go_until_press(0, 6400)
        s0.set_as_home()

        sleep(3)

        Thread(target=self.operation_thread).start()


    def operation_thread(self):
        s0.relative_move(1)

        while True:
            sleep(.01)
            self.position = s0.get_position()
            self.pos_label.text = str(self.position)
            if not self.opfreeze:

                magon(self.magstat)
                up(self.ifup)

                if self.leftbtn.state == "down":
                    s0.go_until_press(0, 2000)
                elif self.rightbtn.state == "down":
                    s0.go_until_press(1, 2000)
                else:
                    s0.softStop()

            else:
                sleep(.5)

    def autobeepboop(self):
        self.opfreeze = True
        print("beepboop")

        if not (cyprus.read_gpio() & 0b0001) == 1:  # binary bitwise AND of the value returned from read.gpio()

            up(True)
            s0.goTo(7394)
            up(False)
            sleep(3)
            magon((True))
            up(True)
            sleep(2)
            s0.goTo(9350)
            sleep(1.5)
            up(False)
            sleep(1.5)
            magon((False))
            up(True)
        else:
            up(True)
            s0.goTo(9350)
            up(False)
            sleep(1.5)
            magon((True))
            up(True)
            sleep(2)
            s0.goTo(7394)
            sleep(.5)
            up(False)
            sleep(3)
            magon((False))
            up(True)

        self.opfreeze = False

    def autobeepboopbeep(self):
        print("beepboopbeep")
        self.opfreeze = True
        s0.goHome()
        s0.relative_move(-5)
        sleep(.1)
        self.magstat = False
        sleep(1)
        s0.relative_move(5)
        magon(False)
        self.opfreeze = False

    def magnet(self):
        if self.magnet_button.text == "magnet on":
            self.magnet_button.text = "magnet off"
            self.magstat = False

        else:
            self.magnet_button.text = "magnet on"
            self.magstat = True


    def updown(self):
        self.ifup = not self.ifup
        if self.ifup:
            self.upbtn.text = "Up"
        else:
            self.upbtn.text = "Down"

    def shutdown(self):
        self.magstat = False  # status of the magnet
        self.opfreeze = False
        self.ifup = True
        magon(False)
        up(True)
        s0.goTo(0)
        s0.free_all()
        spi.close()
        cyprus.close()
        GPIO.cleanup()

        exit(12)


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