import colors
import pygame
import math
import time

""" This module draws the radar screen """

def draw(radarDisplay, targets, angle, distance, fontRenderer):
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
        c = math.sin(math.radians(targets[angle].angle)) * 800.0
        d = math.cos(math.radians(targets[angle].angle)) * 800.0
	# change the scale if the range is changed
        e = math.sin(math.radians(targets[angle].angle)) * (700 / 50) * targets[angle].distance
        f = math.cos(math.radians(targets[angle].angle)) * (700 / 50) * targets[angle].distance

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
    
