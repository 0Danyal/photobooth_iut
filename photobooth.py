import picamera
import pygame
import time
import os
import PIL.Image
import RPi.GPIO as GPIO

from threading import Thread
from pygame.locals import *
from time import sleep
from PIL import Image, ImageDraw


# initialise global variables
Numeral = ""  # Numeral is the number display
Message = ""  # Message is a fullscreen message
BackgroundColor = ""
CountDownPhoto = ""
SmallMessage = ""  # SmallMessage is a lower banner message
TotalImageCount = 0  # Counter for Display and to monitor paper usage
imagefolder = 'Photos'
templatePath = os.path.join('Photos', 'Template', "template.png") #Path of template image
ImageShowed = False
BUTTON_PIN = 25
IMAGE_WIDTH = 550
IMAGE_HEIGHT = 360


# Load the background template
bgimage = PIL.Image.open(templatePath)

#Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialise pygame
pygame.init()  # Initialise pygame
pygame.mouse.set_visible(False) #hide the mouse cursor
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w,infoObject.current_h), pygame.FULLSCREEN)  # Full screen 
background = pygame.Surface(screen.get_size())  # Create the background object
background = background.convert()  # Convert it to a background

screenPicture = pygame.display.set_mode((infoObject.current_w,infoObject.current_h), pygame.FULLSCREEN)  # Full screen
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

			
# blackbars
def set_demensions(img_w, img_h):
	
    global transform_y, transform_x, offset_y, offset_x

    # based on output screen resolution, calculate how to display
    ratio_h = (infoObject.current_w * img_h) / img_w 

    if (ratio_h < infoObject.current_h):
        transform_y = ratio_h
        transform_x = infoObject.current_w
        offset_y = (infoObject.current_h - ratio_h) / 2
        offset_x = 0
    elif (ratio_h > infoObject.current_h):
        transform_x = (infoObject.current_h * img_w) / img_h
        transform_y = infoObject.current_h
        offset_x = (infoObject.current_w - transform_x) / 2
        offset_y = 0
    else:
        transform_x = infoObject.current_w
        transform_y = infoObject.current_h
        offset_y = offset_x = 0

def InitFolder():
    global imagefolder
    
    #check image folder existing, create if not exists
    if not os.path.isdir(imagefolder):	
        os.makedirs(imagefolder)	
            
    imagefolder2 = os.path.join(imagefolder, 'images')
    if not os.path.isdir(imagefolder2):
        os.makedirs(imagefolder2)
		
def DisplayText(fontSize, textToDisplay):
    global Numeral
    global Message
    global screen
    global background
    global pygame
    global ImageShowed
    global screenPicture
    global backgroundPicture
    global CountDownPhoto

    if (BackgroundColor != ""):
            #print(BackgroundColor)
            background.fill(pygame.Color("black"))
    if (textToDisplay != ""):
            #print(displaytext)
            font = pygame.font.Font(None, fontSize)
            text = font.render(textToDisplay, 1, (227, 157, 200))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery
            if(ImageShowed):
                    backgroundPicture.blit(text, textpos)
            else:
                    background.blit(text, textpos)
				
def UpdateDisplay():
    # init global variables from main thread
    global Numeral
    global Message
    global screen
    global background
    global pygame
    global ImageShowed
    global screenPicture
    global backgroundPicture
    global CountDownPhoto
   
    background.fill(pygame.Color("white"))  # White background

    if (BackgroundColor != ""):
            #print(BackgroundColor)
            background.fill(pygame.Color("black"))
    if (Message != ""):
            #print(displaytext)
            font = pygame.font.Font(None, 100)
            text = font.render(Message, 1, (227, 157, 200))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery
            if(ImageShowed):
                    backgroundPicture.blit(text, textpos)
            else:
                    background.blit(text, textpos)

    if (Numeral != ""):
            #print(displaytext)
            font = pygame.font.Font(None, 800)
            text = font.render(Numeral, 1, (227, 157, 200))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery
            if(ImageShowed):
                    backgroundPicture.blit(text, textpos)
            else:
                    background.blit(text, textpos)

    if (CountDownPhoto != ""):
            #print(displaytext)
            font = pygame.font.Font(None, 500)
            text = font.render(CountDownPhoto, 1, (227, 157, 200))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery
            if(ImageShowed):
                    backgroundPicture.blit(text, textpos)
            else:
                    background.blit(text, textpos)
    
    if(ImageShowed == True):
    	screenPicture.blit(backgroundPicture, (0, 0))   	
    else:
    	screen.blit(background, (0, 0))
   
    pygame.display.flip()
    return


def ShowPicture(file, delay):
    global pygame
    global screenPicture
    global backgroundPicture
    global ImageShowed
    backgroundPicture.fill((0, 0, 0))
    img = pygame.image.load(file)
    img = pygame.transform.scale(img, screenPicture.get_size())  # Make the image full screen
    #backgroundPicture.set_alpha(200)
    backgroundPicture.blit(img, (0,0))
    screen.blit(backgroundPicture, (0, 0))
    pygame.display.flip()  # update the display
    ImageShowed = True
    time.sleep(delay)
	
# display one image on screen
def show_image(image_path):	
	screen.fill(pygame.Color("white")) # clear the screen	
	img = pygame.image.load(image_path) # load the image
	img = img.convert()	
	set_demensions(img.get_width(), img.get_height()) # set pixel dimensions based on image	
	x = (infoObject.current_w / 2) - (img.get_width() / 2)
	y = (infoObject.current_h / 2) - (img.get_height() / 2)
	screen.blit(img,(x,y))
	pygame.display.flip()

def CapturePicture():
	global imagefolder
        global Numeral
        global Message
        global screen
        global background
        global screenPicture
        global backgroundPicture
        global pygame
        global ImageShowed
	global BackgroundColor	
	
	BackgroundColor = ""
	Numeral = ""
        Message = ""
	UpdateDisplay()
	time.sleep(1)
	CountDownPhoto = ""
	UpdateDisplay()
	background.fill(pygame.Color("black"))
	screen.blit(background, (0, 0))
	pygame.display.flip()
	camera.start_preview()
	BackgroundColor = "black"

	                     
	Numeral = ""
	Message = "PRENEZ LA POSE"
               
        BackgroundColor = ""
        Numeral = ""
        Message = ""
        UpdateDisplay()
        ts = time.time()
        filename = os.path.join(imagefolder, 'images', str(ts) + '.jpg')
        camera.capture(filename, resize=(IMAGE_WIDTH, IMAGE_HEIGHT))
        camera.stop_preview()
        ShowPicture(filename, 2)
        ImageShowed = False
       # return filename
    
	
def TakePictures():
	global imagecounter
	global imagefolder
	global Numeral
	global Message
	global screen
	global background
	global pygame
	global ImageShowed
	global CountDownPhoto
	global BackgroundColor
	

        input(pygame.event.get())
        CapturePicture()       
        UpdateDisplay()

def MyCallback(channel):
    global Printing
    GPIO.remove_event_detect(BUTTON_PIN)
    Printing=True       
	
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

def main(threadName, *args):
    InitFolder()
    while True:
            show_image('images/start_camera.jpg')
            WaitForEvent()
            time.sleep(0.2)
            TakePictures()
    GPIO.cleanup()


# launch the main thread
Thread(target=main, args=('Main', 1)).start()

