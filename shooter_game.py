from pygame import *
from random import randint 
time.delay(5000)
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


#шрифты и надписи
font.init()
font2 = font.Font(None, 36)


#нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_hero = "ship.png" # герой
img_enemy = "ufo.png" # враг


score = 0 #сбито кораблей
lost = 0 #пропущено кораблей


#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)


        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed


        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#класс главного игрока
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.centery, 5, 5, 20)
        bullets.add(bullet)

bullets = sprite.Group()
hp = 2
class Boss(GameSprite):

   #движение врага
   def update(self):
        if self.rect.x > 100:
            self.rect.x += self.speed
        elif self.rect.x < 100 and self.rect.x > 500:
            self.rect.x += self.speed
            self.derection = 'right'

            if self.derection == 'left':
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
        global hp
        if hp <= 0:
            self.kill()
            # enemy_boss = Boss('rocket.png',99,100,100,100,15)



#класс спрайта-врага  
class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

make = False
#Создаём окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

score2 = 0
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
made = False
a = 4
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
   #событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
            elif e.key == K_q:
                a = 5
            elif e.key == K_e:
                a = 4
                
font = font.SysFont('Arial',40)

if not finish and a == 4:
            #обновляем фон
            
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        sprite_list = sprite.groupcollide(monsters,bullets,True, False)
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        for i in sprite_list:
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

            
            score = score + 1
            score2 = score2 + 1
            if score2 >= 2:
                enemy_boss = Boss('rocket.png',99,100,100,100,15)
                make = False
                made = 1

       
    
        
        
        bullets.update()
        
        monsters.update()       
        
        if made == 1:
            enemy_boss.update()
            enemy_boss.reset()
            
    window.blit(background,(0,0))
    bullets.draw(window)
    monsters.draw(window)
    bullets.update()
    ship.reset()
    ship.update()
    display.update()

    #цикл срабатывает каждую 0.05 секунд
    time.delay(50)


