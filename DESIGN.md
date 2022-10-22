# Design Decisions

## The Limitations
Before we dive right in, I should address some current unresolved bugs.
The first and so far only bug I have experienced is the hitbox failing to detect that a drop has been clicked. This only occurs, however, when there are a substantial amount of drops on the screen.

Therefore, because of these circumstances that the bug appears in, my intuition tells me to look at the hitboxes of the drop and the possibility that it may be taking too long to create some drop's hitboxes. So, when the user clicks on a drop, by chance, that part of the hitbox hasn't been developed or check yet. Ergo, the user has to keep clicking until the hitbox catches the pointer's click. (We will be getting into the specifics on how the hitbox and pointer are registered later on.)

Some solutions for this bug include either adding a delay once the mouse is pressed, giving more time for the hitbox to catch the location, or making the drops smaller, so it's less scanning the hitbox has to do. However, these are addressing the symptom and not necessarily the disease. 

A grounded solution, I think, would be to rewrite drops as an entirely different sprite. Unfortunately, I was made aware of this pygame feature far too recently to implement the entire change in time to turn it in. I do think that when pygame recognizes a sprite, it does so in a lot more efficient manner to create a hitbox. My hitbox was made with a very rough, hand-coded method. But the pygame sprite feature has a function to detect collision: [pygame.sprite.collide_rect()]

## The Game Window
Before presenting a game to the player, we must first present a window or canvas to show the player of a certain width and height. Thus in pygame, we create a constant variable called [CANVAS] where we store our [WIDTH] and [HEIGHT]. These will be our game window [screen = pg.display.set_mode(CANVAS)].

## Loading the Files
After creating the canvas, we set up the basic functionality of our game, such as a clock to keep track of time and set our refreshes per second, our background image, and sounds.

## Getting Started With Our Drop Variables
Our drops will be the core piece of this game, so they require a hefty amount of variables. We start off with the [DIFFICULTY_TIMER]. All this variable really stores is the countdown before showing the next drop appears. 

### Custom Events
So just how scratch has a broadcast feature, I kinda see events the same way. We can set various events that our game loop can listen for and do a specific action. 

I created three events for this project: [NUMBER_DROPS_EVENT], [CLOUDS_EVENT], and [HIGHSCORE_EVENT].



#### [NUMBER_DROPS_EVENT] 
Will be trigged using the subsequent [pg.time.set_timer(NUMBER_DROPS_EVENT, DIFFICULTY_TIMER)] on line 78. What this line does is essentially a function that will "broadcast" [NUMBER_DROPS_EVENT] every [DIFFICULTY_TIMER] second. And in our game loop, we have the [if event.type == NUMBER_DROPS_EVENT] condition. What [event.type] means a line from the for loop [for event in pg.event.get()] which essentially grabs all the custom events and pygame events like keypresses and mouse clicks. 

Once the event [NUMBER_DROPS_EVENT] occurs, we will call upon our function [createDrops()]. (And yes, I was kinda split between camel case for variables or functions, but decided to go with camel case, hehehe).

#### [CLOUDS_EVENT]
This event works similarly to the prior event but has its own timer. Once that timer [pg.time.set_timer(CLOUDS_EVENT, 2000)]. Once the event is called, we run the function [clouddMove()]

#### [HIGHSCORE_EVENT]
This event will be broadcasted similarly. However, when we check for this event with [if event.type == HIGHSCORE_EVENT and points > highscore and lives != 0] We are only checking this event if the user has surpassed the old high score and if indeed their lives are not zero (meaning they're not dead yet). 

In the case that all these conditions are true, then we can apply special color properties: 

if change_color == 0:
   change_color == 1
change_color += 1

The reason [change_color] is checking if it's equal to zero is that this variable is essentially the list location of the special yellow high score color that will be flashed once the player breaks their old record. Meaning, the drops, the popped drops, the popped number, and the score all have this list of colors that we could oscillate between the old blue and new gold color. (More on this later).

### How the drops are set up
Now, there are many ways I could have approached adding the drops to the screen. I was originally thinking of using an image of a raindrop that falls down. However, I realized that this image would get redrawn multiple times. That seemed very inefficient, especially if the image was a noticeable size.

This lead me to create the drops by mathimatically drawing them to the screen, which I presume is less demanding: 

pg.draw.circle(screen, drop_color, (drops["changeX"][i], drops["changeY"][i]), DROP_RADIUS, 0)

However, this does make collision detection a lot more complicated because I can't just state, "go to the image location and if the pointer is clicking the image, pop the drop". Let's dive in.

#### Before Creating the Drops
The aforementioned function draws the circle to the screen by taking in the screen parameter, the color of the drop, the location to draw, the desired radius, and the 0 tells the function to fill the circle. 

Now, the reasoning behind [drops["changeX"][i], drops["changeY][i]] is that all our drops that appear on the screen, whether popped or not popped, are lists apart of a dictionary. The dictionary being [drops] that holds keys or characteristics of a drop. If I were to be using C#, this is where I would have likely created a datatype. Anyhow, the keys consist of the starting/spawn x-axis location of the drop, the new position/change in the x-axis and y-axis, the alpha (which means the transparency... more on this later), whether the drop is popped, the position the drop was popped in, and the text to display when the drop is popped (which is dormant until summoned).

#### Creating the Drops [createDrops()]
To create the drops, we first summon the [createDrops()] function. I originally had this bug where a drop would appear at a location. The next drop would appear in the same exact x-axis as the prior drop and basically never move from that axis. This bug led me to realize that I actually had to clear all of the starting positions of the drops within the array once they appeared to set a new random starting location.

We append to the drop array the spawn of our new drops and their starting properties and increment our number_drops variable by 1.

#### Changing Drop colors [droplets()]!
What goes up must come down! And we do exactly that in [droplets(pCOne, pCTwo, pfC)]

Admittedly, this is probably the most cryptic line in my code, but also the most important. 

We start with a loop that doesn't loop over our number of drops variable [number_drops], but rather the number of falling drops. I took this subtle design leap because of the limitations of the [number_drops] variable. That is, the variable only counts the number of unpopped drops, but this function must account for all falling entities. So we get the number of entities in any key within our [drops] dict. 

Each entity has an ID number, which is it's list [i] position in each key value inside the dictionary [drops]. If the drop is not popped [if not drops["is_popped"][i]], we will just draw the drop and its location to the screen [pg.draw.circle(screen, drop_color, (drops["changeX"][i], drops["changeY"][i]), DROP_RADIUS, 0)].

On the other hand, if the drop is popped, then we will print our little pop animations:
   pg.draw.circle(screen, pCOne, (drops["changeX"][i] - 3, drops["changeY"][i] + 20), DROP_RADIUS / 4, 0)
   pg.draw.circle(screen, pCOne, (drops["changeX"][i] + 10, drops["changeY"][i] + 7), DROP_RADIUS / 4, 0)
   pg.draw.circle(screen, pCTwo, (drops["changeX"][i] - 5, drops["changeY"][i] + 2), DROP_RADIUS / 4, 0)
   pg.draw.circle(screen, pCTwo, (drops["changeX"][i] + 5, drops["changeY"][i] - 2), DROP_RADIUS / 4, 0)
   pg.draw.circle(screen, pCOne, (drops["changeX"][i], drops["changeY"][i] - 20), DROP_RADIUS / 4, 0)

The pCOne and pCTwo basically take in the poppedColorOne and poppedColorTwo lists:
poppedColorOne = [(43, 217, 255), (255, 215, 0)]
poppedColorTwo = [(56, 114, 255), (255, 215, 0)]

These lists hold two RGB values: one color being a shade of blue and the other being the highscore shade that get passed through the following function: 

droplets(poppedColorOne[change_color % 2], poppedColorTwo[change_color % 2], poppedFontColor[change_color % 2])

Now, when the highscore event is triggered, and if the player has a present score higher than their prior high score, and the player isn't dead –– 
[if event.type == HIGHSCORE_EVENT and points > highscore and lives != 0]

We will increment the variable [change_color] by one, or if it's the first event that occurs where the user has broken the high score, we will set the [change_color] to 1. 

This enables our drops and the score font, on the left side, to change by one and stay at that change state until the event occurs again.

Back to our droplets(poppedColorOne[change_color % 2], poppedColorTwo[change_color % 2], poppedFontColor[change_color % 2]) function. Because the variable [change_color] will change by 1 every 100ms, and we want to oscillate between two colors, then using the module will help us distinguish between even and odd numbers –– which will produce the value of 0 or 1. Meaning, our popped drops, +1 number, and score text change from their original blue (0) and hold that state until their new golden color is summoned (2) and repeat until the user dies.

#### The Falling of the Drops [motion()] 🥲
The [motion()] function will essentially keep all drops, popped and unpopped, moving until they hit bottom. 

Now, [if drops["changeY"][i] >= 666 - DROP_RADIUS and not drops["is_popped"][i]] states that when the drops hit bottom (or the radius length of the bottom), then we will save this drop's id/list location for subsequent deletion and subtract the user's lives by one.

If the dropped hits the bottom and IS already popped [elif drops["changeY"][i] >= 666 - DROP_RADIUS and drops["is_popped"][i]], then we will simply just store this drop's location for future deletion.

If the drops are actually not popped nor hit the bottom just yet [elif drops["changeY"][i] < 666 - DROP_RADIUS and not drops["is_popped"][i]], we'll just simply change their y-position by the amount specified in [DROP_SPEED].

The only situation remaining is when the dropped is popped and hasn't hit bottom. In this scenario, we only apply the much faster [POPPED_SPEED]. 

#### Deleting the Drops When they Hit the Bottom [delete()]
Here we will check our list of all the drop's ids/list locations saved by [motion()] for deletion. 

This is pretty simple; we just loop through the drops dict, using the value stored at [do_delete[i]] as the list located in the drops dict. We also subtract the [number_drops] on the screen by 1 and clear the entire do_delete list to store new values.

### CLOUDY WITH A CHANCE OF MEATBALLS! [cloudMove()]
Here we just do a simple left or right move depending on the present location of all the clouds.


## Other Notable Designs
The last design I think is worth noting would be the hitbox.

The horrid looking variables [hit_box_x_start] and [hit_box_y_start] basically are meant to collectively select the top left corner of each drop, assuming the drop is a box and presuming the position of the drop stated in the center. 

From here, we create a nested for loop to sort through the rows and height of the drops:
for y in range(DROP_RADIUS * 2):
   for x in range(DROP_RADIUS * 2):

Here we will check the position of the mouse "unclick" stored in [pos] to the far left x-axis of the drop [hit_box_x_start] plus the position [x] where our loop is presently at in addition to the y axis of the drop [hit_box_y_start] plus the present position of the array [y].

And we will loop from this combined top left corner to the bottom right corner until the mouse's "unclick" position is equal to the present position in the nested for loop. Of course, if this condition turns out to be true, we will increment points by one and mark the drop as popped. And if it's a high score, we'll play a cool sound; if it's not a high score, we will play the default drop sound. 

And that is all! I hope you have/had fun playing it :)
