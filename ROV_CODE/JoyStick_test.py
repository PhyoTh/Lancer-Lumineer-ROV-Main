'''""import pygame

def test_controller():
    pygame.init() # Initialize Pygame
    pygame.joystick.init() # Initialize the joystick module

    if pygame.joystick.get_count() == 0:
        print("No joystick detected.")
        return

    joystick = pygame.joystick.Joystick(0) # Create a joystick object by selecting the first joystick detected (index 0)
    joystick.init() # Initialize the joystick

    print("Joystick Name:", joystick.get_name())
    print("Number of Axes:", joystick.get_numaxes()),
    print("Number of Buttons:", joystick.get_numbuttons())
    print("Number of Hats:", joystick.get_numhats())

    try: # Starts a try block to catch exceptions
        while True: # Loop forever
            for event in pygame.event.get(): # Get events from the queue
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.JOYAXISMOTION:
                    print("Axis {} moved to {:.2f}".format(event.axis, joystick.get_axis(event.axis)))
                elif event.type == pygame.JOYBUTTONDOWN:
                    print("Button {} pressed".format(event.button))
                elif event.type == pygame.JOYBUTTONUP:
                    print("Button {} released".format(event.button))
                elif event.type == pygame.JOYHATMOTION:
                    print("Hat {} moved to {}".format(event.hat, joystick.get_hat(event.hat)))
    finally: # Executes the finally block of code after the try block
        pygame.quit()

if __name__ == "__main__": # If this script is run as the main module
    test_controller()'''
    
import pygame

def test_controller():
    pygame.init()  # Initialize Pygame
    pygame.joystick.init()  # Initialize the joystick module

    assert pygame.joystick.get_count() != 0, "No joystick detected"

    joystick = pygame.joystick.Joystick(0)  # Create a joystick object by selecting the first joystick detected (index 0)
    joystick.init()  # Initialize the joystick

    print("Joystick Name:", joystick.get_name())
    print("Number of Axes:", joystick.get_numaxes())
    print("Number of Buttons:", joystick.get_numbuttons())
    print("Number of Hats:", joystick.get_numhats())

    # Set up the screen
    screen_width = 1280
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)
    pygame.display.set_caption("Joystick Control")

    # Set up the rectangle
    rect_width = 50
    rect_height = 50
    rect_x = screen_width // 2 - rect_width // 2
    rect_y = screen_height // 2 - rect_height // 2
    rect_speed = 5

    try:
        while True:  # Loop forever
            for event in pygame.event.get():  # Get events from the queue
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Move the rectangle based on joystick input
            for i in range(joystick.get_numaxes()):
                if i == 0:  # Horizontal axis
                    rect_x += int(joystick.get_axis(i) * rect_speed)
                elif i == 1:  # Vertical axis
                    rect_y += int(joystick.get_axis(i) * rect_speed)

            # Fill the screen with white
            screen.fill((255, 255, 255))

            # Draw the rectangle
            pygame.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height))

            pygame.display.flip()
            pygame.time.Clock().tick(240)  # Limit to 60 frames per second
    finally:
        pygame.quit()

if __name__ == "__main__":  # If this script is run as the main module
    test_controller()
