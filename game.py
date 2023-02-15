import sys, pygame
import dialog as dia
import classes

def drawText(surface, text, color, rect, font, aa=False, bkg=None, center=False, input=False):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = 0
    image = None

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        text_rect = image.get_rect()
        if center == True:
            text_rect.center = rect.center
            surface.blit(image, text_rect)
        else:
            surface.blit(image, (rect.left+20, y+10))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    if input == True:
        return image
    return text

def start_screen():

    #### SETUP ####
    pygame.init()

    size = width, height = 1600, 900
    black = 0, 0, 0
    speed = [3, 0]

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size)

    base_font = pygame.font.Font("VCR.001.ttf", 32)

    color_passive = pygame.Color('black')

    background = pygame.image.load("cave.png")
    background = pygame.transform.scale(background,(1600,900))

    title_rect = pygame.Rect(width-1000,height-800,400,50)
    start_rect = pygame.Rect(width-900,height-550,200,50)
    options_rect = pygame.Rect(width-900,height-400,200,50)
    exit_rect = pygame.Rect(width-850,height-250,100,50)

    i = 0

    while True:
        screen.fill(black)
        screen.fill(black)
        screen.blit(background, (width+i,0))
        screen.blit(background, (i, 0))
        color_start = pygame.Color('black')
        color_options = pygame.Color('black')
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
                if exit_rect.collidepoint(event.pos):
                    return "exit"

        if start_rect.collidepoint(pygame.mouse.get_pos()):
            color_start = pygame.Color(200,0,0)
        if options_rect.collidepoint(pygame.mouse.get_pos()):
            color_options = pygame.Color(200,0,0)
        if exit_rect.collidepoint(pygame.mouse.get_pos()):
            color_exit = pygame.Color(200,0,0)

        # Draw buttons
        pygame.draw.rect(screen, color_passive, title_rect)
        pygame.draw.rect(screen, color_start, start_rect)
        pygame.draw.rect(screen, color_options, options_rect)
        pygame.draw.rect(screen, color_exit, exit_rect)
        
        # Draw the text onto the buttons
        drawText(screen, "Dan's Game v.00", pygame.Color(255,255,255,0), title_rect, base_font, False, None, center=True)
        drawText(screen, "Wake Up", pygame.Color(255,255,255,0), start_rect, base_font, False, None, center=True)
        drawText(screen, "Options", pygame.Color(255,255,255,0), options_rect, base_font, False, None, center=True)
        drawText(screen, "Exit", pygame.Color(255,255,255,0), exit_rect, base_font, False, None, center=True)

        pygame.display.update()
        clock.tick(60)

def in_dialog():

    #### SETUP ####
    size = width, height = 1600, 900
    speed = [3, 0]
    black = 0, 0, 0

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size)

    background = pygame.image.load("cave.png")
    background = pygame.transform.scale(background,(1600,900))

    base_font = pygame.font.Font("VCR.001.ttf", 32)
    user_text = dia.dialog_start

    dialog_rect = pygame.Rect(width-1550,height-250,1500,200)
    color_passive = pygame.Color('black')

    i = 0
    advance = 0
    exit_next = 0
    move = True

    while True:
        screen.fill(black)
        screen.blit(background, (width+i,0))
        screen.blit(background, (i, 0))

        if move == True:
            if (i == -width):
                screen.blit(background, (width+i, 0))
                i=0
            i-=1
        else:
            screen.blit(background, (width, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dialog_rect.collidepoint(event.pos):
                    background, move = determine_background(user_text[0][advance], background, move)
                    if exit_next == 1:
                        sys.exit()
                    elif user_text[0][advance] == "Please select an option.":
                        choice = dialog_options(screen, user_text[0][advance+1], user_text[0][advance+2], user_text[1], user_text[2], background)
                        proceed = sort_options(choice)
                        user_text = dia.determine_dialog(choice)
                        advance = 0
                    elif user_text[0][advance] == "Please type into the box.":
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

        pygame.draw.rect(screen, color_passive, dialog_rect)
        #text_surface = base_font.render(user_text, True, (255,255,255))
        #screen.blit(text_surface, (input_rect.x+20, input_rect.y+20))
        #input_rect.w = max(1500, text_surface.get_width()+10)
        drawText(screen, user_text[0][advance], (255,255,255), dialog_rect, base_font)

        pygame.display.update()
        clock.tick(60)

def dialog_options(screen, text_left, text_right, target_left, target_right, background):
    size = width, height = 1600, 900
    clock = pygame.time.Clock()
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    base_font = pygame.font.Font("VCR.001.ttf", 32)

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


def input_box(target, background):
    size = width, height = 1600, 900
    clock = pygame.time.Clock()
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    base_font = pygame.font.Font("VCR.001.ttf", 32)

    color_passive = pygame.Color('black')

    i = 0

    user_text = ''
    
    # create rectangle
    input_rect = pygame.Rect(width-750, height/2, 200, 50)
    input_rect.center = (width/2, height/2)
    
    
    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = pygame.Color('red')
    
    # color_passive store color(chartreuse4) which is
    # color of input box.
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
                    return [dia.determine_dialog(target, user_text[:-1]), user_text[:-1]]
    
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
        background = pygame.image.load("forest.png")
        background = pygame.transform.scale(background,(1600,900))
        return background, True
    if dialog == "Maybe you should just follow that road over there until you run into something.":
        background = pygame.image.load("village.jpg")
        background = pygame.transform.scale(background,(1600,900))
        return background, False
    else:
        return bg, move

def controller():
    global name_global
    while True:
        option = start_screen()
        if option == "dialog":
            in_dialog()
        elif option == "exit":
            sys.exit()

if __name__ == "__main__":
    controller()



