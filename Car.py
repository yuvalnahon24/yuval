from pygame import *
from random import *
import time
init()

Window = display.set_mode((1000, 1200))
display.set_caption("Car")

# Load images
crossroad_bg = image.load("road.png")
Car = image.load("Car.png")
Tree = image.load("tree.png")
Shield = image.load("shiled.png")
coin = image.load("coin.png")
rock = image.load("rock.png")

# Resize images
small_Car = transform.scale(Car, (180, 180))
small_Shield = transform.scale(Shield, (180, 180))
small_Tree = transform.scale(Tree, (180, 180))
small_coin = transform.scale(coin, (180, 180))
small_rock = transform.scale(rock, (180, 180))

# Rects
box_Car = Rect(500, 1000, small_Car.get_width(), small_Car.get_height())
box_Coin = Rect(randint(0, 820), randint(0, 250), small_coin.get_width(), small_coin.get_height())
box_Tree = Rect(randint(0, 820), randint(0, 250), small_Tree.get_width(), small_Tree.get_height())
box_rock = Rect(randint(0, 820), randint(0, 250), small_rock.get_width(), small_rock.get_height())
box_Shield = Rect(randint(0, 820), randint(-100, -50), small_Shield.get_width(), small_Shield.get_height())

# Speeds
coin_speed = 1
Tree_speed = 2
rock_speed = 1
shield_speed = 1

# Score
score_value = 0

# Fonts
font_score = font.SysFont("Ariel", 100)
font_win = font.SysFont("Ariel", 200)
font_small = font.SysFont("Ariel", 60)

# Shield state
shield_active = False
shield_cooldown_time = 0  # when shield can spawn again
invincible = False
invincible_start_time = 0
invincible_duration = 10  # seconds

run = True
while run:
    current_time = time.time()

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_a:
                box_Car.x -= 60
            if e.key == K_d:
                box_Car.x += 60
            if e.key == K_w:
                box_Car.y -= 40
            if e.key == K_s:
                box_Car.y += 40

    # Move objects
    box_Coin.y += coin_speed
    box_rock.y += rock_speed
    box_Tree.y += Tree_speed

    # Respawn Coin
    if box_Coin.y > 1200:
        box_Coin.y = randint(-100, -50)
        box_Coin.x = randint(0, 820)
    if box_Car.colliderect(box_Coin):
        box_Coin.y = randint(0, 250)
        box_Coin.x = randint(0, 820)
        score_value += 1

    # Respawn Rock
    if box_rock.y > 1200:
        box_rock.y = randint(-100, -50)
        box_rock.x = randint(0, 820)
    if box_Car.colliderect(box_rock):
        box_rock.y = randint(0, 250)
        box_rock.x = randint(0, 820)
        if not invincible:
            score_value -= 1

    # Respawn Tree
    if box_Tree.y > 1200:
        box_Tree.y = randint(-100, -50)
        box_Tree.x = randint(0, 820)
    if box_Car.colliderect(box_Tree):
        box_Tree.y = randint(0, 250)
        box_Tree.x = randint(0, 820)
        if not invincible:
            score_value -= 2

    # End invincibility after 10 seconds
    if invincible and current_time - invincible_start_time > invincible_duration:
        invincible = False

    # Spawn Shield if not active and cooldown is over
    if not shield_active and current_time - shield_cooldown_time > 20 and random() < 0.01:
        shield_active = True
        box_Shield.y = randint(-100, -50)
        box_Shield.x = randint(0, 820)

    # Move and check shield
    if shield_active:
        box_Shield.y += shield_speed

        if box_Shield.y > 1200:
            shield_active = False

        if box_Car.colliderect(box_Shield):
            shield_active = False
            invincible = True
            invincible_start_time = current_time
            shield_cooldown_time = current_time  # start 20 sec cooldown

    # Draw background
    Window.blit(crossroad_bg, (0, 0))

    # Draw everything
    Window.blit(small_Car, box_Car)
    Window.blit(small_coin, box_Coin)
    Window.blit(small_rock, box_rock)
    Window.blit(small_Tree, box_Tree)

    if shield_active:
        Window.blit(small_Shield, box_Shield)

    # Show countdown if invincible
    if invincible:
        time_left = int(invincible_duration - (current_time - invincible_start_time))
        shield_timer_text = font_small.render(f"Shield: {time_left}", True, (0, 200, 0))
        Window.blit(shield_timer_text, (750, 50))  # Top-right corner

    # Score
    score = font_score.render("Score:" + str(score_value), True, "Black")
    Window.blit(score, (100, 50))

    # Win/Lose conditions
    if score_value >= 16:
        Window.blit(font_win.render("You Won!", True, "Black"), (250, 500))
        display.update()
        time.sleep(2)
        run = False

    elif score_value <= -2:
        Window.blit(font_win.render("You Lost!", True, "Black"), (250, 500))
        display.update()
        time.sleep(2)
        run = False

    display.update()

quit()
