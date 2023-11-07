import time
import sys
from fhict_cb_01.custom_telemetrix import CustomTelemetrix

# Constants
LED_PINS = [4, 5]  # Red LED on pin 4, Green LED on pin 5
BUTTON_PIN = 8  # Button connected to pin 8
BUZZER_PIN = 3  # Buzzer connected to pin 3

# Global variables
level = 0
prevLevel = 0
button_pressed = False  # Flag to indicate if the button has been pressed
green_led_on = False  # Flag to indicate if the green LED is on

# Callback function for button state change
def ButtonChanged(data):
    global level, button_pressed
    level = data[2]
    if level == 0:
        button_pressed = True

# Functions
def setup():
    global board
    board = CustomTelemetrix()
    for pin in LED_PINS:
        board.set_pin_mode_digital_output(pin)
    board.set_pin_mode_digital_output(BUZZER_PIN)  # Set the buzzer pin as an output

    board.set_pin_mode_digital_input_pullup(BUTTON_PIN, callback=ButtonChanged)

def wait_for_button_press():
    print('Press the button to start...')
    while not button_pressed:
        time.sleep(0.1)

def display_countdown_and_buzz_led(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        remaining_time = int(duration - (time.time() - start_time))
        remaining_time = max(remaining_time, 0)
        board.displayShow("{:02d}".format(remaining_time))
        
        # Blink the red LED every 0.5 seconds
        if (int((time.time() - start_time) * 2) % 2) == 0:
            board.digital_write(4, 1)
            board.digital_write(BUZZER_PIN, 1)  # Turn on the buzzer
        else:
            board.digital_write(4, 0)
            board.digital_write(BUZZER_PIN, 0)  # Turn off the buzzer
        
        time.sleep(0.25)

def reset_program_state():
    global button_pressed, green_led_on
    button_pressed = False
    green_led_on = False
    board.digital_write(4, 0)  # Turn off the red LED
    board.digital_write(5, 0)  # Turn off the green LED
    board.digital_write(BUZZER_PIN, 0)  # Turn off the buzzer

# Main program
setup()
try:
    while True:
        wait_for_button_press()

        # Display a 20-second countdown and blink the red LED and buzz the buzzer
        display_countdown_and_buzz_led(60)  # Adjusted to run for 20 seconds

        # Turn on the green LED
        green_led_on = True
        board.digital_write(5, 1)

        # Wait for 15 seconds before turning off the green LED
        time.sleep(5)  # Green LED on for 5 seconds

        board.digital_write(5, 0)  # Turn off the green LED

        # Wait for 1 seconds before turning off the red LED and resetting the program state
        time.sleep(1)  # Red LED and buzzer on for 5 seconds

        reset_program_state()  # Reset the program state
        

except KeyboardInterrupt:
    print('Shutdown')
    board.shutdown()
    sys.exit(0)
