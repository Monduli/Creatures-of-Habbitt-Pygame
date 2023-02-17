import pygame

def retrieve_background(choice):
    if choice == "cave":
        background = pygame.image.load("cave.png")
        background = pygame.transform.scale(background,(1600,900))
        return background
    elif choice == "forest":
        background = pygame.image.load("forest.png")
        background = pygame.transform.scale(background,(1600,900))
        return background
    elif choice == "village":
        background = pygame.image.load("village.jpg")
        background = pygame.transform.scale(background,(1600,900))
        return background

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
