import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Invaders")
#Load ships
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))
#Main player
YELLOW_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets","pixel_ship_yellow.png")),(60,60))
#Load lasers
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))
#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def move(self, vel):
        self.y += vel
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    def collision(self, obj):
        return collide(obj, self)
class Ship:
    COOLDOWN = 30
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.laser_image = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


        

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1


    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_height()

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_image)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__( x, y, health)
        self.ship_image = YELLOW_SPACE_SHIP
        self.laser_image = YELLOW_LASER
        self.max_health = health
        self.mask = pygame.mask.from_surface(self.ship_image)
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                         self.lasers.remove(laser)
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_image)
            self.lasers.append(laser)
            self.cool_down_counter = 1

                         

class Enemy(Ship):
    COLOUR_MAP = {
                  "red": (RED_SPACE_SHIP, RED_LASER),
                  "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
                  "green": (GREEN_SPACE_SHIP, GREEN_LASER)
    }
    def __init__(self, x, y, colour, health=20):
        super().__init__(x, y, health)
        self.ship_image, self.laser_image = self.COLOUR_MAP[colour]
        self.mask = pygame.mask.from_surface(self.ship_image)

    def move(self, vel):
        self.y += vel 
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-10, self.y, self.laser_image)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj2.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None








def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    level = 0
    lives = 5
    main_font=pygame.font.SysFont("comicsans",25)
    lost_font=pygame.font.SysFont("comicsans",45)
    player = Player(275, 450)
    player_vel = 7
    enemy_vel = 1
    laser_vel = 5
    enemies = []
    wave_length = 5
    lost = False
    lost_count = 0


    def redraw_window():
        WIN.blit(BG,(0,0))
        level_label = main_font.render(f"Level: {level}",1,(255,0,255))
        lives_label = main_font.render(f"Lives: {lives}",1,(255,0,255))
        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10,10))
        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)
        if lost:
            lost_label = main_font.render("Game Over",1,(255,0,0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2,HEIGHT/2))

        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window() 
        if lives <= 0 or player.health <= 0:
             lost = True
             lost_count += 1
        
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
             level += 1
             wave_length += 5

             for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0 :
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_width() < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 120) == 1:
                enemy.shoot()
            if collide(enemy, player):   
                player.health -= 10
                enemies.remove(enemy)
                ;
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

            


        player.move_lasers(-laser_vel, enemies)

        
main()

