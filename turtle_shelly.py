import turtle
import random
import math
import time
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load sounds
bounce_sound = pygame.mixer.Sound('c:/Users/ASUS/SheCodes/python/space_turtle_chomp/bounce.mp3')
chomp_sound = pygame.mixer.Sound('c:/Users/ASUS/SheCodes/python/space_turtle_chomp/chomp.mp3')

# Set up screen
turtle.setup(650, 650)
wn = turtle.Screen()
wn.bgcolor('white')
wn.bgpic('c:/Users/ASUS/SheCodes/python/space_turtle_chomp/shelly2.gif')
wn.tracer(3)

# Draw border
mypen = turtle.Turtle()
mypen.penup()
mypen.setposition(-300, -300)
mypen.pendown()
mypen.pensize(3)
mypen.color('black')
mypen.speed(0)
for side in range(4):
    mypen.forward(600)
    mypen.left(90)
mypen.hideturtle()

# Create player turtle
player = turtle.Turtle()
player.color('lightgreen')
player.shape('turtle')
player.penup()
player.speed(0)

# Create opponent turtle
comp = turtle.Turtle()
comp.color('red')
comp.shape('turtle')
comp.penup()
comp.setposition(random.randint(-290, 290), random.randint(-290, 290))

# Create competition score
mypen2 = turtle.Turtle()
mypen2.color('red')
mypen2.hideturtle()

# Create variable score
score = 0
comp_score = 0

# Create food
maxFoods = 10
foods = []

for count in range(maxFoods):
    new_food = turtle.Turtle()
    new_food.shapesize(.5)
    new_food.color("white")
    new_food.shape("circle")
    new_food.penup()
    new_food.speed(0)
    new_food.setposition(random.randint(-290, 290), random.randint(-290, 290))
    foods.append(new_food)

# Set speed variable
speed = 1
# Set game time limit
timeout = time.time() + 10 * 6

# Define functions
def turn_left():
    player.left(90)

def turn_right():
    player.right(90)

def increase_speed():
    global speed
    speed += 1

def decrease_speed():
    global speed
    if speed > 1:
        speed -= 1

def isCollision(t1, t2):
    d = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    return d < 20

# Set keyboard binding
wn.listen()
wn.onkey(turn_left, 'Left')
wn.onkey(turn_right, 'Right')
wn.onkey(increase_speed, 'Up')
wn.onkey(decrease_speed, 'Down')

# Update function to avoid tkinter issues
def game_update():
    global score, comp_score

    # Check for game over
    if time.time() > timeout:
        mypen.setposition(0, 0)
        mypen.color("yellow")
        if score > comp_score:
            mypen.write("Game Over: You WIN", align="center", font=("Arial", 28, "normal"))
        else:
            mypen.write("Game Over: You LOSE", align="center", font=("Arial", 28, "normal"))
        return  # End the game

    player.forward(speed)
    comp.forward(3)

    # Boundary Player Checking x coordinate
    if player.xcor() > 290 or player.xcor() < -290:
        player.right(180)
        bounce_sound.play()

    # Boundary Player Checking y coordinate
    if player.ycor() > 290 or player.ycor() < -290:
        player.right(180)
        bounce_sound.play()

    # Boundary Comp Checking x coordinate
    if comp.xcor() > 290 or comp.xcor() < -290:
        comp.right(random.randint(10, 170))
        bounce_sound.play()

    # Boundary Comp Checking y coordinate
    if comp.ycor() > 290 or comp.ycor() < -290:
        comp.right(random.randint(10, 170))
        bounce_sound.play()

    # Move food around and check for collisions
    for food in foods:
        food.forward(3)
        if food.xcor() > 290 or food.xcor() < -290:
            food.right(180)
            bounce_sound.play()
        if food.ycor() > 290 or food.ycor() < -290:
            food.right(180)
            bounce_sound.play()

        # Player Collision with food
        if isCollision(player, food):
            food.setposition(random.randint(-290, 290), random.randint(-290, 290))
            chomp_sound.play()
            score += 1
            # Clear and redraw the score instead of using undo
            mypen.clear()
            mypen.penup()
            mypen.hideturtle()
            mypen.setposition(-290, 310)
            mypen.write(f"Score: {score}", align="left", font=("Arial", 14, "normal"))

        # Comp Collision with food
        if isCollision(comp, food):
            food.setposition(random.randint(-290, 290), random.randint(-290, 290))
            chomp_sound.play()
            comp_score += 1
            # Clear and redraw the opponent's score
            mypen2.clear()
            mypen2.penup()
            mypen2.hideturtle()
            mypen2.setposition(200, 305)
            mypen2.write(f"Score: {comp_score}", align="left", font=("Arial", 14, "normal"))

    # Schedule the next update
    wn.ontimer(game_update, 50)

# Start game loop
game_update()
turtle.done()
