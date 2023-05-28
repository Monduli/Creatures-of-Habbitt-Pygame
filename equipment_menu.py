from helpers import * 
import pygame as pyg
from OpenGL.GL import *
from OpenGL.GLU import *

class EquipmentMenu():

    def __init__(self, function):
        self.function = function

    def pull_function(self):
        if self.function == "ACC":
            # Load accessories list to create haberdash menu
            pass
        elif self.function == "WEP":
            # Load weapons list to create smithing menu
            pass
