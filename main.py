# PyGame LDLC
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

#On définit les variables concernant notre jeu
WIDTH = 400
HEIGHT = 600
FPS = 60

# On définit des couleurs à utiliser plus tard
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# ----------------------------------- Enemy -----------------------------------------


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2)
        #On choisit une position x aléatoire entre le côté gauche de l'écran et le côté droit - la largeur du vaisseau
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        #On choisit une position y aléatoire entre 100 pixels au dessus de l'écran et le haut de l'écran - la hauteur du vaisseau
        self.rect.y = random.randrange(-100, 0-self.rect.height)
        #On donne une vitesse aléatoire au vaisseau
        self.speedY = random.randrange(2,5)
        self.speedX = random.randrange(-3,3)

    def update(self):
        self.rect.y += self.speedY
        self.rect.x += self.speedX

        #Si le vaisseau atteint le bas de l'écran, on lui redonne une position et une vitesse aléatoire
        if self.rect.bottom > HEIGHT + 100 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(0,WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100, 0-self.rect.height)
            self.speedY = random.randrange(2,5)



# ----------------------------------- Player -----------------------------------------


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.shield = 100
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedX = 0
        self.speedY = 0
        self.shoot_delay = 350
        self.last_shot = pygame.time.get_ticks()


    def update(self):
        pygame.sprite.Sprite.update(self)
        keys_pressed = pygame.key.get_pressed()

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        if keys_pressed[pygame.K_SPACE]:
            self.shoot()

        self.speedX = 0

        if keys_pressed[pygame.K_LEFT]:
            self.speedX = -5
        if keys_pressed[pygame.K_RIGHT]:
            self.speedX = 5
        
        #On bouge le vaisseau en fonction de la vitesse
        self.rect.x += self.speedX

        #On empêche le vaisseau de sortir de l'écran
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
        #Pareil qu'au dessus, mais pour le déplacement vertical
        self.speedY = 0
        if keys_pressed[pygame.K_UP]:
            self.speedY = -5
        if keys_pressed[pygame.K_DOWN]:
            self.speedY = 5

        self.rect.y += self.speedY

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT



    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

    # Cache le vaisseau quand il est détruit
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


# ----------------------------------- Missiles -----------------------------------------


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # ça ne dépasse pas le bord
        if self.rect.bottom < 0:
            self.kill()


# ----------------------------------- Explosion -----------------------------------------


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


# On initialise pygame et on crée la fenêtre grâce aux variables WIDTH et HEIGHT


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame")
clock = pygame.time.Clock()

# Chemin vers le dossier assets


assets_dir = path.join(path.dirname(__file__), 'assets')
background = pygame.image.load(path.join(assets_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(assets_dir, 'player.png')).convert()
enemy_img = pygame.image.load(path.join(assets_dir, 'enemy.png')).convert()
bullet_img = pygame.image.load(path.join(assets_dir, 'missile_player.png')).convert()

# Chemin vers le dossier snd


shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))


# On crée un groupe pour les sprites


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
enemy = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# -----------------------------------Vies-----------------------------------------


player_img = pygame.image.load(path.join(assets_dir, "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

# -----------------------------------Son et musique-----------------------------------------


expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)


# -----------------------------------Animation explosion-----------------------------------------


explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "BOOM!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Les flèches pour bouger, et espace pour tirer", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Appuie sur une touche pour jouer", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def newmob():
    m = Enemy()
    all_sprites.add(m)
    enemy.add(m)


for i in range(8):
    newmob()


score = 0
pygame.mixer.music.play(loops=-1)

# Tant que le jeu tourne

game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0
    #On fixe le jeu à 60 FPS
    clock.tick(FPS)
    
    #Récupération des inputs

    for event in pygame.event.get():
        #Pour fermer la fenêtre, on arrête la boucle while
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #Tous les sprites sont updatés
    all_sprites.update()

    #Tous les sprites sont dessinés
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    
    #Une fois que tout est dessiné, on l'affiche à l'écran
    pygame.display.flip()

    # Tir de missile
    hits = pygame.sprite.groupcollide(enemy, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()

    # Collision
    hits = pygame.sprite.spritecollide(player, enemy, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    if player.lives == 0 and not death_explosion.alive():
        game_over = True

#Quand on sort de la boucle, on ferme le jeu
pygame.quit()
