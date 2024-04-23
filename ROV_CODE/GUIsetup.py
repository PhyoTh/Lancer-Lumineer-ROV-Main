'''
Purpose: To create a GUI for the ROV control system
Usage: for ROV_main.py
'''
import widgets2 as widgets
import pygame

class GUI:
    def __init__(self, sideBarWidth, height, size):
        self.sideBarWidth = sideBarWidth
        self.height = height
        self.size = size
        
    def render(self):
        pygame.display.set_caption('ROV Control')
        screen = pygame.display.set_mode(self.size, pygame.SCALED)
        screen.fill((16, 43, 87)) #Background: (16, 43, 87) is a dark blue color
        guiScreen = pygame.Surface((80 + self.sideBarWidth, self.height), pygame.SRCALPHA) #SRCALPHA allows for transparency
        guiScreen.fill((0, 0, 0, 0)) #(0, 0, 0, guiTransparency) is black with transparency
        
    def create_widgets(self, sideBarWidth):
        onStatus = widgets.toggleable("Thrusters-Turbo Mode", sideBarWidth)
        volt_display = widgets.display("Voltage (V)", sideBarWidth)
        temp_display = widgets.display("Temp (C)", sideBarWidth)
        th_up_left_display = widgets.display("Servo Up (Left)", sideBarWidth)
        th_up_right_display = widgets.display("Servo Up (Right)", sideBarWidth)
        th_left_display = widgets.display("Servo Left", sideBarWidth)
        th_right_display = widgets.display("Servo Right", sideBarWidth)
        claw_display = widgets.display("Main Claw Value", sideBarWidth)
        claw_rotate_display = widgets.display("Claw rotate Value", sideBarWidth)