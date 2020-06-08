#from photoboothv2.py import *
import pygame
import time
import os
import PIL.Image
import RPi.GPIO as GPIO
from threading import Thread

from threading import Thread
from pygame.locals import *
from time import sleep
from PIL import Image, ImageDraw

imagefolder = 'Photos'
dir = os.path.join(imagefolder, 'images')
imageCount = len(next(os.walk(dir))[2]) 
BUTTON_PIN = 16
buttonPressed = False

#Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialise pygame
pygame.init()  # Initialise pygame
pygame.mouse.set_visible(False) #hide the mouse cursor
infoObject = pygame.display.Info()
#screen = pygame.display.set_mode((infoObject.current_w,infoObject.current_h), pygame.FULLSCREEN)  # Full screen 
screen = pygame.display.set_mode((500,500))  # Full screen
background = pygame.Surface(screen.get_size())  # Create the background object
background = background.convert()  # Convert it to a background

#screenPicture = pygame.display.set_mode((infoObject.current_w,infoObject.current_h), pygame.FULLSCREEN)  # Full screen
screenPicture = pygame.display.set_mode((500,500))  # Full screen
backgroundPicture = pygame.Surface(screenPicture.get_size())  # Create the background object
backgroundPicture = background.convert()  # Convert it to a background


def resetBackground():
    #Clear the background from any old picture
    background.fill(pygame.Color("black"))
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
def slideshow():
    global imageCount
    global buttonPressed
    while True:
        for i in range(0 , imageCount):
            if buttonPressed:
                os.system('python photoboothv2.py &')
                print('button pressed')
                pygame.display.quit()
                pygame.quit()
            filename = os.path.join(imagefolder, 'images', str(i) + '.jpg')
            img = pygame.image.load(filename) # load the image
            width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
            width, height =500,500
            img = pygame.transform.scale(img, (width,height))
            screen.blit(img,(0,0))
            pygame.display.flip()
            time.sleep(5)
            resetBackground()
            
def detectButton():
    global buttonPressed
    while True:
        input_state = GPIO.input(BUTTON_PIN)
        if input_state == False:
            buttonPressed = True
            #print("Button pressed")
            sleep(0.1)

Thread(target = detectButton).start()
Thread(target = slideshow).start()


