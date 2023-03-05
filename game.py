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

    screen = pygame.display.set_mode((width, height),
                                              pygame.DOUBLEBUF|pygame.OPENGL)

    base_font = pygame.font.Font("font/VCR.001.ttf", 32)

    color_passive = "BLACK"
    color_start, color_town_start, color_options, color_exit = color_passive, color_passive, color_passive, color_passive
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
        
        draw_start_screen(color_start, color_town_start, color_options, color_exit)
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

        
        # Draw the text onto the buttons


        pygame.display.flip()
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
    global party
    party = []

    curr_text = user_text[0][advance][1]
    if curr_text in ["inn"]:
        choice = inn_menu(screen, progress, background)

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
                        party.append(add_party_member("nsteen"))
                        advance += 1
                    elif user_text[0][advance][1] in ["Please select a destination.", "[Returning to town.]", "To Town"]:
                        if progress == 1:
                            choice = town_options(screen, "Inn", "???", "inn", None, "???", "Add Party", None, "party_debug", "Venture Out", "leave", background)
                            if choice == "party_debug":
                                party.append(add_party_member("nsteen"))
                                party.append(add_party_member("radish"))
                                party.append(add_party_member("toffee"))
                                party.append(add_party_member("grapefart"))
                                user_text = [[[None, "Added party members."], [None, "[Returning to town.]"]]]
                                progress += 1
                                advance = 0
                            if choice == "inn":
                                user_text = dia.determine_dialog(choice, progress)
                                progress += 1
                                advance = 0
                            if choice == "leave":
                                user_text = [[[None, "You shouldn't go out alone. Maybe someone in the inn can help you?"], [None, "[Returning to town.]"]]]
                                advance = 0
                        elif progress == 2:
                            choice = town_options(screen, "Inn", "Smithy", "inn", "blacksmith", "???", "???", None, None, "Venture Out", "leave", background)
                            if choice == "blacksmith":
                                user_text = [[[None, "There is no one to run the blacksmith, so it remains closed."], [None, "[Returning to town.]"]]]
                                advance = 0
                            elif choice == "inn":
                                choice = inn_menu(screen, progress, background)
                                user_text = dia.determine_dialog(choice, progress)
                                advance = 0
                            elif choice == "leave":
                                if len(party) > 0:
                                # Should go to location menu
                                    dungeon = "cave"
                                    state = match.Game().play(party, get_dungeon(dungeon))
                                    if state == "WIN":
                                        user_text = [[[None, "Your party was victorious!"],[None, "[Returning to town.]"]]]
                                    elif state == "DEAD":
                                        user_text = [[[None, "Your party was wiped out..."],[None, "[Returning to town.]"]]]
                                    elif state == "RAN":
                                        user_text = [[[None, "[Returning to town.]"]]]
                                    advance = 0
                    elif user_text[0][advance][1] == "[You leave him to his devices.]":
                        choice = inn_menu(screen, progress, background)
                        user_text = dia.determine_dialog(choice, progress)
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

def inn_menu(screen, progress, background):

    size = width, height = 1600, 900
    clock = pygame.time.Clock()
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    base_font = pygame.font.Font("font/VCR.001.ttf", 32)

    color_passive = pygame.Color('black')

    title_rect = pygame.Rect(width-1500,height-800,1400,50)
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
                    return "nsteen"
                if top_right_rect.collidepoint(event.pos):
                    if progress >= 3:
                        return "radish"
                if bot_left_rect.collidepoint(event.pos):
                    pass
                if bot_right_rect.collidepoint(event.pos):
                    pass
                if leave_rect.collidepoint(event.pos):
                    return "town"

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

        global party
        pygame.draw.rect(screen, color_passive, title_rect)
        drawText(screen, "Who would you like to speak to?", (255,255,255), title_rect, base_font)
        pygame.draw.rect(screen, color_top_left, top_left_rect)
        drawText(screen, "Bear N. Steen", (255,255,255), top_left_rect, base_font)
        pygame.draw.rect(screen, color_top_right, top_right_rect)
        if in_party("Radish"):
            drawText(screen, "Radish Rabbit", (255,255,255), top_right_rect, base_font)
        else:
            drawText(screen, "???", (255,255,255), top_right_rect, base_font)
        pygame.draw.rect(screen, color_bot_left, bot_left_rect)
        if in_party("Name"):
            drawText(screen, "Not Found", (255,255,255), bot_left_rect, base_font)
        else:
            drawText(screen, "???", (255,255,255), bot_left_rect, base_font)
        pygame.draw.rect(screen, color_bot_right, bot_right_rect)
        if in_party("Name"):
            drawText(screen, "Not Found", (255,255,255), bot_right_rect, base_font)
        else:
            drawText(screen, "???", (255,255,255), bot_right_rect, base_font)
        pygame.draw.rect(screen, color_leave, leave_rect)
        drawText(screen, "Leave", (255,255,255), leave_rect, base_font)


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



def in_party(name):
    global party
    for member in party:
        if member.get_name() == name:
            return True
    return False

def controller():
    global name_global
    global progress
    progress = 1
    while True:
        option = start_screen()
        if option == "dialog":
            in_dialog()
        elif option == "dialog skip":
            name_global = "Dan"
            in_dialog("To Town")
        elif option == "exit":
            sys.exit()

def draw_start_screen(color_start, color_town_start, color_options, color_exit):
    gl_text("BLACK", width-1100, width-600, height-750, height-800, "Creatures of Habbitt", 1, 1)
    gl_text(color_start, width-900, width-700, height-500, height-550, "Start", 1, 1)
    gl_text(color_town_start, width-900, width-700, height-425, height-475, "Skip to Town", 1, 1)
    gl_text(color_options, width-900, width-700, height-350, height-400, "Options", 1, 1)
    gl_text(color_exit, width-850, width-750, height-200, height-250, "Exit", 1, 1)

if __name__ == "__main__":
    print(os.getcwd())
    controller()



