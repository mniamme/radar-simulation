import RPi.GPIO as GPIO
import pygame
import math
import time
import colors
from target import *

GPIO.setmode(GPIO.BOARD)

# initialize the program
x = pygame.init()

pygame.font.init()

defaultFont = pygame.font.get_default_font()

fontRenderer = pygame.font.Font(defaultFont, 20)

radarDisplay = pygame.display.set_mode((1400, 800))

pygame.display.set_caption('Radar Screen')

# setup the servo
servoPin = 12

GPIO.setup(servoPin, GPIO.OUT)

servo = GPIO.PWM(servoPin, 50)

servo.start(7)

# setup the ultrasonic sensor
TRIG = 16
ECHO = 18
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# targets list
targets = {}


# changing servo angle function
def servoChange(angle):
    angle = 180 - angle
    dc = 1.0 / 18.0 * angle + 2
    servo.ChangeDutyCycle(dc)


# read from the ultrasonic sensor
def ultrasonicRead():
    
    # settling the sensor
    GPIO.output(TRIG, False)
    time.sleep(0.01)

    # send a signal
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # catch a signal
    error = 0
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
        error += 1
        if error > 1000:
            break
    if error > 1000:
        return -1

    end_time = time.time()
    while GPIO.input(ECHO) == 1:
        end_time = time.time()

    # calculate the distance 
    total_time = end_time - start_time
    distance = (34300 * total_time) / 2
    distance = round(distance, 2)

    return distance


# drawing function
def draw(angle, distance):
     # draw initial screen
    radarDisplay.fill(colors.black)

    pygame.draw.circle(radarDisplay, colors.green, (700,800), 650, 1)

    pygame.draw.circle(radarDisplay, colors.green, (700,800), 550, 1)

    pygame.draw.circle(radarDisplay, colors.green, (700,800), 450, 1)

    pygame.draw.circle(radarDisplay, colors.green, (700,800), 300, 1)

    pygame.draw.circle(radarDisplay, colors.green, (700,800), 150, 1)

    radarDisplay.fill(colors.black, [0, 785, 1400, 20])

    # horizental line
    pygame.draw.line(radarDisplay, colors.green, (30, 780), (1370, 780), 1)

    # 45 degree line
    pygame.draw.line(radarDisplay, colors.green, (700, 780),(205, 285), 1)

    # 90 degree line
    pygame.draw.line(radarDisplay, colors.green, (700, 780), (700, 80), 1)

    # 135 degree line
    pygame.draw.line(radarDisplay, colors.green, (700, 780), (1195, 285), 1)

    # draw stastics board
    pygame.draw.rect(radarDisplay, colors.blue, [20, 20, 270, 100], 2)

    # write the 0 degree
    text = fontRenderer.render("0", 1, colors.green)
    radarDisplay.blit(text,(10,780))

    # write the 45 degree
    text = fontRenderer.render("45", 1, colors.green)
    radarDisplay.blit(text,(180,260))

    # write the 90 degree
    text = fontRenderer.render("90", 1, colors.green)
    radarDisplay.blit(text,(690,55))

    # write the 135 degree
    text = fontRenderer.render("135", 1, colors.green)
    radarDisplay.blit(text,(1205,270))

    # write the 180 degree
    text = fontRenderer.render("180", 1, colors.green)
    radarDisplay.blit(text,(1365,780))

    # draw the moving line
    a = math.sin(math.radians(angle)) * 700.0
    b = math.cos(math.radians(angle)) * 700.0
    pygame.draw.line(radarDisplay, colors.green, (700, 780), (700 - int(b), 780 - int(a)), 3)


    # write the current angle
    text = fontRenderer.render("Angle : " + str(angle), 1, colors.white)
    radarDisplay.blit(text,(40,40))

    # write the distance
    if distance == -1:
        text = fontRenderer.render("Distance : Out Of Range" , 1, colors.white)
    else:
        text = fontRenderer.render("Distance : " + str(distance) + " cm" , 1, colors.white)

    radarDisplay.blit(text,(40,80))

    # draw targets
    for angle in targets.keys():
        # calculate the coordinates and the remoteness of the target
        c = math.sin(math.radians(targets[angle].angle)) * 700.0
        d = math.cos(math.radians(targets[angle].angle)) * 700.0
        e = math.sin(math.radians(targets[angle].angle)) * 400.0
        f = math.cos(math.radians(targets[angle].angle)) * 400.0

        # draw the line indicating the target
        pygame.draw.line(radarDisplay, targets[angle].color, (700 - int(f), 780 - int(e)), (700 - int(d), 780 - int(c)), 3)
        
        # fading

        diffTime = time.time() - targets[angle].time
        
        if diffTime >= 0.0 and diffTime <= 0.5:
            targets[angle].color = colors.red1L
        elif diffTime > 0.5 and diffTime <= 1:
            targets[angle].color = colors.red2L
        elif diffTime > 1.0 and diffTime <= 1.5:
            targets[angle].color = colors.red3L
        elif diffTime > 1.5 and diffTime <= 2.0:
            targets[angle].color = colors.red4L
        elif diffTime > 2.0 and diffTime <= 2.5:
            targets[angle].color = colors.red5L
        elif diffTime > 2.5 and diffTime <= 3.0:
            targets[angle].color = colors.red6L
        elif diffTime > 3.0:
            del targets[angle]
            



    # update the screen
    pygame.display.update()
    


try:
    while True:
        
        # draw
        for angle in range(0, 180):
            distance = ultrasonicRead()
            if distance != -1 and distance < 20:
                targets[angle] = Target(angle)
                
            draw(angle, distance)
            servoChange(angle)
            time.sleep(0.01)
            


        for angle in range(180, 0, -1):
            distance = ultrasonicRead()
            if distance != -1 and distance < 20:
                targets[angle] = Target(angle)
            
            draw(angle, distance)
            servoChange(angle)
            time.sleep(0.01)
            
except KeyboardInterrupt:
    print 'Radar Exit'
    servo.stop()
    GPIO.cleanup()
    
pygame.quit()
quit()
