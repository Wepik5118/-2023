from pygame import *
from random import randint
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 80)
win = font2.render('ХАРОШ!', True, (255, 255, 255))
lose = font2.render('ТИ ЛОХ!', True, (180, 0, 0))

img_back = "mos.jpg"
img_hero = "zelenskiy.png"
img_enemy = "pngegg (1).png"
img_bullet = "pngwing.com.png"

lost = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(
            image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
            
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 20, 40, -15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 8)
            self.rect.y = 0
            lost = lost +1
win_width = 700
win_height = 500
display.set_caption("Шутер")
window = display.set_mode((700, 500))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height-100, 80,100,25)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width-80), -40,50,50, randint(1,5))
    monsters.add(monster)

finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    if not finish:
        window.blit(background, (0, 0))
        text_score = font1.render('Рахунок: '+str(score), 1, (255,255,255))
        window.blit(text_score, (0, 0))
        text_lose = font1.render('Пропущено: '+str(lost), 1, (255,255,255))
        window.blit(text_lose, (0, 30))
        ship.update()
        ship.reset()
        monsters.update()
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= 3:
            finish = True
            window.blit(lose, (200, 200))
        if score >= 50:
            finish = True
            window.blit(win, (200,200))
        display.update()
    time.delay(50)