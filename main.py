import pygame, os, time, random

#initialising
pygame.init()
pygame.font.init()

#window
width = height = 750
win = pygame.display.set_mode((width,height))
pygame.display.set_caption('Space Invaders')

# assets
# ships
red_spaceship = pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png'))
green_spaceship = pygame.image.load(os.path.join('assets', 'pixel_ship_green_small.png'))
blue_spaceship = pygame.image.load(os.path.join('assets', 'pixel_ship_blue_small.png'))
yellow_spaceship = pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png'))#player

#lasers
red_laser = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
green_laser = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
blue_laser = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
yellow_laser = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))

#Background
bg = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (width, height))

#functions

class Ship:
    COOLDOWN = 10
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_laser(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        if self.cool_down_counter > 0:
            self.cool_down_counter += 1


    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x,self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x,y,health)
        self.ship_img = yellow_spaceship
        self.laser_img = yellow_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_laser(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height()+10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width()*(self.health/self.max_health), 10))

class Enemy(Ship):
    color_map = {'red':(red_spaceship, red_laser), 'green':(green_spaceship, green_laser), 'blue':(blue_spaceship,blue_laser)}

    def __init__(self, x, y, color, health=100):
        super().__init__(x,y,health)
        self.ship_img, self.laser_img = self.color_map[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-15,self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Laser():
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

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    fps = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 60)
    player = Player(300,630)
    player_vel = 5
    laser_vel = 5
    enemy_vel = 1
    lost = False
    lost_count = 0
    s_speed = 2

    enemies = []
    wave_length = 5

    clock = pygame.time.Clock()

    def redraw_window():
        win.blit(bg,(0,0))
        #draw text
        lives_label = main_font.render('Lives : {}'.format(lives,), True, (255,255,255))
        level_label = main_font.render('Level : {}'.format(level,), True, (255,255,255))
        win.blit(lives_label, (10,10))
        win.blit(level_label, (width-level_label.get_width()-10, 10))

        for enemy in enemies:
            enemy.draw(win)

        player.draw(win)

        if lost:
            lost_label = lost_font.render('You lost!!', True, (255,255,255))
            win.blit(lost_label, (width//2 - lost_label.get_width()/2, height//2))

        pygame.display.update()

    while run:
        clock.tick(fps)
        f = open('fps.txt', 'a')
        f.write(str(int(clock.get_fps()))+'\n')
        f.close()
        redraw_window()

        if lives <= 0 or player.health == 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 3:
                run=False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            player.health = player.max_health
            wave_length = level ** 2
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, width-100), random.randrange(-1500, -100), random.choice(['red','green','blue']))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < width:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < height:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_laser(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)

        player.move_laser(-laser_vel, enemies)

def main_menu():
    run = True
    title_font = pygame.font.SysFont('comicsans', 70)
    title_label = title_font.render('Press any key to begin', True, (255,255,255))
    while run:
        win.blit(bg, (0,0))
        win.blit(title_label, ((width / 2) - (title_label.get_width() / 2), 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                main()

    pygame.quit()

main_menu()
f = open('fps.txt')
#r = f.read().split('\n')
f.seek(0)
r = f.readlines()
f.close()
for i in range(len(r)):
    if i != '0':
        r[i] = int(r[i])
print('Average FPS:',sum(r)//len(r))
time = {'hours':0,'minutes':0,'seconds':0}
time['seconds'] = len(r)//60
if time['seconds'] >= 60:  
    time['seconds'] = len(r)%60
    time['minutes'] = (len(r)//3600)

if time['minutes'] >= 60:
    time['minutes'] = (len(r)%3600)//60
    time['hours'] = len(r)//(60**3)

print('Time played:')
print(time)
