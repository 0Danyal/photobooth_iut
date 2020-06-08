import picamera
import pygame
import time
import os
import PIL.Image
import RPi.GPIO as GPIO
from threading import Timer

from threading import Thread
from pygame.locals import *
from time import sleep
from PIL import Image, ImageDraw


# initialise global variables
imagefolder = 'Photos'
templatePath = os.path.join('Photos', 'Template', "template.png") #Path of template image
BUTTON_PIN = 16
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
dir = os.path.join(imagefolder, 'images')
imageCount = len(next(os.walk(dir))[2]) +1
startTime = 0


img1 = os.path.join('Photos', 'Template', "img1.png")
img2 = os.path.join('Photos', 'Template', "img2.png")
img3 = os.path.join('Photos', 'Template', "img3.png")



idle = 0



# Load the background template
bgimage = PIL.Image.open(templatePath)

#Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialise pygame
pygame.init()  # Initialise pygame
pygame.mouse.set_visible(False) #hide the mouse cursor
infoObject = pygame.display.Info()
#screen = pygame.display.set_mode((infoObject.current_w,infoObject.current_h), pygame.FULLSCREEN)  # Full screen 
screen = pygame.display.set_mode((500,500)) 
background = pygame.Surface(screen.get_size())  # Create the background object
background = background.convert()  # Convert it to a background

#screenPicture = pygame.display.set_mode((infoObject.current_w,infoObject.current_h), pygame.FULLSCREEN)  # Full screen
screenPicture = pygame.display.set_mode((500,500))
backgroundPicture = pygame.Surface(screenPicture.get_size())  # Create the background object
backgroundPicture = background.convert()  # Convert it to a background

transform_x = infoObject.current_w # how wide to scale the jpg when replaying
transfrom_y = infoObject.current_h # how high to scale the jpg when replaying

camera = picamera.PiCamera()
# Initialise the camera object
camera.resolution = (infoObject.current_w, infoObject.current_h)
camera.rotation              = 0
camera.hflip                 = True
camera.vflip                 = False
camera.brightness            = 50
camera.preview_alpha = 120
camera.preview_fullscreen = True

# A function to handle keyboard/mouse/device input events
def input(events):
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()

	
def WaitForEvent():
    global pygame
    NotEvent = True
    while NotEvent:
            input_state = GPIO.input(BUTTON_PIN)
            if input_state == False:
                    NotEvent = False			
                    return
            for event in pygame.event.get():			
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                        if event.key == pygame.K_DOWN:
                            NotEvent = False
                            return
            time.sleep(0.2)

            
def show_image(image_path , duration):
    img = pygame.image.load(image_path) # load the image
    #width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    width, height = 500,500
    img = pygame.transform.scale(img, (width,height))
    screen.blit(img,(0,0))
    pygame.display.flip()
    time.sleep(duration)
    resetBackground()
    takePicture
    

def takePicture():
    
    global startTime
    global imageCount
    global imagefolder
    global img1
    global img2
    global img3
    global idle
    
    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    f_img1 = pygame.transform.scale(pygame.image.load(img1), (width,height))
    f_img2 = pygame.transform.scale(pygame.image.load(img2), (width,height))
    f_img3 = pygame.transform.scale(pygame.image.load(img3), (width,height))
       
    resetBackground() #clear background
    camera.start_preview() 
    WaitForEvent()  
    
    screen.blit(f_img3,(0,0))
    pygame.display.flip()
    sleep(1)
    resetBackground()
    
    screen.blit(f_img2,(0,0))
    pygame.display.flip()
    sleep(1)
    resetBackground()
    
    screen.blit(f_img1,(0,0))
    pygame.display.flip()
    sleep(1)
    resetBackground()
    
    startTime = time.time()

    
    filename = os.path.join(imagefolder, 'images', str(imageCount) + '.jpg')
    
    camera.capture(filename, resize=(IMAGE_WIDTH, IMAGE_HEIGHT)) #take picture
    
    idle = 0
    
    camera.stop_preview()
    imageCount +=1
    show_image(filename , 3) #show the image for 3s
    
        
def resetBackground():
    #Clear the background from any old picture
    background.fill(pygame.Color("black"))
    screen.blit(background, (0, 0))
    pygame.display.flip()
    

                
def waitForIdle():
    global idle
    while True:
        if idle < 30:
            sleep(1)
            idle+=1
        else:
            camera.stop_preview()
            os.system('python slideshow.py &')
            pygame.display.quit()
            pygame.quit()
        

def main(threadName, *args):
    
    global idle
    
    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen.blit(pygame.transform.scale(pygame.image.load(templatePath),(width,height)),(0,0))
    pygame.display.flip()
    WaitForEvent()
    takePicture()
    while True:
        takePicture()
    GPIO.cleanup()



# launch the main thread
Thread(target=main, args=('Main', 1)).start()
Thread(target=waitForIdle, args=[]).start()

