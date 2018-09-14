#imports
import pygame
import time
import random
import math

#note section

#Game idea:
#Kim is like a pacman (KimMan, Dashpac, PacDash, KarMan, DashMan)
#She eats little kanyes, kylies, and kendals.
#Makeup is a powerup... or something.
#Amber rose is poisonous (minus life)
#Ray jay = career/points boost.
#She can collect things
#Comedy genre

#Choose character??                                                         DONE
#randomise colours/ shapes - introduce unpredictability
# "loading"/instruction screen
# sort top/bottom boundary                                                  DONE
# work on colour scheme/fonts
# other metrics, like health, items collected
# add to the dead() function to make something happen when avatar dies

#######################################################################################################################

pygame.init() #always need this, it initiates the pygame package

#defining screen dim.
display_width = 800
display_height = 600

#nice font
rounded_ele_path = '/Users/ainefairbrother/Documents/pygame_files/Fonts/rounded_elegance.ttf'

#defining basic text types
largeText = pygame.font.Font(rounded_ele_path, 30)
medText = pygame.font.Font(rounded_ele_path, 20)

#basic colours
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
block_colour = (153,0,230) #purple

#anime sunset palette
peach = (244,170,137)
dark_peach = (239,131,131)
red_pink = (240,98,97)
light_plum = (169,88,165)
plum = (97,62,151)

#background colour and corresponding rect coordinate
bkg = [(peach,[0,0,800,120]),(dark_peach,[0,120,800,120]),(red_pink,[0,240,800,120]),(light_plum,[0,360,800,120]),(plum,[0,480,800,120])]

#importing avatar images
kim_img = pygame.image.load('/Users/ainefairbrother/Documents/pygame_files/kim.png') #storing the image of kim avatar in a variable, loading it
kim_white_ol = pygame.image.load('/Users/ainefairbrother/Documents/pygame_files/kim_white_ol.png')
kanye_img = pygame.image.load('/Users/ainefairbrother/Documents/pygame_files/kanye.png')
kanye_white_ol = pygame.image.load('/Users/ainefairbrother/Documents/pygame_files/kanye_white_ol.png')
kris_img = pygame.image.load('/Users/ainefairbrother/Documents/pygame_files/kris.png')

#defining size of kim avatar
kim_width = 50
kim_length = 58
kim_midpoint = (kim_length/2,kim_width/2)
#defining size of kanye avatar
kanye_width = 50
kanye_length = 72
kanye_midpoint = (kanye_width/2,kanye_length/2)
#defining size of kanye avatar
kris_width = 55
kris_length = 44
kris_midpoint = (kris_width/2, kris_length/2)

#defining some basic math fn
pi = math.pi

#setting up the game display
gameDisplay = pygame.display.set_mode((display_width,display_height))

#window title
pygame.display.set_caption('PacDash')

#creating an object to help track time
clock = pygame.time.Clock()


#functions

def things(thingx, thingy, thingw, thingh, colour):
    """

    This function generates rectangles according to the given parameters:

    :param thingx:      top left x co-ord
    :param thingy:      top left y co-ord
    :param thingw:      width of shape
    :param thingh:      height of shape
    :param colour:      colour of shape
    :return:            returns a drawn shape

    """
    pygame.draw.rect(gameDisplay, block_colour, [thingx, thingy, thingw, thingh])

def kim(x,y):
    """
    Blits the Kim avatar to the co-ordinates passed through the function.
    x and y represent the co-ords of the top left corner

    """
    gameDisplay.blit(kim_img,(x,y))

def kim_white_outline(x,y):
    gameDisplay.blit(kim_white_ol, (x-25,y-8.25))

def kanye(x,y):
    """
    Blits the Kanye avatar to the co-ordinates passed through the function.
    x and y represent the co-ords of the top left corner

    """
    gameDisplay.blit(kanye_img,(x,y))

def kanye_white_outline(x,y):
    gameDisplay.blit(kanye_white_ol, (x-30.4,y-5.5))

def kris(x,y):
    gameDisplay.blit(kris_img, (x,y))

def text_objects(text, font, col):
    textSurface = font.render(text, True, col)
    return textSurface, textSurface.get_rect()

def things_dodged(count):
    """
    Function to display a score count in the top left corner. This function takes a given/calculated number,
    and displays it. Adds relevant word next to it and renders it as text.
    Converts count to string.
    Then blits - necessary to display in game.

    """
    font = pygame.font.Font(rounded_ele_path, 18)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text, (0,0))

def message_display(text, size, col):
    """
    Sends 'text' to the screen.
    pygame.display.update() - It allows only a portion of the screen to be updated, instead of the entire area.
    Updates portion of screen, holds it there shortly.

    """
    #You might want other messages, so this isn't included in the
    #crash function, as it's code that will be used again for
    #other scenarios i.e. winning
    font = pygame.font.Font(rounded_ele_path, size)
    TextSurf, TextRect = text_objects(text, font, col)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def dead():
    """

    Feeds a message to the message_display function to indicate that the user has killed Kim.

    """
    gameDisplay.fill(plum)
    text = str("You are dead.")
    message_display(text, 50, white)
    time.sleep(1)
    pygame.display.update()

def quitgame():
    """
    Quits the game
    :return:
    """
    pygame.quit()
    quit()

def image_button(x, y, w, h, avatar_name):
    """
    :param msg: what should the button say?
    :param x: x pos
    :param y: y pos
    :param w: width of button
    :param h: height of button
    :param i_col: inactive colour
    :param a_col: active colour
    :param action: what should it do? Default is nothing.
    :return:
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if avatar_name == kim: #creating avatar movements
            avatar_name(x,y)
            kim_white_outline(x,y)
        if avatar_name == kanye:
            avatar_name(x, y)
            kanye_white_outline(x,y)
        if click[0] == 1:
            game_loop(avatar_name) #begins game with selected avatar passed to game_loop()

def button(msg, x, y, w, h, i_col, a_col, text_col, action=None):
    """
    :param msg: what should the button say?
    :param x: x pos
    :param y: y pos
    :param w: width of button
    :param h: height of button
    :param i_col: inactive colour
    :param a_col: active colour
    :param action: what should it do? Default is nothing.
    :return:
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, a_col, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, i_col, (x, y, w, h))

    smallText = pygame.font.Font(rounded_ele_path, 20)
    textSurf, textRect = text_objects(msg, smallText, text_col)
    textRect.center = ((x + (w / 2), y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)

def text_to_screen(text, size, x, y, col):
    """
    :param text: what text do you want to push to the screen
    :param size: integer
    :param x: x loc
    :param y: y loc
    :param col: colour
    :return:
    """
    text = str(text)
    text_len = len(text)
    font = pygame.font.Font(rounded_ele_path, size)
    text = font.render(text, True, col)
    gameDisplay.blit(text, (x - text_len, y))

# def loading_screen():
#     loading = True
#
#     while loading:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#
#         gameDisplay.fill(peach)
#
#         text_to_screen("Loading...", 30, display_height/2, display_width/2, red_pink)
#
#         kris(display_height/2,display_width/2)
#
#         for num in range(-pi,2*pi):
#             pygame.transform.rotate(kris_img,num)
#
#         pygame.display.update()

def game_intro():
    """
    Function to add an intro to the game. This is run prior to the main game loop.
    It provides the game title, and calls the button function to add a go and quit button.

    """
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # backgound col
        for col, coord in bkg:
            gameDisplay.fill(col, rect=coord)

        # pixAr = pygame.PixelArray(gameDisplay)
        # pixAr[:, 0:160] = peach
        # pixAr[:, 160:320] = dark_peach
        # pixAr[:, 320:480] = red_pink
        # pixAr[:, 480:520] = light_plum
        # pixAr[:, 520:640] = plum

        #This places the title of the game at the center of the screen
        TextSurf, TextRect = text_objects("PacDash", largeText, white)
        TextRect.center = ((display_width/2), (display_height/8))
        gameDisplay.blit(TextSurf, TextRect)

        #additional text
        select_char_text = "Select your character"
        message_display(select_char_text, 30, white)
        #disp_with_div2 = display_width + len(select_char_text)
        #text_to_screen(select_char_text, 20, disp_with_div2/2, display_height/2, white)

        kim(150,275)
        kanye(600,275)

        image_button(150, 275, kim_width, kim_length, kim)
        image_button(600, 275, kanye_width, kanye_length, kanye)

        #Using our button function to draw a go and quit button
        #button("GO!", 150, 450, 100, 50, green, bright_green, game_loop)
        #button("Quit!", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()

def game_loop(avatar):     #game loop (logic for the game):
    """
    Determines the actual running of the game.

    """
    x = (display_width*0.45)
    y = (display_height*0.8)

    x_change = 0
    y_change = 0

    thing_startx = random.randrange(0,display_width)
    thing_starty = -600
    thing_speed = 3
    thing_width = 100
    thing_height = 100

    avatar_width = 0
    avatar_length = 0

    dodged = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or pygame.K_DOWN:
                    x_change = 0
                    y_change = 0

        y += y_change
        x += x_change

        # backgound col
        for col, coord in bkg:
            gameDisplay.fill(col, rect=coord)

        #for col in bkg_col and coord in bkg_coord:
            #gameDisplay.fill(col, coord)

        things(thing_startx, thing_starty, thing_width, thing_height, black) #drawing the blocks
        thing_starty += thing_speed

        #Allows avatar selection, applies their width:
        if avatar == kim:
            avatar_width = kim_width
            avatar_length = kim_length
            kim(x,y) #drawing kim
        elif avatar == kanye:
            avatar_width = kanye_width
            avatar_length = kanye_length
            kanye(x,y)

        things_dodged(dodged) #drawing the score

        if x > display_width - avatar_width or x < 0:
            dead()
        if y > display_height - avatar_length or y < 0:
            dead()

        if thing_starty > display_height: # every time block falls below bottom of screen
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += 1
            thing_width += dodged * 1.2

        if y > thing_starty and y < thing_starty + thing_height or y + avatar_length > thing_starty and y + avatar_length < thing_starty + thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x + avatar_width > thing_startx and x + avatar_width < thing_startx + thing_width:
                dead()






        pygame.display.update()
        clock.tick(60)

game_intro()
#loading_screen()
game_loop()
pygame.quit()
quit()

# if the y co-ord of avatar is less than the y co-ord + height of the block
    # OR if the y co-ord of the avatar is greater than

    # if the x co-ord of avatar is greater than the top left of block
                # AND the x co-ord of avatar is less than the top right corner

    # OR the x-co-ord of avatar plus its width is greater than the top left of block
                # AND the x co-ord of avatar plus its width is less than the top right of the block
