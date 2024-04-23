'''
Purpose: To create widgets for the GUI
Usage: for ROV_main.py
'''

import pygame

'''Class for Toggleable Widgets'''
class toggleable:
    def __init__(self,name,width):
        self.name = name
        self.width = width
        self.myfont = pygame.font.SysFont(None,16)
        self.state = False 

    def render(self):
        if self.state:
            text = self.myfont.render(self.name + ": On", True, (0,0,0)) #(0,0,0) is black
        else:
            text = self.myfont.render(self.name + ": Off", True, (0,0,0))
        background  =  pygame.Surface((self.width, text.get_height()))
        background.fill(((not self.state) *150, self.state *150,0)) #background color is green if state is true, red if state is false
        background.blit(text, (0,0))
        return background

    def get_height(self):
        return self.myfont.get_height()

    def toggle(self):
        self.state = not self.state

    def enable(self):
        self.state = True

    def disable(self):
        self.state = False

'''Class for displaying values'''
class display: 
    def __init__(self,name,width):
        self.name = name
        self.width = width
        self.myfont = pygame.font.SysFont(None, 16)
        self.value = 0
        self.bgcolor = (255,255,255) #(255,255,255) is white
       
    def render(self):
        text = self.myfont.render(self.name+": "+ str(self.value),True, (0,0,0))
        background = pygame.Surface((self.width,text.get_height()))
        background.fill(self.bgcolor)
        background.blit(text,(0,0))
        return background

    def get_height(self):
        return self.myfont.get_height()

    def setValue(self, value):
        self.value = value
        
'''Class for displaying sliders'''
class sliderdisplay:
    def __init__(self,name,width,height):
        self.name = name
        self.width = width
        self.height = height
        self.value = 0
        self.myfont = pygame.font.SysFont(None, 16)

    def render(self):
        bar = pygame.Surface((self.width,self.height))
        bar.fill((230,230,230)) #display background color is light gray
      
        if self.value < 0:
            bar.fill((70,70,240), (0,self.height*.5,self.width,-self.value*self.height*.5)) #(70,70,240) is blue
        else:
            bar.fill((70,70,240),(0,(1-self.value)*self.height*.5,self.width,self.value*self.height*.5))

        for i in range(1,10): #draws tick marks
            pygame.draw.line(bar,(89, 174, 240),(0,self.height*i*.1),(self.width*.25, self.height*i*.1)) #(89,174,240) is light blue
            pygame.draw.rect(bar, (89, 174, 240),pygame.Rect(0, 0, self.width,self.height),2) #draws border

        label  =  400
        for j in range(1, 10): #draws labels
            text  =  self.myfont.render(str(label), True, (0, 0, 0))
            bar.blit(text, (2, self.height * j * .1 - 13.5))
            label  =  label - 100
        return bar