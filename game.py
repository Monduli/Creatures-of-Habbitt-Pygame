import sys, pygame
pygame.init()

size = width, height = 1600, 900
speed = [3, 0]
black = 0, 0, 0

clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)

background = pygame.image.load("cave.png")
background = pygame.transform.scale(background,(1600,900))

base_font = pygame.font.Font("VCR.001.ttf", 32)
user_text = "Welcome to Dan's character generator, undecided project version .001. Next To-Do: finish making the text advance when you click on the box."

input_rect = pygame.Rect(width-1550,height-250,1500,200)
color_passive = pygame.Color('black')

i = 0
advance = False

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
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

        surface.blit(image, (rect.left+20, y+10))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

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
            if input_rect.collidepoint(event.pos):
                advance = True
            else:
                advance = False

    pygame.draw.rect(screen, color_passive, input_rect)
    #text_surface = base_font.render(user_text, True, (255,255,255))
    #screen.blit(text_surface, (input_rect.x+20, input_rect.y+20))
    #input_rect.w = max(1500, text_surface.get_width()+10)
    drawText(screen, user_text, (255,255,255), input_rect, base_font)
    advance = False

    pygame.display.update()
    clock.tick(60)



