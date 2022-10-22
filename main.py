from imports import *

# Initializes the game engine 🟢  🏎💨
pg.init()

# Set rate of which our python clock will tick per second
clock_rate = 60

# Settings the window properties and creating a game screen
WIDTH = 1000
HEIGHT = 666
CANVAS = (WIDTH, HEIGHT)
screen = pg.display.set_mode(CANVAS)
# Window title
pg.display.set_caption("LLUVIA")
# Window Icon
icon = pg.image.load("assets/icon.png")
pg.display.set_icon(icon)
# Clock object
clock = pg.time.Clock()
# Create a background
background = pg.image.load("assets/background.png").convert()

# Game sounds
popped_sound = pg.mixer.Sound("assets/pop.wav")
highscore_sound = pg.mixer.Sound("assets/highscore.wav")
lose_life_sound = pg. mixer.Sound("assets/loselife.wav")

# Text 
font = pg.font.Font('assets/font.ttf', 27)
score_font = pg.font.Font('assets/font.ttf', 16)
game_over_font = pg.font.Font('assets/font.ttf', 100)
subGameOverFont = pg.font.Font('assets/font.ttf', 50)

# Set's the difficulty of the game
DIFFICULTY_TIMER = 750

# Creates custom events that we call broadcast once the timer resets
NUMBER_DROPS_EVENT = pg.USEREVENT + 0
CLOUDS_EVENT = pg.USEREVENT + 1
HIGHSCORE_EVENT = pg.USEREVENT + 2

# These constants are to set the drops' radius, starting position, and speeds.
DROP_RADIUS = 15
DROP_STARTY = 0 + DROP_RADIUS * 2
DROP_SPEED = 1
# The popped speed is faster for esthethic effect
POPPED_SPEED = 6
# Keeps score of how many drops we will draw to the screen per timer
number_drops = 1
# The drops change position is the drop's present position
drop_color = (31, 232, 104)
# Mark drop for deletion –– the one being a placeholder for the drop's position in array
do_delete = []
# Life points
lives = 3
# Score
points = 0

# Here we have an indicator whether the drop is popped, the color of the popped drop,
# And where the drop was popped to print our text and fade away.
poppedColorOne = [(43, 217, 255), (255, 215, 0)]
poppedColorTwo = [(56, 114, 255), (255, 215, 0)]
poppedFontColor = [(5, 199, 242), (255, 215, 0)]
change_color = 0

# Creating an dict to kinda organize all drops and their properties into one place
drops = {    "startX": [],
            "changeX": [],
            "changeY": [],
              "alpha": [],
          "is_popped": [],
    "popped_position": [],
        "popped_font": []}

# Assigning properties to each individual drop
# Rain Drop properties that we will be modifying
pg.time.set_timer(NUMBER_DROPS_EVENT, DIFFICULTY_TIMER)

# Cloud properties
MAX_CLOUDS = 3
CLOUD_MOVE = 36
pg.time.set_timer(CLOUDS_EVENT, 2000)
clouds = {"cloudImg": [],
            "cloudX": [36, 332, 628],
            "cloudY": []}

# Setting properties for each cloud for however many clouds we decide to show
for i in range(MAX_CLOUDS):
    clouds["cloudImg"].append(pg.image.load("assets/clouds.png"))
    clouds["cloudY"].append(0)

# Displays the scores and lives
def show_score(fColor):
    score = score_font.render(f"SCORE: {str(points)}", True, fColor)
    life = score_font.render(f"LIFE: {str(lives)}", True, (255, 255, 255))
    screen.blit(score, (15, 333))
    screen.blit(life, (15, 363))


# Game over screen
def gameover():
    end = game_over_font.render("GAMEOVER", True, (255, 0, 0))
    netScore = subGameOverFont.render(f"SCORE: {points}", True, (255, 255, 255))
    screen.blit(end, (110, 250))
    screen.blit(netScore, (275, 400))

# Here we prepare how the user's score will be saved
def writeScore():
    with open("highscores.txt", "w") as file:
        file.write(str(points))
def readScore():
    with open("highscores.txt", "r") as file:
        return int(file.read())
highscore = readScore()
pg.time.set_timer(HIGHSCORE_EVENT, 100)


# Create drops
def createDrops():
    global number_drops
    # A fresh spawn for all our new drops
    drops["startX"].clear()

    drops["startX"].append(random.randint(0 + DROP_RADIUS * 2, WIDTH - DROP_RADIUS * 2))
    drops["changeX"].append(drops["startX"][0])
    drops["changeY"].append(DROP_STARTY)
    drops["alpha"].append(255)
    drops["is_popped"].append(False)
    drops["popped_position"].append((0, 0))
    drops["popped_font"].append(font.render("+1", True, poppedFontColor[0]))
    number_drops += 1
    


# Set up the drops to draw
def droplets(pCOne, pCTwo, pFC):
    global alpha, number_drops, change_color

    # I decided to go with coded circles because they seem faster than images 😊
    for i in range(len(drops["changeX"])):
        if not drops["is_popped"][i]:
            pg.draw.circle(screen, drop_color, (drops["changeX"][i], drops["changeY"][i]), DROP_RADIUS, 0)
        else:
            pg.draw.circle(screen, pCOne, (drops["changeX"][i] - 3, drops["changeY"][i] + 20), DROP_RADIUS / 4, 0)
            pg.draw.circle(screen, pCOne, (drops["changeX"][i] + 10, drops["changeY"][i] + 7), DROP_RADIUS / 4, 0)
            pg.draw.circle(screen, pCTwo, (drops["changeX"][i] - 5, drops["changeY"][i] + 2), DROP_RADIUS / 4, 0)
            pg.draw.circle(screen, pCTwo, (drops["changeX"][i] + 5, drops["changeY"][i] - 2), DROP_RADIUS / 4, 0)
            pg.draw.circle(screen, pCOne, (drops["changeX"][i], drops["changeY"][i] - 20), DROP_RADIUS / 4, 0)
            drops["popped_font"][i] = font.render("+1", True, pFC)
            # Here we fade the text
            if drops["alpha"][i] > 0:
                # Reduces the alpha of each frame and makes sure it doesn't go below 0
                drops["alpha"][i] -= 2.5
                # We set the alpha to the new alpha
                drops["popped_font"][i].set_alpha(drops["alpha"][i])
                # We draw the font inside the if statement to ensure we don't keep drawing a ghost font 👻🙅‍♂️
                screen.blit(drops["popped_font"][i], drops["popped_position"][i])


# We keep the drop moving downards until it's either popped or hits bottom
def motion():
    global lives
    # Here we'll esentially check for all items on the screen and their state
    for i in range(len(drops["changeY"])):
        # Maytee maytee we, the player, have been hit !! We lose a life :c 
        if drops["changeY"][i] >= 666 - DROP_RADIUS and not drops["is_popped"][i]:
            do_delete.append(i)
            lives -= 1
        
        # For any popped drops that just hit bottom, we must delete
        elif drops["changeY"][i] >= 666 - DROP_RADIUS and drops["is_popped"][i]:
            do_delete.append(i)

        # If the drops aren't popped and they haven't hit the ground yet,, ehh we'll be chillin 😎🆒
        elif drops["changeY"][i] < 666 - DROP_RADIUS and not drops["is_popped"][i]:
            drops["changeY"][i] += DROP_SPEED

        # The remaining out come is the popped drops that have not yet hit bottom
        else:
            drops["changeY"][i] += POPPED_SPEED

# Delete the drops 
def delete():
    global number_drops, do_delete

    for i in range(len(do_delete)):
        # We use this method of deletion for O(1) deletion instead of another loop
        del drops["changeX"][do_delete[i]]
        del drops["changeY"][do_delete[i]]
        del drops["alpha"][do_delete[i]]
        del drops["is_popped"][do_delete[i]]
        del drops["popped_position"][do_delete[i]]
        del drops["popped_font"][do_delete[i]]
        number_drops -= 1

    # Clear our deleted list
    do_delete.clear()
    

# Move the clouds
def cloudMove():
    for i in range(MAX_CLOUDS):
        if clouds["cloudX"][2] + 260 <= 888:
            clouds["cloudX"][i] += CLOUD_MOVE
        elif clouds["cloudX"][2] >= 664:
            clouds["cloudX"][i] -= CLOUD_MOVE



# Game loop
running = True
while running:

    # Draws the background to the screen
    screen.blit(background, (0, 0))

    # Let's read for events B)
    for event in pg.event.get():
        # Event for when the user quits
        if event.type == pg.QUIT:
            running = False

        # Event for when our drop timer goes off
        if event.type == NUMBER_DROPS_EVENT:
            createDrops()

        if event.type == CLOUDS_EVENT:
            cloudMove()

        if event.type == HIGHSCORE_EVENT and points > highscore and lives != 0:
            if change_color == 0:
                change_color == 1
            change_color += 1

        # Event for mouse clicks
        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()

            # Making a hitbox for our lil rain drops
            for i in range(len(drops["changeY"])):
                # I kinda see the hitbox as a changing range of positions where we check 
                # If the mouse is within that range
                if not drops["is_popped"][i]:

                    # LOL the variable names are really looking rough at this point... 😂
                    hit_box_x_start = drops["changeX"][i] - DROP_RADIUS
                    hit_box_y_start = drops["changeY"][i] - DROP_RADIUS
                    for y in range(DROP_RADIUS * 2):
                        for x in range(DROP_RADIUS * 2):
                        # When the click position is within the hit box, we will do something 
                            if pos == (hit_box_x_start + x, hit_box_y_start + y) and not drops["is_popped"][i]:
                                drops["is_popped"][i] = True
                                drops["popped_position"][i] = pos
                                points += 1
                                if points < highscore:
                                    popped_sound.play()
                                else:
                                    highscore_sound.play()

    # We'll keep running the same old tasks as long as the player is still alive
    if lives != 0:
        show_score(poppedFontColor[change_color % 2])

        # Rain falls down so we change the Y axis of each drop until it hits bottom
        # We loop through the dictionary instead of the number of drops to account for popped drops
        motion()


        # Draws the droplets, both unpopped and popped animations to the screen
        # Modula so we linger on each color before switching 
        droplets(poppedColorOne[change_color % 2], poppedColorTwo[change_color % 2], poppedFontColor[change_color % 2])

        # Deletes all drops marked for deletion from motion
        delete()
       
        # Here we draw all the clouds to the screen            
        for i in range(len(clouds["cloudImg"])):
            screen.blit(clouds["cloudImg"][i], (clouds["cloudX"][i], clouds["cloudY"][i]))
        

    # Otherwise, we'll end the game.
    else:
        gameover()
        if points > highscore:
            writeScore()


    # Updates the display
    pg.display.update()

    # We'll set the maximum rate of clock ticks per second to 60
    clock.tick(clock_rate)

# TODO: save the score
