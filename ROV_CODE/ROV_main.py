import widgets2 as widgets
import JoyStick_constants as JoyStick

import pygame
import math
import json #to convert python dictionary to json format
import serial #to communicate with Arduino Mega Board

'''---DEBUGGING purpose---'''
DEBUG = False

'''---Display purpose: window (16:9) and mac (16:10) have different screen ratios---'''
WINDOW = False #if running on Windows, set to True
MAC = True  #if running on Mac, set to True

'''---DISPLAY CONSTANTS---'''
# Constants for Pygame Window
sideBarWidth = 300
if WINDOW:
    size = width, height = 980 + sideBarWidth, 720 #1280 x 720
    fps = 60 #60fps
elif MAC:
    size = width, height = 980 + sideBarWidth, 800 #1280 x 800
    fps = 240 #240fps ( mac is better:> )

'''---SETUPs---'''
# Open serial port to communicate with Arduino Mega Board
# note: change the port according to where you plugged in the Arduino Mega Board
try:
    ser = serial.Serial(port='/dev/cu.usbmodem21201', baudrate=9600, timeout=.1, dsrdtr=True) #dsrdtr=True stops Arduino Mega from auto resetting
except serial.SerialException:
    print("ROV is not connected")
    quit()

# Joystick setup
pygame.init()
pygame.joystick.init()
assert pygame.joystick.get_count() != 0, "No joystick detected"
joystick = pygame.joystick.Joystick(0) #initialize joystick to the first available controller (index 0)
joystick.init()

# Create the drawing window
pygame.display.set_caption('ROV Control')
screen = pygame.display.set_mode(size, pygame.SCALED)
screen.fill((16, 43, 87)) #Background: (16, 43, 87) is a dark blue color

# GUI setup
guiScreen = pygame.Surface((80 + sideBarWidth, height), pygame.SRCALPHA) #SRCALPHA allows for transparency
guiTransparency = 0
guiScreen.fill((0, 0, 0, guiTransparency)) #(0, 0, 0, guiTransparency) is black with transparency

onStatus = widgets.toggleable("Thrusters-Turbo Mode", sideBarWidth)
temp_display = widgets.display("Temp (C)", sideBarWidth)
th_up_display = widgets.display("Servo Up", sideBarWidth)
th_left_display = widgets.display("Servo Left", sideBarWidth)
th_right_display = widgets.display("Servo Right", sideBarWidth)
claw_display = widgets.display("Main Claw Value", sideBarWidth)
claw_rotate_display = widgets.display("Claw rotate Value", sideBarWidth)

zSlider = widgets.sliderdisplay("Z", 100, 320)
mLeftSlider = widgets.sliderdisplay("LeftSlider", 100, 320)
mRightSlider = widgets.sliderdisplay("RightSlider", 100, 320)

# Text setup
font = pygame.font.SysFont(None, 16)
leftText = font.render("Left", True, (255, 255, 255))
rightText = font.render("Right", True, (255, 255, 255))
ZAxisText = font.render("Z-axis", True, (255, 255, 255))

# User Controls setup
Controls = font.render("User Controls: ", True, (255, 255, 255)) 
left_button = font.render("LB: Close Claw", True, (255, 255, 255))
right_button = font.render("RB: Open Claw", True, (255, 255, 255))
button_A = font.render("A: Toggle Max Thrust", True, (255, 255, 255))
LF_Joy_Up = font.render("Left Joy Up: Forward", True, (255, 255, 255))
LF_Joy_Down = font.render("Left Joy Down: Reverse", True, (255, 255, 255))
LF_Joy_Left = font.render("Left Joy Left: Turn Left", True, (255, 255, 255))
LF_Joy_Right = font.render("Left Joy Right: Turn Right", True, (255, 255, 255))
RG_Joy_Up = font.render("Right Joy Up: Ascend", True, (255, 255, 255))
RG_Joy_Down = font.render("Right Joy Down: Descend", True, (255, 255, 255))

'''---CLAW CONSTANTS---'''
MAX_CLAW = 65 #Main Claw max value
MIN_CLAW = 0 #Main Claw min value
clawValue = 0 #Main Claw initial value

MAX_CLAW_ROTATE = 360 #Claw rotate max value
MIN_CLAW_ROTATE = 0 #Claw rotate min value
clawRotate = 0 #Claw rotate initial value

# Boolean values for the trigger buttons
trigger_button = [False, False] #states for LB and RB buttons
x_y_button = [False, False] #states for X and Y buttons

'''---MAIN LOOP FOREVER---'''
while True:
    # Event handling
    pygame.event.pump() #it updates the internal states of the joystick
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Button {} pressed".format(event.button))
            
            if event.button == JoyStick.A:  #for toggling max thruster status On/Off
                onStatus.toggle()
                
            if event.button == JoyStick.LB and trigger_button[1] == False: #for closing the claw
                trigger_button[0] = True
                if not clawValue <= MIN_CLAW:
                    clawValue -= 5
                    
            if event.button == JoyStick.RB and trigger_button[0] == False: #for opening the claw
                trigger_button[1] = True
                if not clawValue >= MAX_CLAW:
                    clawValue += 5
                
            if event.button == JoyStick.X and x_y_button[1] == False: #for rotating the claw left
                x_y_button[0] = True
                if not clawRotate <= MIN_CLAW_ROTATE:
                    clawRotate -= 5
                
            if event.button == JoyStick.Y and x_y_button[0] == False: #for rotating the claw right
                x_y_button[1] = True
                if not clawRotate >= MAX_CLAW_ROTATE:
                    clawRotate += 5
                
        elif event.type == pygame.JOYBUTTONUP:
            print("Button {} released".format(event.button))
            
            if event.button ==  JoyStick.LB and trigger_button[0] == True:
                trigger_button[0] = False
            if event.button == JoyStick.RB and trigger_button[1] == True:
                trigger_button[1] = False
            if event.button == JoyStick.X and x_y_button[0] == True:
                x_y_button[0] = False
            if event.button == JoyStick.Y and x_y_button[1] == True:
                x_y_button[1] = False

        for i in range(joystick.get_numaxes()):
            turbo = 1.414 if onStatus.state else 1 #TURBO MODE FOR PRO PILOTs
                
            if i == JoyStick.L_ANALOG_X: #left joystick x-axis for rov head rotate
                x = joystick.get_axis(i) * turbo
                x = 0 if abs(x) < .5 else x #deadzone
                
            if i == JoyStick.L_ANALOG_Y: #left joystick y-axis for rov head tilt
                y = joystick.get_axis(i) * turbo
                y = 0 if abs(y) < .5 else y #deadzone
                
            if i == JoyStick.R_ANALOG_Y: #right joystick y-axis for vertical
                z = joystick.get_axis(i) * turbo
                z = 0 if abs(z) < .5 else z #deadzone
            
            ''' UNDER MAINTENANCE: Haven't tested in water yet
            if i == JoyStick.R_ANALOG_X: #right joystick x-axis for crabbing 
                c = joystick.get_axis(i) * turbo
                c = 0 if abs(c) < .5 else c #deadzone '''
                
    # Math for analog 45 degree angles
    x_new = (x * math.cos(math.pi / -4)) - (y * math.sin(math.pi / -4))
    x_new = min(max(x_new, -1.0), 1.0) #if x_new is less than -1, x_new = -1; if x_new is greater than 1, x_new = 1
    
    y_new = (x * math.sin(math.pi / -4)) + (y * math.cos(math.pi / -4))
    y_new = min(max(y_new, -1.0), 1.0)

    ''' UNDER MAINTENANCE: Haven't tested in water yet
    z_new = (z * math.cos(math.pi / -4)) - (c * math.sin(math.pi / -4))
    z_new = min(max(z_new, -1.0), 1.0)
    
    c_new = (z * math.sin(math.pi / -4)) + (c * math.cos(math.pi / -4))
    c_new = min(max(c_new, -1.0), 1.0) '''
    
    # Send commands to ROV
    commands = {}  #define python dictionary
    commands['tleft'] = mLeftSlider.value = x_new ** 3 #cubing(x^3) the values gives more control with lower power
    commands['tright'] = mRightSlider.value = y_new ** 3
    commands['tup'] = zSlider.value = z ** 3
    commands['claw'] = clawValue
    commands['claw_rotate'] = clawRotate

    if DEBUG:
        print("---Before parsing to JSON---")
        print("tleft: ", commands['claw_rotate'])
        print("tright: ", commands['tright'])
        print("tup: ", commands['tup'])
        print("claw: ", commands['claw'])
        print("claw_rotate: ", commands['claw_rotate'])
    
    MESSAGE = json.dumps(commands)  #puts python dictionary in Json format to MESSAGE as string
    ser.write(bytes(MESSAGE, 'utf-8'))  #byte format sent to Arduino
    ser.flush() #it ensures that ser.write is completed before moving on
    
    if DEBUG:
        print("---After parsing to Arduino JSON---")
        print("tleft: ", commands['claw_rotate'])
        print("tright: ", commands['tright'])
        print("tup: ", commands['tup'])
        print("claw: ", commands['claw'])
        print("claw_rotate: ", commands['claw_rotate'])
        
    try:
        dict_json = json.loads(ser.readline().decode('utf-8')) #read a line from Arduino and decode it to utf-8
        if DEBUG:
            print("---The whole JSON file---")
            print(dict_json)
        
        # Pass the values to the display widgets
        temp_display.value = dict_json['volt']  #assign temp to dispaly
        th_up_display.value = dict_json['sig_up_1']  #vertical thruster value from Arduino
        th_left_display.value = dict_json['sig_lf']  #vertical thruster value from Arduino
        th_right_display.value = dict_json['sig_rt']  #vertical thruster value from Arduino
        claw_display.value = dict_json['claw']  #claw value from Arduino
        claw_rotate_display.value = dict_json['claw_rotate'] #servo value from Arduino
        ser.flush()

    except Exception as e:
        print(e)

    pass
    # Draw Stuff (Rendering the data as a display for the GUI)
    dHeight = onStatus.get_height() #get the height of the toggleable widget
    guiScreen.blit(onStatus.render(), (0, 0)) #blitting the running status
    guiScreen.blit(mLeftSlider.render(), (0, 9 * dHeight)) #blitting thruster values
    guiScreen.blit(mRightSlider.render(), (100, 9 * dHeight)) #blitting thruster values
    guiScreen.blit(zSlider.render(), (200, 9 * dHeight))  #blitting thruster values

    guiScreen.blit(temp_display.render(), (0, dHeight))  #blitting temperature values, pick a font you have and set its size
    guiScreen.blit(th_up_display.render(), (0, 2 * dHeight)) #blitting thruster values
    guiScreen.blit(th_left_display.render(), (0, 3 * dHeight)) #blitting thruster values
    guiScreen.blit(th_right_display.render(), (0, 4 * dHeight)) #blitting thruster values
    guiScreen.blit(claw_display.render(), (0, 5 * dHeight))  #display the claw value on the screen
    guiScreen.blit(claw_rotate_display.render(),( 0, 6* dHeight))
    
    # Rendering more labeling and display elements onto Pygame window.
    screen.blit(guiScreen, (0, 140))  #all the gui
    # screen.blit(scaledImage, (10, -60))  #discord logo
    # Rending the text for the user controls onto the GUI window as defined in the beginning of the code.
    screen.blit(leftText, (15, 290))
    screen.blit(rightText, (115, 290))
    screen.blit(ZAxisText, (215, 290))
    screen.blit(Controls, (720, 390))
    screen.blit(left_button, (650, 425))
    screen.blit(right_button, (650, 450))
    screen.blit(button_A, (650, 470))
    screen.blit(LF_Joy_Up, (650, 495))
    screen.blit(LF_Joy_Down, (650, 520))
    screen.blit(LF_Joy_Left, (650, 550))
    screen.blit(LF_Joy_Right, (650, 570))
    screen.blit(RG_Joy_Up, (650, 600))
    screen.blit(RG_Joy_Down, (650, 620))

    pygame.display.flip()  #update screen for all rectangular images
    pygame.time.Clock().tick(fps)  #fps limit