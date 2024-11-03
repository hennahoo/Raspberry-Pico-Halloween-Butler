import time
import board
import audiomp3
import audiopwmio
import pwmio
import pulseio

#######################################################################
# ULTRA SONIC SENSOR
#######################################################################
#import the Ultra Sonic sensor library from adafruit zip
import adafruit_hcsr04
#sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP3, echo_pin=board.GP2)
#sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP3, echo_pin=board.GP2)
#sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D3, echo_pin=board.D2)
#######################################################################

#############################################################################
# NEOPIXEL RGB LED STRIPE
#############################################################################
from rainbowio import colorwheel
import neopixel
#Setting up the Neopixel LED stripe, to port A1
pixel_pin = board.A1
num_pixels = 30
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)
#############################################################################

##########################################################
# SERVO MOTOR CONTROL
##########################################################
from adafruit_motor import servo
# Create PWMOut object
pwm = pwmio.PWMOut(board.GP20, frequency=50)
# Create a servo object with the pwm  object created above
servo_1 = servo.Servo(pwm)
##########################################################

##########################################################
# MP3 PLAYER
##########################################################
#Setting up the MP3 file for playing
audio = audiopwmio.PWMAudioOut(board.GP0)
decoder = audiomp3.MP3Decoder(open("halloween.mp3", "rb"))
##########################################################



# LED STRIPE CONTROL
def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
        time.sleep(0.5)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)


while True:   
    servo_1.angle = 0        # Move servo motor to position 0,  turn the skull
    audio.play(decoder)      # Playing MP3 on constant loop

    if sonar.distance > 0 and sonar.distance < 100:
        human_detected=true
        print ("Human detected!")
        
    elif sonar.distance > 100 and sonar.distance < 1500:
        human_detected=false
        print ("Human not detected")

    if human_detected == true:
        servo_1.angle = 90
        audio.play(decoder)        # Playing MP3 on constant loop
        pixels.fill(RED)
        pixels.show()     
        # Inc. or decrease to change the speed of the solid color change.
        time.sleep(1)
    
    elif human_detected == false:
        servo_1.angle = 0        
        pixels.fill(GREEN)
        pixels.show()
        time.sleep(1)
        pixels.fill(BLUE)
        pixels.show()
        time.sleep(1)
        servo_1.angle = 180        
        color_chase(RED, 0.1)  # Inc. the number to slow down the color chase
        color_chase(YELLOW, 0.1)
        color_chase(GREEN, 0.1)
        color_chase(CYAN, 0.1)
        color_chase(BLUE, 0.1)
        color_chase(PURPLE, 0.1)
        rainbow_cycle(0)  # Inc. the number to slow down the rainbow
