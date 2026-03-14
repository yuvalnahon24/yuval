from pygame import *
import random


init()
# יצירת החלון באיזה גודל שנרצה
Window = display.set_mode((800, 600))
# בחירת שם החלון
display.set_caption("space")
# צריך לייבא את התמונה לתוכנית
galaxy = image.load("bg.jpg")


# צריך לייבא את התמונה של החללית לתוכנית
spaceship = image.load("ship.jpg")
# הקטנה של החללית
small_spaceship = transform.scale(spaceship , (180,180))
small_spaceship .set_colorkey((255, 255, 255))
box_spaceship = Rect(300 , 400 , small_spaceship.get_width(), small_spaceship.get_height())



fireball = image.load("fireball.jpg")
small_fireball = transform.scale(fireball, (25 , 25))
small_fireball.set_colorkey((255, 255, 255))
box_fireball = Rect(378 , 410 , small_fireball.get_width(), small_fireball.get_height())


alien = image.load("enemy1.jpg")
alien.set_colorkey((0,0,0))
alienS = transform.scale(alien, (100, 80))
aliens_images = []
alienX_changh = []
aliens_Rect = []
aliens_down = 30
num_of_aliens = 6


for i in range(num_of_aliens):
    aliens_images.append(alienS )
    one_rect = Rect(random.randint(0,800) , random.randint(0,200), alien.get_width() ,alien.get_height())
    aliens_Rect.append(one_rect)
    alienX_changh.append(24)

    

score_value = 0
font_score = font.SysFont("Ariel", 30)

# מצב מוכן ואפשר לשגר עוד כדור
fireball_state = "ready"



clock = time.Clock()


run = True
while run:
    # לשים את התמונה על המסך
    Window.blit(galaxy , (0 , 0))
    Window.blit(small_spaceship , box_spaceship)


    for e in event.get():
        if e.type == QUIT:
            run = False


        if e.type == KEYDOWN:
            if e.key == K_a:
                box_spaceship.x = box_spaceship.x - 40
            if e.key == K_d:
                box_spaceship.x = box_spaceship.x + 40
            if e.key == K_SPACE:
                if fireball_state == "ready":
                         box_fireball.x = box_spaceship.x
                         fireball_state = "fire"


        if fireball_state == "fire":
            Window.blit(small_fireball , box_fireball  ) 
            box_fireball.y = box_fireball.y - 20


        if box_fireball.y > 0:
            box_fireball.y = box_spaceship.y
            fireball_state = "ready"


        if box_spaceship.x < 0:
            box_spaceship.x = 0


        if box_spaceship.x >= 600:
            box_spaceship.x = 600


    for i in range(num_of_aliens):
        Window.blit(aliens_images[i] , aliens_Rect[i])
        
        aliens_Rect[i].x = aliens_Rect[i].x + alienX_changh[i]
        if aliens_Rect[i].x > 740:
            alienX_changh[i] = - 24
            aliens_Rect[i].y += aliens_down


        if aliens_Rect[i].x < 0:
            alienX_changh[i] =  24
            aliens_Rect[i].y += aliens_down
        if box_fireball.colliderect(aliens_Rect[i]) and fireball_state == "fire":
            aliens_Rect[i].y = random.randint(0, 200)
            score = score + 1
    score = font_score.render("score" + str(score), True, "white")
    Window.blit(score_value, 10 , 10)
    clock.tick(20)
    display.update()






quit()