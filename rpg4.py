import pygame, random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (50,140,0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

pygame.init()

#Nazwy plikow png -------------------------------------------------------------------------------------------------------
heart = pygame.image.load("heart.png")
flower = "flower.png"
tadeuszP = "tadko.png"
telimenaP = "telimena.png"
zosiaP = "zosia.png"
sedziaP = "sedzia.png"
hrabiaP = "hrabia.png"
mushroom = "mushroom.png"
zameksign = "zameksign.png"
barX = "barX.png"
barY = "barY.png"
lassign = "lassign.png"
dworeksign = "dworeksign.png"
dobrzynsign = "dobrzyn.png"
dworekP = "dworek.png"
#-----------------------------------------------------------------------------------------

#zmienne pomocnicze globalne-----------------------------------------------------------
points = { 'zosia': 0, 'hrabia': 0, 'mushroom': 0, 'dworek': 0}
myfont = pygame.font.SysFont("Georgia", 15)
score = 0
showme = ""
lives = 3
cr = 0 # wejscie do dworku / zamku
#zwierzeta----------------------------------------------------------------------
class Animal(pygame.sprite.Sprite):
    def __init__(self, name, x, y, pic):
        super().__init__()
        self.image = pygame.image.load(pic)
        self.name = name
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.addx = 0
        self.addy = 0
    def move(self, ram, ramy):
        clocky = pygame.time.get_ticks()
        if clocky % 5 == 0:
            self.addx = ram
            self.addy = ramy
            if self.rect.x > 700:
                self.addx = -6
            if self.rect.x < 100:
                self.addx = 6
            if self.rect.y < 100:
                self.addy = 6
            if self.rect.y > 500:
                self.addy = -6
        self.rect.y += self.addy
        self.rect.x += self.addx

mucha1 = Animal("mucha",20,50,"fly.png")
mucha2 = Animal("mucha",750,120,"fly.png")
mucha3 = Animal("mucha",590,580,"fly.png")
mucha4 = Animal("mucha",490,400,"fly.png")
bear = Animal("bear",300,300,"niedz.png")

#-------------------------------------------------------------------------------------------------------

# definicje postaci -------------------------------------------------------------------------------------------------------
class Character(pygame.sprite.Sprite):
    def __init__(self, name, x, y, pic, text):
        super().__init__()
        self.image = pygame.image.load(pic)
        self.name = name
        self.text = text

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

hrabia =Character("hrabia",60,300,hrabiaP,"jestem hrabia")
zosia = Character("zosia", 30, 200, zosiaP, "jestem Zosia")
sedzia = Character("sedzia", 30, 200, sedziaP, "jestem Sędzią")
wojski = Character("wojski", 230, 100, "wojski.png", "jestem wojski")
telimena = Character("telimena", 230, 200, telimenaP, "jestem Telimeną")

#----------------------------------------------------------------------------------------------------------------------------


class Wall(pygame.sprite.Sprite):

    def __init__(self, name, x, y, pic):
        super().__init__()
        self.image = pygame.image.load(pic )
        self.name = name
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Player(pygame.sprite.Sprite):

    change_x = 0
    change_y = 0

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(tadeuszP)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def move(self, walls, chars, anim):

        global showme
        global score
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if block.name == "mushroom":
                showme = "you chose wisely"
                if points['mushroom']==0:
                    points['mushroom']=1
                    score+=1
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
        #################################################################33
        char_hit_list = pygame.sprite.spritecollide(self, chars, False)
        for character in char_hit_list:
            showme = character.text
            if self.change_x > 0:
                self.rect.right = character.rect.left
            else:
                self.rect.left = character.rect.right
        animal_hit_list = pygame.sprite.spritecollide(self, anim, True)
        if animal_hit_list:
            global lives
            lives -=1

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            global cr
            if block.name == "dworek":
                if points['dworek']==0:
                    cr = 7
                    self.rect.bottom = 575
            elif block.name == "krawedzX":
                self.rect.top = 370
                if points['dworek']==0:
                    points['dworek']=1
                    score+=1
                    cr = 3
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
        #########################################################################
        char_hit_list = pygame.sprite.spritecollide(self, chars, False)
        for character in char_hit_list:
            showme = character.text
            if self.change_y > 0:
                self.rect.bottom = character.rect.top
            else:
                self.rect.top = character.rect.bottom

class Room(object):
    """ Base class for all rooms. """
    wall_list = None
    char_list = None
    animal_list = None
    room_background = None

    def __init__(self, background):
        self.wall_list = pygame.sprite.Group()
        self.char_list = pygame.sprite.Group()
        self.animal_list = pygame.sprite.Group()
        self.room_background = pygame.image.load(background)
class Room1(Room):
    """ wszystko co jest w 1. pokoju"""

    def __init__(self):
        super().__init__("grasscross.png")

        # lista obiektow w pokoju (nazwa wsporzedne x i y i obrazek do podstawienia) - DO ZMIANY
        walls = [["zameksign",50, 190, zameksign],
                 ["lassign", 600, 190, lassign],
                 ["dworeksign",410, 10, dworeksign],
                 ["dobrzynsign",410, 500, dobrzynsign]
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)
class Room2(Room):
    """wszystko w 2. pokoju"""

    def __init__(self):
        super().__init__("grassroadend2.png")

        # DO ZMIANY:
        walls = [["krawedz",0, 0, barX],
                 ["krawedz",0, 580, barX],
                 ["mushroom",680, 350, mushroom]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2],item[3])
            self.wall_list.add(wall)
        self.char_list.add(wojski)
class Room3(Room):
    """wszystko w 3. pokoju"""

    def __init__(self):
        super().__init__("grassroadend.png")

        walls = [["krawedz", 0, 0, barY],
                 ["krawedz", 0, 0, barX],
                 ["krawedz", 0, 580, barX]
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)
        ##############################################################3
        self.char_list.add(zosia)
        self.char_list.add(hrabia)
class Room4(Room):
    """wszystko w 3. pokoju"""

    def __init__(self):
        super().__init__("grassroadend4.png")

        walls = [["krawedz", 0, 0, barY],
                 ["krawedz", 0, 0, barX],
                 ["krawedz", 780, 0, barY],
                 ["dworek", 270, 170, dworekP]
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)
        ##############################################################3
        self.char_list.add(sedzia)
        self.char_list.add(hrabia)
class Room5(Room):
    """wszystko w 3. pokoju"""

    def __init__(self):
        super().__init__("grassroadend3.png")

        walls = [["krawedz", 0, 0, barY],
                 ["krawedz", 0, 580, barX],
                 ["krawedz", 780, 0, barY]
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)
        ##############################################################3
class Room6(Room):
    """wszystko w 2. pokoju"""

    def __init__(self):
        super().__init__("grass.png")

        # DO ZMIANY:
        walls = [["krawedz",0, 580, barX],
                 ["krawedz", 780, 0, barY],
                 ["mushroom",680, 350, mushroom]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2],item[3])
            self.wall_list.add(wall)
        self.char_list.add(telimena)
class Room7(Room):
    """wszystko w 3. pokoju"""

    def __init__(self):
        super().__init__("grass.png")

        walls = [["krawedz", 0, 0, barY],
                 ["krawedz", 0, 0, barX],
                 ["krawedz", 780, 0, barY]
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)
        ##############################################################3
            self.animal_list.add(bear)
class wdworku(Room):
    """wszystko w 3. pokoju"""

    def __init__(self):
        super().__init__("floor.png")

        walls = [["krawedz", 0, 0, barY],
                 ["krawedzX", 0, 0, barX],
                 ["krawedz", 0, 580, barX],
                 ["krawedz", 780, 0, barY]
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)
        ##############################################################3
        self.animal_list.add(mucha1)
        self.animal_list.add(mucha2)
        self.animal_list.add(mucha3)
        self.animal_list.add(mucha4)
def main():
    """ Main Program """
    #
    screen = pygame.display.set_mode([800, 600])
    pygame.display.set_caption('Nazwa')
    player = Player(50, 50)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)
    player.rect.x = 380
    player.rect.y = 270

    rooms = []

    room = Room1()
    rooms.append(room)
    room = Room2()
    rooms.append(room)
    room = Room3()
    rooms.append(room)
    room = Room4()
    rooms.append(room)
    room = Room5()
    rooms.append(room)
    room = Room6()
    rooms.append(room)
    room = Room7()
    rooms.append(room)
    room = wdworku()
    rooms.append(room)

    current_room_no = 0
    current_room = rooms[current_room_no]

    clock = pygame.time.Clock()

    # --------------------------------------------------------------
    f = pygame.font.SysFont('Bevan', 70);
    t = f.render('GTA', True, (255, 255, 255));
    screen.fill(GREEN)
    screen.blit(t, (170, 120));
    pygame.display.update();
    pygame.time.wait(1100);
    # -------------------------------------------------------------------

    done = False
    global lives
    lives = 3
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            global showme
            if event.type == pygame.KEYDOWN:
                showme=""
                if event.key == pygame.K_LEFT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, -5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 5)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -5)

        # --- Game Logic ---

        player.move(current_room.wall_list, current_room.char_list, current_room.animal_list)
        for item in current_room.animal_list:
            item.move(random.randint(-3,3), random.randint(-3,3))
        global cr
        if cr!=0:
            current_room_no = cr
            current_room = rooms[cr]
        if player.rect.x < -15:
            if current_room_no == 0:
                current_room_no = 2
                current_room = rooms[current_room_no]
                player.rect.x = 790
            elif current_room_no == 1:
                current_room_no = 0
                current_room = rooms[current_room_no]
                player.rect.x = 790
            else:
                current_room_no = 1
                current_room = rooms[current_room_no]
                player.rect.x = 790
        if player.rect.x > 801:
            if current_room_no == 0:
                current_room_no = 1
                current_room = rooms[current_room_no]
                player.rect.x = 0
            elif current_room_no == 1:
                current_room_no = 5
                current_room = rooms[current_room_no]
                player.rect.x = 0
            else:
                current_room_no = 0
                current_room = rooms[current_room_no]
                player.rect.x = 0
        if player.rect. y < -15:
            if current_room_no == 0:
                current_room_no = 3
                current_room = rooms[current_room_no]
                player.rect.y = 600
            elif current_room_no == 5:
                current_room_no = 6
                current_room = rooms[current_room_no]
                player.rect.y = 600
            else:
                current_room_no = 0
                current_room = rooms[current_room_no]
                player.rect.y = 600
        if player.rect.y > 600:
            if current_room_no == 3:
                current_room_no = 0
                current_room = rooms[current_room_no]
                player.rect.y = 0
            elif current_room_no == 6:
                current_room_no = 5
                current_room = rooms[current_room_no]
                player.rect.y = 0
            else:
                current_room_no = 4
                current_room = rooms[current_room_no]
                player.rect.y = 0

        # --- Drawing on screen---
        screen.fill(GREEN)
        screen.blit(current_room.room_background, [0,0])
        global score
        movingsprites.draw(screen)
        current_room.wall_list.draw(screen) # wyswietlanie scian
        current_room.char_list.draw(screen) # wyswietlanie postaci
        current_room.animal_list.draw(screen)  # wyswietlanie zwierzat
        label = myfont.render(showme, 1, (5, 5, 0))  # TEKST postaci
        screen.blit(label, (200, 100))
        points = myfont.render("Wynik: " + str(score), 1, WHITE) # WYNIK
        screen.blit(points, (720,2))
        if lives>2:
            screen.blit(heart, (640,3)) # ZYCIA
            screen.blit(heart, (660, 3))
            screen.blit(heart, (680, 3))
        elif lives>1:
            screen.blit(heart, (660,3)) # ZYCIA
            screen.blit(heart, (680, 3))
        elif lives ==1:
            screen.blit(heart, (680,3)) # ZYCIA
        else:
            done = True
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
