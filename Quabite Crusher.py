# Quabite Crusher
# Created by Jordan Hedgecock using Pygame a gaming library.
# Sprites made with Piskel.

import pygame
import random
import sys
from os import path

img_dir = path.join(path.dirname('__file__'), 'img')
snd_dir = path.join(path.dirname('__file__'), 'snd')

#Set screen and frames (Portrait)
WIDTH = 480
HEIGHT = 600
FPS = 60
HS_FILE = "highscore.txt"

# set up score / other variables
score = 0
EventCheck = 0
reward = 0
eye_of_the_storm = 0
confirm = 0
level = 0
lvl_frames = 0
lvl_chng = 0
mob_cap = 0
mob_spawn = True
cheat = False

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# randomize caption jokes
joke = random.randrange(1,6)
if joke is 1:
    joke = "In Case of Emergency Use Towel"
elif joke is 2:
    joke = "Now in 1D!"
elif joke is 3:
    joke = "Fire, Aquadron! Fire!"
elif joke is 4:
    joke = "Press alt-f4"
else:
    joke = "Coming Soon to a Computer Near You!"
pygame.display.set_caption("Quabite Crusher: " + str(joke))
clock = pygame.time.Clock()

font_name = pygame.font.match_font('Press Start 2P')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def newmob2():
    mm = Mob2()
    all_sprites.add(mm)
    mobs2.add(mm)

def newmob3():
    mmm = Mob3()
    all_sprites.add(mmm)
    mobs3.add(mmm)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = pct
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_boss_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BOSS_BAR_LENGTH = 100
    BOSS_BAR_HEIGHT = 10
    fill = pct
    outline_rect = pygame.Rect(x, y, BOSS_BAR_LENGTH, BOSS_BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BOSS_BAR_HEIGHT)
    pygame.draw.rect(surf, PURPLE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# Load all game graphics
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "Blue Electric.gif")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
power1_img = pygame.image.load(path.join(img_dir, "Health powerup.png")).convert()
quabite1_img = pygame.image.load(path.join(img_dir, "Tamed Quabite.png")).convert()
quabite2_img = pygame.image.load(path.join(img_dir, "Emoji Quabite.png")).convert()
quabite3_img = pygame.image.load(path.join(img_dir, "Deadly_Quabite.png")).convert()
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
explosion_anim['boss'] = []
for i in range(9):
    filename = 'Explosion0{}.gif'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(YELLOW)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    explosion_anim['player'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    img_bs = pygame.transform.scale(img, (120, 120))
    explosion_anim['boss'].append(img_bs)
boss_anim = {}
boss_anim['Mother'] = []
for i in range(30):
    filename = 'Mother0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_mother = pygame.transform.scale(img, (120, 120))
    boss_anim['Mother'].append(img_mother)

#Load all game sounds
laser_snd = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
pow_snd = pygame.mixer.Sound(path.join(snd_dir, 'powerup.wav'))
death_snd = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'music_jewels.ogg'))
pygame.mixer.music.set_volume(1)

#Spaceship Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.rect = self.image.get_rect()
        self.radius = 16
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        if cheat:
            self.shot_delay = 0
        else:
            self.shot_delay = 500
        self.last_shot = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            # CHEAT
            if cheat:
                bullet = Bullet(self.rect.left, self.rect.bottom)
                all_sprites.add(bullet)
                bullets.add(bullet)
                bullet = Bullet(self.rect.right, self.rect.bottom)
                all_sprites.add(bullet)
                bullets.add(bullet)
            laser_snd.play()

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -6
        if keystate[pygame.K_d]:
            self.speedx = 6
        if keystate[pygame.K_w]:
            self.speedy = -6
        if keystate[pygame.K_s]:
            self.speedy = 6
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top <0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.shield > 100:
            self.shield = 100

#Quabite Sprite
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = quabite2_img
        self.image = self.image_orig.copy()
        self.image_orig.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85  / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        if self.rot_speed is 0:
            self.rot_speed += 1
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.kill()
            newmob()

#Quabite (easy) Sprite
class Mob2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = quabite1_img
        self.image = self.image_orig.copy()
        self.image_orig.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85  / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        if self.rot_speed is 0:
            self.rot_speed += 1
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.kill()
            newmob2()

#Quabite (hard) Sprite
class Mob3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = quabite3_img
        self.image = self.image_orig.copy()
        self.image_orig.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85  / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        if self.rot_speed is 0:
            self.rot_speed += 1
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.kill()
            newmob3()

# Laser sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image = pygame.transform.scale(bullet_img, (10,20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# Explosion animation
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
# powerups
class Powerup_HP(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = power1_img
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(power1_img, (30, 30))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .45  / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = 4
        self.speedx = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            powerup.kill()

#Mother Quabite
class Mother(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.frame = 0
        self.image = boss_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.egg_sac = 100
        self.health = 100
        self.speedx = 5
        self.radius = int(self.rect.width * .85  / 2)
        self.shot_delay = random.randrange(500, 700)
        self.last_shot = pygame.time.get_ticks()
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.phasecheck = 0
        self.fire = True
        self.radius = int(self.rect.width * .45  / 2)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > random.randrange(500, 600):
            self.last_shot = now
            anti = Anti_Bullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(anti)
            anti_bullets.add(anti)

    def update(self):
        now = pygame.time.get_ticks()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH and self.phasecheck is not 1:
            self.rect.right = WIDTH
            self.speedx = -5
        if self.rect.left < 0 and self.phasecheck is not 1:
            self.rect.left = 0
            self.speedx = 5
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame is 3 and self.phasecheck is 0:
                self.frame = 0
            else:
                x = self.rect.centerx
                y = self.rect.top
                self.image = boss_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.centerx = x
                self.rect.top = y
        if self.egg_sac < 1 and self.phasecheck is 0:
                self.phasecheck = 1
                self.frame_rate = 130
                self.speedx = 0
                self.frame = 4
                x = self.rect.centerx
                y = self.rect.top
                self.image = boss_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.centerx = x
                self.rect.top = y
                self.fire = False
                for i in range(15):
                    newmob3()
        if self.frame is 29 and self.phasecheck is 1:
            self.speedx = 5
            self.frame_rate = 50
        if self.frame is 29:
            self.phasecheck = 2
            self.frame = 27
            x = self.rect.centerx
            y = self.rect.top
            self.image = boss_anim[self.size][self.frame]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.top = y
            self.fire = True
        if self.fire is True:
            self.shoot()

#Anti-Bullet
class Anti_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image = pygame.transform.scale(bullet_img, (10,20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

def show_go_screen():
    screen.blit(background, background_rect)
    # load highscore
    dirs = path.dirname('__file__')
    with open(path.join(dirs, HS_FILE), 'r') as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0
    draw_text(screen, "Quabite Crusher!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "SPACE to fire, W,A,S,D to move",22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press Enter/Return to begin", 18, WIDTH /2, HEIGHT * 3 / 4)
    draw_text(screen, "High Score: " + str(highscore), 22, WIDTH / 2, 14)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RETURN]:
            waiting = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def show_over_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "GAME OVER", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Score: " + str(score),22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press Enter/Return to play again", 18, WIDTH /2, HEIGHT * 3 / 4)
    # load highscore
    dirs = path.dirname('__file__')
    with open(path.join(dirs, HS_FILE), 'r') as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0
    if score > highscore:
        highscore = score
        draw_text(screen, "NEW HIGH SCORE!", 22, WIDTH / 2, HEIGHT / 2 + 40)
        with open(path.join(dirs, HS_FILE), 'w') as f:
            f.write(str(score))
    else:
        draw_text(screen, "High Score: " + str(highscore), 22, WIDTH / 2, 14)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RETURN]:
            waiting = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Define sprite Groups
bullets = pygame.sprite.Group()
anti_bullets = pygame.sprite.Group()
bosses = pygame.sprite.Group()
mobs = pygame.sprite.Group()
mobs2 = pygame.sprite.Group()
mobs3 = pygame.sprite.Group()
powerups = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
powerup = Powerup_HP()

pygame.mixer.music.play(-1)
# Game loop
start = True
running = True
game_over = False
lvl_up = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # check to see if player collects powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        pow_snd.play()
        if player.shield is 100:
            score += 100
        else:
            player.shield += 25

    # check to see if bullet hits mother
    hits = pygame.sprite.groupcollide(bosses, bullets, False, True, pygame.sprite.collide_circle)
    for hit in hits:
        if confirm is 0:
            mother.kill()
            score = 0
        elif mother.health < 1:
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'boss')
            all_sprites.add(expl)
            mother.kill()
            score += 1000
            reward += 1000
            eye_of_the_storm = 0
            confirm = 0
            mob_spawn = True
            EventCheck = 0

            for i in range(3):
                mob_cap += 1
                newmob()

            for i in range(3):
                mob_cap += 1
                newmob2()

            for i in range(2):
                mob_cap += 1
                newmob3()

        else:
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if mother.phasecheck is 0:
                mother.egg_sac -= 10
                score += 50
                reward += 50
            else:
                mother.health -= 6.5
                score += 50
                reward += 50

    hits = pygame.sprite.spritecollide(player, anti_bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 15
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.kill()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 15
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        mob_cap += 1
        if mob_cap != 20:
            if mob_spawn == True:
                newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            death_snd.play()
            player.kill()

    hits = pygame.sprite.spritecollide(player, mobs2, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 10
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        mob_cap += 1
        if mob_cap != 20:
            if mob_spawn == True:
                newmob2()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            death_snd.play()
            player.kill()

    hits = pygame.sprite.spritecollide(player, mobs3, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= (20 + level)
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        mob_cap += 1
        if mob_cap != 20:
            if mob_spawn == True:
                newmob3()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            death_snd.play()
            player.kill()

    # Delay time after players death for game to close to properly show animations
    if not player.alive() and not death_explosion.alive():
        game_over = True

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 200
        reward += 200
        eye_of_the_storm += 200
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        mob_cap += 1
        if mob_cap != 20:
            if mob_spawn == True:
                newmob()

    hits = pygame.sprite.groupcollide(mobs2, bullets, True, True)
    for hit in hits:
        score += (100 + level)
        reward += (100 + level)
        eye_of_the_storm += 100
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        mob_cap += 1
        if mob_cap != 20:
            if mob_spawn == True:
                newmob2()

    hits = pygame.sprite.groupcollide(mobs3, bullets, True, True)
    for hit in hits:
        score += 300
        reward += 300
        eye_of_the_storm += 300
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        mob_cap += 1
        if mob_cap != 20:
            if mob_spawn == True:
                newmob3()

    # Make levels change
    if level - lvl_chng is 2:
        lvl_chng = level
        suprise = random.randrange(1,4)
        mob_cap += 1
        if suprise is 1:
            newmob2()
        elif suprise is 2:
            newmob()
        else:
            newmob3()

    # activate Quabite storm
    if score >= 50000 and EventCheck is 0:
        score += 1500
        reward += 1500
        eye_of_the_storm += 1500
        EventCheck = 1
        for i in range(1):
            mob_cap += 1
            newmob2()
        for i in range(1):
            mob_cap += 1
            newmob()
        for i in range(2):
            mob_cap += 1
            newmob3()

    # ACTIVATE BOSS EVENT
    if eye_of_the_storm >= 100000 and EventCheck is 1:
        EventCheck = 2
        m = Mob()
        mm = Mob2()
        score += 500
        reward += 500
        eye_of_the_storm = 0
        mother = Mother(WIDTH / 2, 10, 'Mother')
        all_sprites.add(mother)
        bosses.add(mother)
        confirm = 1
        mob_spawn = False

    # Reward player
    if reward >= 5000:
        reward -= 5000
        lvl_up = True
        level += 1
        lvl_frames = 0
        powerup = Powerup_HP()
        all_sprites.add(powerup)
        powerups.add(powerup)

    if start:
        show_go_screen()
        start = False
        all_sprites = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        powerup = Powerup_HP()
        bullets = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        mobs2 = pygame.sprite.Group()
        mobs3 = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        # AUTO BOSS FIGHT! DEBUG ONLY DO NOT EDIT!
        # mother = Mother(WIDTH / 2, 10, 'Mother')
        # all_sprites.add(mother)
        # bosses.add(mother)
        # confirm = 1

        mob_cap = 0

        for i in range(4):
            mob_cap += 1
            newmob()

        for i in range(3):
            mob_cap += 1
            newmob2()

        for i in range(2):
            mob_cap += 1
            newmob3()

        score = 0
        EventCheck = 0
        reward = 0
        eye_of_the_storm = 0
        lvl_chng = 0
        level = 0
        lvl_frames = 0
        lvl_up = True
        mob_spawn = True

    if game_over:
        show_over_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        powerup = Powerup_HP()
        bullets = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        mobs2 = pygame.sprite.Group()
        mobs3 = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        mob_cap = 0

        for i in range(4):
            mob_cap += 1
            newmob()

        for i in range(3):
            mob_cap += 1
            newmob2()

        for i in range(2):
            mob_cap += 1
            newmob3()

        score = 0
        EventCheck = 0
        reward = 0
        eye_of_the_storm = 0
        confirm = 0
        level = 0
        lvl_frames = 0
        lvl_chng = 0
        lvl_up = True
        mob_spawn = True

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    if confirm is 1:
        draw_boss_bar(screen, WIDTH - 105, 5, (mother.health + mother.egg_sac) / 2)
    if lvl_up is True:
            draw_text(screen, "Level " + str(level), 64, WIDTH / 2, HEIGHT / 4)
            lvl_frames += 1
            if lvl_frames is 50:
                lvl_up = False
                lvl_frames = 0
    if level >= 1000:
        draw_text(screen, "You Win. Being one of the very few to see this is your reward", 20, WIDTH / 2, HEIGHT / 4)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
