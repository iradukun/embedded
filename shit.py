import pygame
import serial
import sys
from pynput.keyboard import Key, Controller  # Import the necessary pynput modules
import random

# Initialize Pygame
pygame.init()

# Create a Pygame display surface
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a Pygame clock object to control the frame rate
clock = pygame.time.Clock()

# Create a serial connection to the Arduino
arduino = serial.Serial('/dev/cu.usbmodem14201', 115200, timeout=0.1)  # Update the port to your Arduino port

# Define game constants and variables
BACKGROUND_COLOR = (0, 0, 0)
CHARACTER_COLOR = (255, 255, 255)
ITEM_COLOR = (255, 0, 0)  # Color for items
character_x, character_y = WIDTH // 2, HEIGHT // 2
character_speed = 5

keysDown = {}  # Dictionary to track currently pressed keys

# Import pynput modules and create a keyboard controller
from pynput.keyboard import Key, Controller
keyboard = Controller()

# Your existing functions

def keyDown(key):
    keyboard.press(key)

def keyUp(key):
    keyboard.release(key)

def handleJoyStickAsArrowKeys(x, y, z):
    if x == 0:
        keyDown(Key.down)
        keyUp(Key.up)
    elif x == 2:
        keyDown(Key.up)
        keyUp(Key.down)
    else:
        keyUp(Key.up)
        keyUp(Key.down)

    if y == 2:
        keyDown(Key.right)
        keyUp(Key.left)
    elif y == 0:
        keyDown(Key.left)
        keyUp(Key.right)
    else:
        keyUp(Key.left)
        keyUp(Key.right)

    if z == 1:
        keyDown(Key.space)
    else:
        keyUp(Key.space)

# Function to move the character
def move_character(direction):
    if direction == 'up':
        character_y -= character_speed
    elif direction == 'down':
        character_y += character_speed
    elif direction == 'left':
        character_x -= character_speed
    elif direction == 'right':
        character_x += character_speed

# List to store item positions (sample data)
items = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(10)]

# Define the win condition (you can adjust this as needed)
win_condition = len(items) == 0  # Win if there are no items left

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read joystick data from the serial interface
    joystick_data = arduino.readline().decode('utf-8')
    if joystick_data.startswith("S"):
        joystick_values = joystick_data.split()
        if len(joystick_values) == 3:
            try:
                dx = int(joystick_values[0])
                dy = int(joystick_values[1])
                JSButton = int(joystick_values[2])
                handleJoyStickAsArrowKeys(dx, dy, JSButton)
            except ValueError:
                print("Invalid data format:", joystick_data)
        else:
            print("Invalid data format:", joystick_data)

    # Update character's position based on joystick input
    if 'up' in keysDown:
        move_character('up')
    if 'down' in keysDown:
        move_character('down')
    if 'left' in keysDown:
        move_character('left')
    if 'right' in keysDown:
        move_character('right')

    # Check if the character collects an item
    for item in items[:]:
        if abs(character_x - item[0]) < 10 and abs(character_y - item[1]) < 10:
            items.remove(item)

    # Draw the character and items on the screen
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, CHARACTER_COLOR, pygame.Rect(character_x, character_y, 20, 20))
    for item in items:
        pygame.draw.circle(screen, ITEM_COLOR, item, 5)

    # Check for the win condition
    if win_condition:
        # Handle the win condition (e.g., show a win message)
        print("You win!")
        running = False

    # Update the display and control the frame rate
    pygame.display.flip()
    clock.tick(60)

# Close the Arduino serial connection
arduino.close()

# Check for the lose condition
if len(items) > 0:
    # Handle the lose condition (e.g., show a lose message)
    print("You lose!")

# Quit Pygame
pygame.quit()
sys.exit()
