import sys, pygame, os
import dialog as dia
import classes
from helpers import *
import match
from classes import *

def start_screen():

    #### SETUP ####
    pygame.init()

    size = width, height = 1600, 900
    black = 0, 0, 0
    speed = [3, 0]

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size)

    base_font = pygame.font.Font("font/VCR.001.ttf", 32)

    color_passive = pygame.Color('black')

    background = retrieve_background("cave")

    title_rect = pygame.Rect(width-1100,height-800,500,50)
    start_rect = pygame.Rect(width-900,height-550,200,50)
    town_start_rect = pygame.Rect(width-900,height-475,200,50)
    options_rect = pygame.Rect(width-900,height-400,200,50)
    exit_rect = pygame.Rect(width-850,height-250,100,50)

    i = 0

    while True:
        screen.fill(black)
        screen.blit(background, (width+i,0))
        screen.blit(background, (i, 0))
        color_start, color_town_start, color_options, color_exit = color_passive
        color_exit = pygame.Color('black')

        if (i == -width):
            screen.blit(background, (width+i, 0))
            i=0
        i-=1

        for event in pygame.event.get():                  
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return "dialog"
                if town_start_rect.collidepoint(event.pos):
                    return "dialog skip"
                if exit_rect.collidepoint(event.pos):
                    return "exit"

        if start_rect.collidepoint(pygame.mouse.get_pos()):
            color_start = pygame.Color(200,0,0)
        if town_start_rect.collidepoint(pygame.mouse.get_pos()):
            color_town_start = pygame.Color(200,0,0)
        if options_rect.collidepoint(pygame.mouse.get_pos()):
            color_options = pygame.Color(200,0,0)
        if exit_rect.collidepoint(pygame.mouse.get_pos()):
            color_exit = pygame.Color(200,0,0)

        # Draw buttons
        pygame.draw.rect(screen, color_passive, title_rect)
        pygame.draw.rect(screen, color_start, start_rect)
        pygame.draw.rect(screen, color_town_start, town_start_rect)
        pygame.draw.rect(screen, color_options, options_rect)
        pygame.draw.rect(screen, color_exit, exit_rect)
        
        # Draw the text onto the buttons
        drawText(screen, "Creatures of Habbitt v.01", pygame.Color(255,255,255,0), title_rect, base_font, False, None, center=True)
        drawText(screen, "Wake Up", pygame.Color(255,255,255,0), start_rect, base_font, False, None, center=True)
        drawText(screen, "Skip", pygame.Color(255,255,255,0), town_start_rect, base_font, False, None, center=True)
        drawText(screen, "Options", pygame.Color(255,255,255,0), options_rect, base_font, False, None, center=True)
        drawText(screen, "Exit", pygame.Color(255,255,255,0), exit_rect, base_font, False, None, center=True)

        pygame.display.update()
        clock.tick(60)

def in_dialog(skip=None):

    #### SETUP ####
    size = width, height = 1600, 900
    speed = [3, 0]
    black = 0, 0, 0

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size)

    background = retrieve_background("cave")

    base_font = pygame.font.Font("font/VCR.001.ttf", 32)
    user_text = dia.dialog_start

    dialog_rect = pygame.Rect(width-1550,height-250,1500,200)
    name_rect = pygame.Rect(width-1550, height-320, 300, 50)
    color_passive = pygame.Color('black')

    i = 0
    advance = 0
    exit_next = 0
    move = True
    global progress
    progress = 0
    global party
    party = []

    if skip:
        user_text = [[[None, "To Town"]]]

    while True:
        screen.fill(black)
        
        if move == True:
            screen.blit(background, (width+i,0))
            screen.blit(background, (i, 0))
            if (i == -width):
                screen.blit(background, (width+i, 0))
                i=0
            i-=1
        else:
            screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dialog_rect.collidepoint(event.pos):
                    background, move = determine_background(user_text[0][advance][1], background, move)
                    if exit_next == 1:
                        sys.exit()
                    elif user_text[0][advance][1] == "[Bear N. Steen has joined your party.]":
                        nsteen = Paladin([15, 10, 10, 10, 10, 10])
                        nsteen.set_name("N. Steen")
                        #rabby = Bookish([10,10,10,15,10,10])
                        #rabby.set_name("Radish")
                        party = [nsteen]
                        advance += 1
                    elif user_text[0][advance][1] in ["Please select a destination.", "[Returning to town.]", "To Town"]:
                        progress = 1
                        print(party)
                        if progress < 2:
                            choice = town_options(screen, "Inn", "???", "inn", None, "???", "???", None, None, "Leave", "leave", background)
                            if choice == "inn":
                                user_text = dia.determine_dialog(choice, progress)
                                progress += 1
                                advance = 0
                            if choice == "leave":
                                if len(party) > 0:
                                # Should go to location menu
                                    match.Game().play(party)
                                else:
                                    user_text = [[[None, "You can't go out alone."], [None, "[Returning to town.]"]]]
                                    advance = 0
                        elif progress < 3:
                            choice = town_options(screen, "Inn", "Smithy", "inn", "blacksmith", "???", "???", None, None, "Leave", "leave", background)
                            if choice == "inn" or choice == "blacksmith":
                                user_text = dia.determine_dialog(choice, progress)
                                progress += 1
                                advance = 0
                    elif user_text[0][advance][1] == "Please select an option.":
                        choice = dialog_options(screen, user_text[0][advance+1][1], user_text[0][advance+2][1], user_text[1], user_text[2], background)
                        proceed = sort_options(choice)
                        user_text = dia.determine_dialog(choice, progress)
                        advance = 0
                    elif user_text[0][advance][1] == "Please type into the box.":
                        array = input_box(user_text[1], background)
                        temp = user_text[1]
                        user_text, name = array[0], array[1]
                        global name_global
                        name_global = name
                        sort_options(temp)
                        advance = 0
                    elif 0 <= advance+1 < len(user_text[0]):
                        advance += 1
                    else:
                        user_text = [["End of text."]]
                        exit_next = 1
                        advance = 0

        
        if user_text[0][advance][0] != None:
            pygame.draw.rect(screen, color_passive, name_rect)
            drawText(screen, user_text[0][advance][0], (255,255,255), name_rect, base_font, center=True)
            character = retrieve_character(user_text[0][advance][0])
            screen.blit(character, (width/2, 0))
        pygame.draw.rect(screen, color_passive, dialog_rect)
        #text_surface = base_font.render(user_text, True, (255,255,255))
        #screen.blit(text_surface, (input_rect.x+20, input_rect.y+20))
        #input_rect.w = max(1500, text_surface.get_width()+10)
        drawText(screen, user_text[0][advance][1], (255,255,255), dialog_rect, base_font)

        pygame.display.update()
        clock.tick(60)

def dialog_options(screen, text_left, text_right, target_left, target_right, background):
    size = width, height = 1600, 900
    clock = pygame.time.Clock()
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    base_font = pygame.font.Font("font/VCR.001.ttf", 32)

    color_passive = pygame.Color('black')

    left_rect = pygame.Rect(width-1550,height-250,700,50)
    right_rect = pygame.Rect(width-750,height-250,700,50)

    i = 0

    while True:
        screen.fill(black)
        screen.blit(background, (width+i,0))
        screen.blit(background, (i, 0))
        color_left = pygame.Color('black')
        color_right = pygame.Color('black')

        if (i == -width):
            screen.blit(background, (width+i, 0))
            i=0
        i-=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if left_rect.collidepoint(event.pos):
                    return target_left
                if right_rect.collidepoint(event.pos):
                    return target_right
            
        if left_rect.collidepoint(pygame.mouse.get_pos()):
            color_left = pygame.Color(200,0,0)
        if right_rect.collidepoint(pygame.mouse.get_pos()):
            color_right = pygame.Color(200,0,0)

        pygame.draw.rect(screen, color_left, left_rect)
        drawText(screen, text_left, (255,255,255), left_rect, base_font)
        pygame.draw.rect(screen, color_right, right_rect)
        drawText(screen, text_right, (255,255,255), right_rect, base_font)

        pygame.display.update()
        clock.tick(60)


def town_options(screen, text_top_left, text_top_right, target_top_left, target_top_right, 
    text_bot_left, text_bot_right, target_bot_left, target_bot_right, text_leave, target_leave, background):

    size = width, height = 1600, 900
    clock = pygame.time.Clock()
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    base_font = pygame.font.Font("font/VCR.001.ttf", 32)

    color_passive = pygame.Color('black')

    top_left_rect = pygame.Rect(width-1550,height-350,700,50)
    top_right_rect = pygame.Rect(width-750,height-350,700,50)
    bot_left_rect = pygame.Rect(width-1550,height-250,700,50)
    bot_right_rect = pygame.Rect(width-750,height-250,700,50)
    leave_rect = pygame.Rect(width-750,height-150,700,50)

    while True:
        screen.fill(black)
        screen.blit(background, (0,0))
        color_top_left = color_passive
        color_top_right = color_passive
        color_bot_left = color_passive
        color_bot_right = color_passive
        color_leave = color_passive

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if top_left_rect.collidepoint(event.pos):
                    return target_top_left
                if top_right_rect.collidepoint(event.pos):
                    return target_top_right
                if bot_left_rect.collidepoint(event.pos):
                    return target_bot_left
                if bot_right_rect.collidepoint(event.pos):
                    return target_bot_right
                if leave_rect.collidepoint(event.pos):
                    return target_leave

        if top_left_rect.collidepoint(pygame.mouse.get_pos()):
            color_top_left = pygame.Color(200,0,0)
        if top_right_rect.collidepoint(pygame.mouse.get_pos()):
            color_top_right = pygame.Color(200,0,0) 
        if bot_left_rect.collidepoint(pygame.mouse.get_pos()):
            color_bot_left = pygame.Color(200,0,0)
        if bot_right_rect.collidepoint(pygame.mouse.get_pos()):
            color_bot_right = pygame.Color(200,0,0)
        if leave_rect.collidepoint(pygame.mouse.get_pos()):
            color_leave = pygame.Color(200,0,0)

        pygame.draw.rect(screen, color_top_left, top_left_rect)
        drawText(screen, text_top_left, (255,255,255), top_left_rect, base_font)
        pygame.draw.rect(screen, color_top_right, top_right_rect)
        drawText(screen, text_top_right, (255,255,255), top_right_rect, base_font)
        pygame.draw.rect(screen, color_bot_left, bot_left_rect)
        drawText(screen, text_bot_left, (255,255,255), bot_left_rect, base_font)
        pygame.draw.rect(screen, color_bot_right, bot_right_rect)
        drawText(screen, text_bot_right, (255,255,255), bot_right_rect, base_font)
        pygame.draw.rect(screen, color_leave, leave_rect)
        drawText(screen, text_leave, (255,255,255), leave_rect, base_font)


        pygame.display.update()
        clock.tick(60)


def input_box(target, background):
    size = width, height = 1600, 900
    clock = pygame.time.Clock()
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    base_font = pygame.font.Font("font/VCR.001.ttf", 32)

    color_passive = pygame.Color('black')

    i = 0

    user_text = ''
    
    # create rectangle
    input_rect = pygame.Rect(width-750, height/2, 200, 50)
    input_rect.center = (width/2, height/2)

    color_active = pygame.Color('red')

    color = color_passive
    
    active = False
    
    while True:
        screen.fill(black)
        screen.blit(background, (width+i,0))
        screen.blit(background, (i, 0))

        if (i == -width):
            screen.blit(background, (width+i, 0))
            i=0
        i-=1
        for event in pygame.event.get():
    
        # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
    
            if event.type == pygame.KEYDOWN:
    
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
    
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
    
                # Unicode standard is used for string
                # formation
                else:
                    user_text += event.unicode
                
                if event.key == pygame.K_RETURN:
                    return [dia.determine_dialog(target, 0, user_text[:-1]), user_text[:-1]]
    
        if active:
            color = color_active
        else:
            color = color_passive
            
        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(screen, color, input_rect)
    
        rect = drawText(screen, user_text, pygame.Color('white'), input_rect, base_font, center=True, input=True)
        
        # set width of textfield so that text cannot get
        # outside of user's text input
        if rect != None:
            input_rect.w = max(100, rect.get_width()+10)
            input_rect.center = (width/2, height/2)
        
        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.update()
        
        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)

def sort_options(choice):
    if choice == "martial_choice":
        prof = classes.Martial([12,10,10,10,10,10])
        prof.set_name = name_global 
        return ["class", prof]
    elif choice == "bookish_choice":
        prof = classes.Bookish([10,10,10,12,10,10])
        prof.set_name(name_global )
        return ["class", prof]

def determine_background(dialog, bg, move):
    if dialog == "Regardless of your choice, I'm taking you outside.":
        return retrieve_background("forest"), True
    if dialog == "Maybe you should just follow that road over there until you run into something." or dialog == "To Town":
        return retrieve_background("village"), False
    else:
        return bg, move

def controller():
    global name_global
    while True:
        option = start_screen()
        if option == "dialog":
            in_dialog()
        elif option == "dialog skip":
            in_dialog("To Town")
        elif option == "exit":
            sys.exit()

if __name__ == "__main__":
    print(os.getcwd())
    controller()



