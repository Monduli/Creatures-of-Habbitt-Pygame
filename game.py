import sys, pygame
import dialog as dia

def drawText(surface, text, color, rect, font, aa=False, bkg=None, center=False):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = 0

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
            color_start = pygame.Color(200,200,200)
        if options_rect.collidepoint(pygame.mouse.get_pos()):
            color_options = pygame.Color(200,200,200)
        if exit_rect.collidepoint(pygame.mouse.get_pos()):
            color_exit = pygame.Color(200,200,200)

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
    user_text = dia.dialog_1

    dialog_rect = pygame.Rect(width-1550,height-250,1500,200)
    color_passive = pygame.Color('black')

    i = 0
    advance = 0
    exit_next = 0

    while True:
        screen.fill(black)
        screen.blit(background, (width+i,0))
        screen.blit(background, (i, 0))

        if (i == -width):
            screen.blit(background, (width+i, 0))
            i=0
        i-=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dialog_rect.collidepoint(event.pos):
                    if exit_next == 1:
                        sys.exit()
                    elif 0 <= advance+1 < len(user_text):
                        advance += 1
                    else:
                        user_text = ["End of text."]
                        exit_next = 1
                        advance = 0

        pygame.draw.rect(screen, color_passive, dialog_rect)
        #text_surface = base_font.render(user_text, True, (255,255,255))
        #screen.blit(text_surface, (input_rect.x+20, input_rect.y+20))
        #input_rect.w = max(1500, text_surface.get_width()+10)
        drawText(screen, user_text[advance], (255,255,255), dialog_rect, base_font)

        pygame.display.update()
        clock.tick(60)

def controller():
    while True:
        option = start_screen()
        if option == "dialog":
            in_dialog()
        elif option == "exit":
            sys.exit()

if __name__ == "__main__":
    controller()



