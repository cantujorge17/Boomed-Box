import pygame
import os

pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Boomed Box")

#Program Constants
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
BG = (107, 186 ,255)
EMPTY_ID = -1
SPACE_ID = 0
CRATE_ID = 1
TNT_ID = 2
NOT_TNT_ID = 3
QUEUE_SPACE = 60
QUEUE_Y_OFFSET = 490
TITLE_FONT = pygame.font.SysFont("comicsans", 30, 1)
TEXT_FONT = pygame.font.SysFont("comicsans", 20)

#Images
GRID_IMAGE = pygame.image.load(os.path.join("Sprites", "Grid.png"))
CRATE_IMAGE = pygame.image.load(os.path.join("Sprites", "Crate.png"))
TNT_IMAGE = pygame.image.load(os.path.join("Sprites", "TNT (1).png"))
NOT_TNT_IMAGE = pygame.image.load(os.path.join("Sprites", "Not TNT (1).png"))
TNT_EXPLOSION_IMAGE = pygame.image.load(os.path.join("Sprites", "Explosion (1).png"))
NOT_TNT_EXPLOSION_IMAGE = pygame.image.load(os.path.join("Sprites", "Explosion (2).png"))
BOX_IMAGE = pygame.image.load(os.path.join("Sprites", "Box.png"))
TITLE_IMAGE = pygame.image.load(os.path.join("Sprites", "Title.png"))
BACKGROUND_IMAGE = pygame.image.load(os.path.join("Sprites", "Background.png"))

#Sprites
GRID = pygame.transform.scale(GRID_IMAGE, (64, 64))
CRATE = pygame.transform.scale(CRATE_IMAGE, (48, 48))
TNT = pygame.transform.scale(TNT_IMAGE, (48, 48))
NOT_TNT = pygame.transform.scale(NOT_TNT_IMAGE, (48, 48))
TNT_EXPLOSION = pygame.transform.scale(TNT_EXPLOSION_IMAGE, (265, 265))
NOT_TNT_EXPLOSION = pygame.transform.scale(NOT_TNT_EXPLOSION_IMAGE, (265, 265))
BOX = pygame.transform.scale(BOX_IMAGE, (300, 200))
TITLE = pygame.transform.scale(TITLE_IMAGE, (320, 240))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (603, 603))

#Sound Effects
CLICK_SOUND = pygame.mixer.Sound(os.path.join("Sound Effects", "Click.wav"))
CRATE_SOUND = pygame.mixer.Sound(os.path.join("Sound Effects", "Crate.wav"))
WIN_SOUND = pygame.mixer.Sound(os.path.join("Sound Effects", "Win.wav"))
LOSE_SOUND = pygame.mixer.Sound(os.path.join("Sound Effects", "Lose.wav"))
TNT_SOUND = pygame.mixer.Sound(os.path.join("Sound Effects", "TNT.wav"))
NOT_TNT_SOUND = pygame.mixer.Sound(os.path.join("Sound Effects", "Not TNT.wav"))
BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join("Sound Effects", "Background.wav"))

#Grid Variables
objectList = []
currentGrid = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
currentLevel = 1
levelCondition = 0
mainMenu = True
conditionSound = True
LEVEL_SIZE = 6
LEVEL_OFFSET = 80
GRID_OFFSET = 75
CRATE_OFFSET = 8
TNT_OFFSET = 8
COLOR = (0, 0, 0)

#The main function
def main():
    global levelCondition
    global currentLevel
    global mainMenu
    global conditionSound
    run = True
    clock = pygame.time.Clock()
    BACKGROUND_MUSIC.play(-1)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mainMenu:
                    CLICK_SOUND.play()
                    mainMenu = False
                    load_level(currentLevel)
                else:
                    if currentLevel >= 21:
                        CLICK_SOUND.play()
                        currentLevel = 1
                        mainMenu = True
                    if levelCondition == 0 and len(objectList) > 0:
                        validClick = clicked(objectList[0])
                        if validClick:
                            objectList.pop(0)
                        levelCondition = check_grid()
                    else:
                        conditionSound = True
                        if levelCondition == 1:
                            CLICK_SOUND.play()
                            currentLevel += 1
                            load_level(currentLevel)
                        if levelCondition == -1:
                            CLICK_SOUND.play()
                            load_level(currentLevel)
                        levelCondition = 0
            if event.type == pygame.KEYDOWN:
                if mainMenu:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                else:
                    if event.key == pygame.K_r:
                        if levelCondition == 0:
                            load_level(currentLevel)
                    if event.key == pygame.K_RIGHT and currentLevel < 20:
                        if levelCondition == 0:
                            currentLevel += 1
                            load_level(currentLevel)
                    if event.key == pygame.K_LEFT:
                        if levelCondition == 0 and currentLevel > 0 and currentLevel <= 20:
                            currentLevel -= 1
                            load_level(currentLevel)
                    if event.key == pygame.K_ESCAPE and currentLevel <= 20:
                        mainMenu = True
        if mainMenu:
            draw_main_menu()
        else:
            draw_window()
    pygame.quit()

def draw_main_menu():
    WIN.fill(BG)
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(TITLE, (140, 20))
    startText = TEXT_FONT.render("Click to play", 1, COLOR)
    WIN.blit(startText, (250, 400))
    pygame.display.update()

#Displays the level
def draw_window():
    global levelCondition
    WIN.fill(BG)
    WIN.blit(BACKGROUND, (0, 0))
    draw_grid()
    fill_grid()
    draw_queue()
    draw_text()
    if levelCondition != 0:
        draw_condition(levelCondition)
    #if(len(objectList) > 0):
        #draw_pointer(objectList[0])
    pygame.display.update()

#Display the grid
def draw_grid():
    for y in range(LEVEL_SIZE):
        for x in range(LEVEL_SIZE):
            if(currentGrid[y][x] != EMPTY_ID):
                xpos = LEVEL_OFFSET + (x * GRID_OFFSET)
                ypos = LEVEL_OFFSET + (y * GRID_OFFSET)
                WIN.blit(GRID, (xpos, ypos))

#Displays the objects in the grid
def fill_grid():
    for y in range(LEVEL_SIZE):
        for x in range(LEVEL_SIZE):
            xpos = LEVEL_OFFSET + (x * GRID_OFFSET)
            ypos = LEVEL_OFFSET + (y * GRID_OFFSET)
            if currentGrid[y][x] == CRATE_ID:
                WIN.blit(CRATE, (xpos  + CRATE_OFFSET, ypos  + CRATE_OFFSET))
            elif currentGrid[y][x] == TNT_ID:
                WIN.blit(TNT, (xpos + TNT_OFFSET, ypos + TNT_OFFSET))
            elif currentGrid[y][x] == NOT_TNT_ID:
                WIN.blit(NOT_TNT, (xpos + TNT_OFFSET, ypos + TNT_OFFSET))

#Add an object to the grid
def clicked(object):
    last_mouse_x, last_mouse_y = pygame.mouse.get_pos()
    x = (last_mouse_x - LEVEL_OFFSET) // GRID_OFFSET
    y = (last_mouse_y - LEVEL_OFFSET) // GRID_OFFSET
    if x < LEVEL_SIZE and x >= 0 and y < LEVEL_SIZE and y >= 0 and currentGrid[y][x] == 0:
        currentGrid[y][x] = object
        if object == TNT_ID:
            tnt_action(x, y)
        elif object == NOT_TNT_ID:
            not_tnt_action(x, y)
        elif object == CRATE_ID:
            CRATE_SOUND.play()
        return True
    return False
    
#Blow up the crates
def tnt_action(x, y):
    fill_grid()
    pygame.display.update()
    pygame.time.delay(200)
    if (y - 1) >= 0 and (x - 1) >= 0 and currentGrid[y - 1][x - 1] != EMPTY_ID:
        currentGrid[y - 1][x - 1] = SPACE_ID
    if (y - 1) >= 0 and currentGrid[y - 1][x] != EMPTY_ID:
        currentGrid[y - 1][x] = SPACE_ID
    if (y - 1) >= 0 and (x + 1) < LEVEL_SIZE and currentGrid[y - 1][x + 1] != EMPTY_ID:
        currentGrid[y - 1][x + 1] = SPACE_ID
    if (x - 1) >= 0 and currentGrid[y][x - 1] != EMPTY_ID:
        currentGrid[y][x - 1] = SPACE_ID
    if (x + 1) < LEVEL_SIZE and currentGrid[y][x + 1] != EMPTY_ID:
        currentGrid[y][x + 1] = SPACE_ID
    if (y + 1) < LEVEL_SIZE and (x - 1) >= 0 and currentGrid[y + 1][x - 1] != EMPTY_ID:
        currentGrid[y + 1][x - 1] = SPACE_ID
    if (y + 1) < LEVEL_SIZE and currentGrid[y + 1][x] != EMPTY_ID:
        currentGrid[y + 1][x] = SPACE_ID
    if (y + 1) < LEVEL_SIZE and (x + 1) < LEVEL_SIZE and currentGrid[y + 1][x + 1] != EMPTY_ID:
        currentGrid[y + 1][x + 1] = SPACE_ID
    currentGrid[y][x] = SPACE_ID

    #Show explosion
    xpos = LEVEL_OFFSET + (x * GRID_OFFSET) - 100
    ypos = LEVEL_OFFSET + (y * GRID_OFFSET) - 100
    TNT_SOUND.play()
    WIN.blit(TNT_EXPLOSION, (xpos, ypos))
    pygame.display.update()
    pygame.time.delay(300)

#Explosion creates crates, unless there is already a crate around the "tnt"
def not_tnt_action(x, y):
    fill_grid()
    pygame.display.update()
    pygame.time.delay(200)
    if (y - 1) >= 0 and (x - 1) >= 0 and currentGrid[y - 1][x - 1] != EMPTY_ID:
        if currentGrid[y - 1][x - 1] == CRATE_ID:
            currentGrid[y - 1][x - 1] = SPACE_ID
        else:
            currentGrid[y - 1][x - 1] = CRATE_ID
    if (y - 1) >= 0 and currentGrid[y - 1][x] != EMPTY_ID:
        if currentGrid[y - 1][x] == CRATE_ID:
            currentGrid[y - 1][x] = SPACE_ID
        else:
            currentGrid[y - 1][x] = CRATE_ID
    if (y - 1) >= 0 and (x + 1) < LEVEL_SIZE and currentGrid[y - 1][x + 1] != EMPTY_ID:
        if currentGrid[y - 1][x + 1] == CRATE_ID:
            currentGrid[y - 1][x + 1] = SPACE_ID
        else:
            currentGrid[y - 1][x + 1] = CRATE_ID
    if (x - 1) >= 0 and currentGrid[y][x - 1] != EMPTY_ID:
        if currentGrid[y][x - 1] == CRATE_ID:
            currentGrid[y][x - 1] = SPACE_ID
        else:
            currentGrid[y][x - 1] = CRATE_ID
    if (x + 1) < LEVEL_SIZE and currentGrid[y][x + 1] != EMPTY_ID:
        if currentGrid[y][x + 1] == CRATE_ID:
            currentGrid[y][x + 1] = SPACE_ID
        else:
            currentGrid[y][x + 1] = CRATE_ID
    if (y + 1) < LEVEL_SIZE and (x - 1) >= 0 and currentGrid[y + 1][x - 1] != EMPTY_ID:
        if currentGrid[y + 1][x - 1] == CRATE_ID:
            currentGrid[y + 1][x - 1] = SPACE_ID
        else:
            currentGrid[y + 1][x - 1] = CRATE_ID
    if (y + 1) < LEVEL_SIZE and currentGrid[y + 1][x] != EMPTY_ID:
        if currentGrid[y + 1][x] == CRATE_ID:
            currentGrid[y + 1][x] = SPACE_ID
        else:
            currentGrid[y + 1][x] = CRATE_ID
    if (y + 1) < LEVEL_SIZE and (x + 1) < LEVEL_SIZE and currentGrid[y + 1][x + 1] != EMPTY_ID:
        if currentGrid[y + 1][x + 1] == CRATE_ID:
            currentGrid[y + 1][x + 1] = SPACE_ID
        else:
            currentGrid[y + 1][x + 1] = CRATE_ID
    currentGrid[y][x] = SPACE_ID

    #Show explosion
    xpos = LEVEL_OFFSET + (x * GRID_OFFSET) - 100
    ypos = LEVEL_OFFSET + (y * GRID_OFFSET) - 100
    NOT_TNT_SOUND.play()
    WIN.blit(NOT_TNT_EXPLOSION, (xpos, ypos))
    pygame.display.update()
    pygame.time.delay(300)

#Selected object follows the cursor
def draw_pointer(object):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if object == TNT_ID:
        WIN.blit(TNT, (mouse_x - 16, mouse_y - 24))
    elif object == NOT_TNT_ID:
        WIN.blit(NOT_TNT, (mouse_x - 16, mouse_y - 24))
    elif object == CRATE_ID:
        WIN.blit(CRATE, (mouse_x - 24, mouse_y - 24))

#Draws the objects in the queue
def draw_queue():
    if len(objectList) > 0:
        i = 0
        while i < len(objectList):
            yPos = QUEUE_Y_OFFSET - i * QUEUE_SPACE
            if objectList[i] == CRATE_ID:
                WIN.blit(CRATE, (10, yPos))
            elif objectList[i] == TNT_ID:
                WIN.blit(TNT, (10, yPos))
            elif objectList[i] == NOT_TNT_ID:
                WIN.blit(NOT_TNT, (10, yPos))
            i += 1

#Draws text in the bottom of certain levels
def draw_text():
    if currentLevel >= 0 and currentLevel <= 20:
        levelText = TITLE_FONT.render(("Level " + str(currentLevel)), 1, COLOR)
        WIN.blit(levelText, (250, 10))
    if currentLevel == 1:
        tutorialText = TEXT_FONT.render("Use the TNT to blow up the crates", 1, COLOR)
        WIN.blit(tutorialText, (140, 550))
    if currentLevel == 2:
        tutorialText = TEXT_FONT.render("The bar on the left shows total items to complete the level", 1, COLOR)
        WIN.blit(tutorialText, (20, 550))
    if currentLevel == 3:
        tutorialText = TEXT_FONT.render("Press R to restart the level", 1, COLOR)
        WIN.blit(tutorialText, (170, 550))
    if currentLevel == 5:
        tutorialText = TEXT_FONT.render("Crates added to the grid must be destroyed as well", 1, COLOR)
        WIN.blit(tutorialText, (60, 550))
    if currentLevel == 6:
        tutorialText = TEXT_FONT.render("If you destroy all the crates before placing one, you still win", 1, COLOR)
        WIN.blit(tutorialText, (15, 550))
    if currentLevel == 9:
        tutorialText = TEXT_FONT.render("Use the right arrow key to skip a level if you get stuck", 1, COLOR)
        WIN.blit(tutorialText, (40, 550))
    if currentLevel == 11:
        tutorialText = TEXT_FONT.render("\"TNT\" adds crates instead of destroying crates", 1, COLOR)
        WIN.blit(tutorialText, (70, 550))
    if currentLevel == 12:
        tutorialText = TEXT_FONT.render("The force of \"TNT\" will break crates next to the explosion", 1, COLOR)
        WIN.blit(tutorialText, (20, 550))
    if currentLevel == 13:
        tutorialText = TEXT_FONT.render("You will need to be smart with your use of \"TNT\"", 1, COLOR)
        WIN.blit(tutorialText, (70, 550))
    if currentLevel >= 21:
        winText = TITLE_FONT.render("You beat the game!", 1, COLOR)
        screenTextOne = TEXT_FONT.render("Click to go back", 1, COLOR)
        screenTextTwo = TEXT_FONT.render("to the main menu", 1, COLOR)
        WIN.blit(winText, (160, 180))
        WIN.blit(screenTextOne, (230, 350))
        WIN.blit(screenTextTwo, (225, 380))

#Draws if a player won or lost a level
def draw_condition(condition):
    global conditionSound
    if condition == 1:
        if  conditionSound:
            WIN_SOUND.play()
            conditionSound = False
        winText = TITLE_FONT.render("Level Complete", 1, COLOR)
        clickText = TEXT_FONT.render("Click for next level", 1, COLOR)
        WIN.blit(BOX, (150, 190))
        WIN.blit(winText, (195, 230))
        WIN.blit(clickText, (215, 320))
    if condition == -1:
        if conditionSound:
            LOSE_SOUND.play()
            conditionSound = False
        loseText = TITLE_FONT.render("Level Failed", 1, COLOR)
        clickText = TEXT_FONT.render("Click to restart", 1, COLOR)
        WIN.blit(BOX, (150, 190))
        WIN.blit(loseText, (216, 230))
        WIN.blit(clickText, (233, 310))

#Checks to see if the board has been cleared
def check_grid():
    winCondition = 0
    for y in range(LEVEL_SIZE):
        for x in range(LEVEL_SIZE):
            if currentGrid[y][x] == CRATE_ID:
                winCondition += 1
    if winCondition == 0:
        return 1
    elif winCondition > 0 and len(objectList) <= 0:
        return -1
    return 0

#Assigns the grid to a certain level
def load_level(level):
    global currentGrid
    if level == 0:
        currentGrid = [[-1, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, -1]]
    if level == 1:
        currentGrid = [[-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, 1, 0, -1, -1], [-1, -1, 0, 1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1]]
    if level == 2:
        currentGrid = [[-1, -1, -1, -1, -1, -1], [-1, 1, 1, 1, 1, -1], [-1, 1, 0, 0, 1, -1], [-1, 1, 0, 0, 1, -1], [-1, 1, 1, 1, 1, -1], [-1, -1, -1, -1, -1, -1]]
    if level == 3:
        currentGrid = [[-1, -1, -1, -1, -1, -1], [-1, 1, 0, 1, 0, -1], [-1, 0, 0, 0, 1, -1], [-1, 1, 0, 1, 0, -1], [-1, 0, 0, 0, 1, -1], [-1, -1, -1, -1, -1, -1]]
    if level == 4:
        currentGrid = [[-1, -1, -1, -1, -1, -1], [0, 0, 0, 0, 1, 0], [0, 1, 1, 0, 0, 0], [1, 0, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0], [-1, -1, -1, -1, -1, -1]]
    if level == 5:
        currentGrid = [[-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, 1, 0, -1, -1], [-1, -1, 0, 0, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1]]
    if level == 6:
        currentGrid = [[-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, 1, -1], [-1, -1, 1, 0, -1, -1], [-1, -1, 1, 1, -1, -1], [-1, 1, -1, -1, 1, -1], [-1, -1, -1, -1, -1, -1]]
    if level == 7:
        currentGrid = [[-1, -1, -1, -1, -1, -1], [-1, -1, 0, -1, 0, -1], [-1, 1, -1, 0, -1, -1], [-1, -1, 1, -1, 1, -1], [-1, 0, -1, 0, -1, -1], [-1, -1, -1, -1, -1, -1]]
    if level == 8:
        currentGrid = [[1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, 0]]
    if level == 9:
        currentGrid = [[0, 0, 1, -1, 0, 0], [0, 1, -1, 1, 0, 1], [0, 0, 1, -1, 0, 0], [0, 0, -1, 1, 0, 1], [0, 0, 1, -1, 0, 0], [1, 0, -1, 0, 0, 0]]
    if level == 10:
        currentGrid = [[-1, 0, 1, 1, 0, -1], [-1, 1, 1, 1, 1, -1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [-1, 1, 1, 1, 1, -1], [-1, 0, 1, 1, 0, -1]]
    if level == 11:
        currentGrid = [[-1, -1, -1, -1, -1, -1], [-1, -1, 1, 1, -1, -1], [-1, -1, 0, 0, -1, -1], [-1, -1, 0, 0, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1]]
    if level == 12:
        currentGrid = [[1, 1, 1, -1, -1, -1], [1, 0, 1, -1, -1, -1], [1, 1, 1, -1, -1, -1], [-1, -1, -1, 1, 1, 1], [-1, -1, -1, 1, 0, 1], [-1, -1, -1, 1, 1, 1]]
    if level == 13:
        currentGrid = [[-1, -1, -1, -1, -1, -1], [-1, 0, 0, 1, 0, -1], [-1, 1, 0, 1, 1, -1], [-1, 1, 0, 0, 0, -1], [-1, 1, 1, 1, 0, -1], [-1, -1, -1, -1, -1, -1]]
    if level == 14:
        currentGrid = [[-1, -1, -1, -1, -1, -1], [0, 1, 0, 1, 0, 1], [-1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, 0], [1, 0, 1, 0, 1, 0], [-1, -1, -1, -1, -1, -1]]
    if level == 15:
        currentGrid = [[-1, 0, -1, -1, 1, -1], [0, 0, 0, 0, 1, 0], [1, 1, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0], [-1, 0, 0, 0, 0, -1], [-1, -1, 1, 1, -1, -1]]
    if level == 16:
        currentGrid = [[0, 0, -1, -1, 0, 0], [0, 0, -1, -1, 0, 0], [-1, -1, 1, 1, -1, -1], [-1, -1, 1, 1, -1, -1], [0, 0, -1, -1, 0, 0], [0, 0, -1, -1, 0, 0]]
    if level == 17:
        currentGrid = [[1, -1, -1, 0, 0, 0], [0, -1, 0, 0, -1, 1], [0, -1, 0, -1, -1, -1], [0, -1, 0, 0, 0, 0], [0, -1, -1, -1, -1, 0], [0, 0, 0, 0, 0, 0]]
    if level == 18:
        currentGrid = [[0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0], [1, 0, 0, 0, 0, 0]]
    if level == 19:
        currentGrid = [[0, 0, 0, 0, -1, 1], [0, -1, 0, 0, 0, 0], [1, 0, 0, -1, 0, 0], [0, -1, 0, 0, 0, 0], [0, 0, 0, 0, -1, 0], [-1, 0, 0, 0, 1, 0]]
    if level == 20:
        currentGrid = [[-1, -1, 0, 0, -1, -1], [-1, 0, 0, 1, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, -1], [-1, 0, -1, -1, 0, -1]]
    if level >= 21:
        currentGrid = [[1, 1, 1, 1, 1, 1], [1, -1, -1, -1, -1, 1], [1, -1, -1, -1, -1, 1], [1, -1, -1, -1, -1, 1], [1, -1, -1, -1, -1, 1], [1, 1, 1, 1, 1, 1]]
    fill_list()

#Fills the list with the objects to be used in the levels
def fill_list():
    global objectList
    if currentLevel == 0:
        objectList = [3, 2, 2]
    if currentLevel == 1:
        objectList = [2]
    if currentLevel == 2:
        objectList = [2, 2, 2, 2]
    if currentLevel == 3:
        objectList = [2, 2]
    if currentLevel == 4:
        objectList = [2, 2]
    if currentLevel == 5:
        objectList = [1, 2]
    if currentLevel == 6:
        objectList = [2, 2, 2, 1]
    if currentLevel == 7:
        objectList = [1, 2, 2]
    if currentLevel == 8:
        objectList = [1, 1, 2, 2, 1, 2]
    if currentLevel == 9:
        objectList = [1, 2, 2, 1, 2, 2]
    if currentLevel == 10:
        objectList = [1, 1, 2, 2, 2, 2, 2, 2]
    if currentLevel == 11:
        objectList = [3, 2, 2]
    if currentLevel == 12:
        objectList = [3, 3]
    if currentLevel == 13:
        objectList = [3, 3, 2]
    if currentLevel == 14:
        objectList = [3, 3, 1, 3, 3]
    if currentLevel == 15:
        objectList = [3, 2, 2]
    if currentLevel == 16:
        objectList = [3, 2, 1, 3]
    if currentLevel == 17:
        objectList = [3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 3]
    if currentLevel == 18:
        objectList = [3, 3, 3, 2, 2, 2]
    if currentLevel == 19:
        objectList = [1, 3, 1, 3, 2, 2]
    if currentLevel == 20:
        objectList = [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3]
    if currentLevel >= 21:
        objectList = [0]

#Goes to main
if __name__ == "__main__":
    main()