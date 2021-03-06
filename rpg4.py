import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (50, 140, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
DARK_RED = (173, 17, 17)

pygame.init()

# nazwy plikow png -----------------------------------------------------------------------------------------------------
heart = pygame.image.load("heart.png")
flower = pygame.image.load("flower.png")
tadeuszP = "tadko.png"
telimenaP = "telimena.png"
wojskiP = "wojski.png"
zosiaP = "zosia.png"
sedziaP = "sedzia.png"
hrabiaP = "hrabia.png"
gerwazyP = "gerwazy.png"
mackoP = "macko.png"
mushroom = pygame.image.load("mushroom.png")
barX = pygame.image.load("barX.png")
barY = pygame.image.load("barY.png")
zameksign = pygame.image.load("zameksign.png")
lassign = pygame.image.load("lassign.png")
dworeksign = pygame.image.load("dworeksign.png")
dobrzynsign = pygame.image.load("dobrzyn.png")
dworekP = pygame.image.load("dworek.png")
zamekP = pygame.image.load("zamek.png")
ramka = pygame.image.load("ramka.png")

# zmienne pomocnicze globalne ------------------------------------------------------------------------------------------
points = {'mushroom': 0, 'dworek': 0, 'zamek': 0 }
answers = {'zosia': 0, 'telimena': 0, 'gerwazy': 0, 'macko': 0, 'sedzia': 0, 'wojski': 0, 'hrabia': 0}
myfont = pygame.font.SysFont("monotypecorsiva", 20)
score = 0
text_field_att = False
char = 'zosia'
lives = 3
cr = 0  # wejscie do dworku / zamku
pl = [0, 0]

# funkcje wyswietlania tekstu ------------------------------------------------------------------------------------------
gameDisplay = pygame.display.set_mode((800, 600))


def texts(lines, x, y, myfont, h):
    text = myfont.render('', 1, WHITE)
    textrect = text.get_rect()
    textrect.x = x
    textrect.y = y
    lines = lines.split('\n')
    for i in lines:
        text = myfont.render(i, 1, WHITE)
        textrect.centery += h
        gameDisplay.blit(text, textrect)


# zwierzeta ------------------------------------------------------------------------------------------------------------


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

mucha1 = Animal("mucha", 20, 50, "fly.png")
mucha2 = Animal("mucha", 750, 120, "fly.png")
mucha3 = Animal("mucha", 590, 580, "fly.png")
mucha4 = Animal("mucha", 490, 400, "fly.png")
bear = Animal("bear", 300, 300, "niedz.png")

# ----------------------------------------------------------------------------------------------------------------------

# definicje postaci ----------------------------------------------------------------------------------------------------


class Character(pygame.sprite.Sprite):

    def __init__(self, name, x, y, pic, text, answer):
        super().__init__()
        self.image = pygame.image.load(pic)
        self.name = name
        self.text = text
        self.answer = answer

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

hrabia = Character("hrabia", 60, 300, hrabiaP, """
Hrabi tekst
A 0
B 0
C 0
""", pygame.K_0)
zosia = Character("zosia", 30, 200, zosiaP, """
Witaj mój najsłodszy! Ja jak zwykle w ogródku ;). Widzę, że wiedziałeś gdzie mnie szukać.
Popatrz na moje uprawy, czyż nie jest cudownie patrzeć jak to wszystko rośnie i dojrzewa?
Ah mój najdroższy! Masz ze sobą obrazek, który ci dałam gdy wyjeżdżałeś? Na pewno masz go ze sobą!
Pamiętasz kto na nim był?
A św. Genowefa
B św. Józef
C św. Katarzyna
""", pygame.K_a)
sedzia = Character("sedzia", 30, 200, sedziaP, """
Witaj Tadeuszu! Dobrze cię widzieć! Szukasz swojej Zosieńki? To tak dobra dziewczyna!
I do tego całkiem gospodarna i ładniutka. Telimena wszystkiego ją nauczyła. Jaka szkoda,
że jej matka Ewa nie dożyła tego czasu, gdy to dziewcze tak wyrosło. Jesteś od niej starszy Tadeuszu,
musisz dbać o tą delikatną istotę. Zaraz... Właściwie ile wy macie lat? (Zosia, Tadeusz)
A 18, 22
B 14, 20
C 16, 20
""", pygame.K_b)
wojski = Character("wojski", 230, 100, wojskiP, "jestem wojski", pygame.K_0)
telimena = Character("telimena", 230, 200, telimenaP, """
Kogo ja widzę? Przyszedłeś mi znów pomóc pozbyć się tych paskudnych owadów?
Bardzo cenię sobie Twoją pomoc... Na szczęście nie widziałam tu dzisiaj tych okropnych mrówek.
Spotkałeś może Hrabiego? Ah, to i tak już teraz nieważne... Nie wiem czy wiesz,
ale wybieramy się z mężem w podróż do Petersburga.
Tadeuszu! Czy ty mnie w ogóle słuchasz?! Pewnie na pamiętasz nawet kto jest moim mężem...
A Rejent
B Asesor
C Hreczecha
""", pygame.K_a)
gerwazy = Character("gerwazy", 320, 450, gerwazyP, """
Mopanku Mopanku! Cóż Ty robisz przy tym Zamku? Jeśliś przyszedł do Hrabiego,
to Pana nie ma w tejże chwili. A to ostatni z Horeszków po kądzieli.
Ma najszlachetniejszy spośród najszlachetniejszych herbów. Każdy powinien wiedzieć jak wygląda.
Żywię nadzieję, że pamiętasz co jest przedstawione na tym herbie.
A Stokozic
B Półrożec
C Półkozic
""", pygame.K_c)
macko = Character("macko", 100, 100, mackoP, """
Witaj w Dobrzynie przyjacielu! O! Uważaj na tego królika! Jest najodważniejszy z całej gromady.
Mówię na niego Bartek Ważniak. Pewnie wiesz, że tu u nas w Dobrzynie mężczyźni mają na imię
Bartek lub Maciek. Wśród kobiet też tylko dwa imiona cieszą się popularnością.
Pamiętasz chociaż jedno z nich?
A Jóźka
B Maryna
C Danuśka
""", pygame.K_b)
# ----------------------------------------------------------------------------------------------------------------------


class Wall(pygame.sprite.Sprite):

    def __init__(self, name, x, y, pic):
        super().__init__()
        self.image = pic
        self.name = name
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Player(pygame.sprite.Sprite):

    change_x = 0
    change_y = 0
    speed = [0, 0]

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(tadeuszP)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.speed = [0,0]

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y
        self.speed = [self.change_x, self.change_y]

    def move(self, walls, chars, anim):

        global char
        global cr
        global lives
        global score
        global gameDisplay
        global text_field_att
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if block.name == "mushroom":
                # showme = "you chose wisely" - do zmiany
                if points['mushroom'] == 0:
                    points['mushroom'] = 1
                    score += 1
            elif block.name == "krawedzEnd":
                if points['dworek'] == 0:
                    points['dworek'] = 1
                    score += 1
                    cr = 3
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        #################################################################

        char_hit_list = pygame.sprite.spritecollide(self, chars, False)
        for character in char_hit_list:
            char = character
            text_field_att = True
            if self.change_x > 0:
                self.rect.right = character.rect.left
            else:
                self.rect.left = character.rect.right
        animal_hit_list = pygame.sprite.spritecollide(self, anim, True)
        if animal_hit_list:
            lives -= 1

        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if block.name == "dworek" and self.change_y<0:  # wejscie do dworku
                if points['dworek'] == 0:
                    cr = 7
                    gameDisplay.blit(ramka, (20, 20))
                    texts("""
Ah! Co tu się dzieje?! Skąd się tu wzięło tyle much?! I to nie byle jakich! Przecież to muchy szlacheckie!
Toż to specjalność Wojskiego! Wygląda na to, że największy wróg tych owadów gdzieś się zawieruszył...
No cóż... W takim wypadku Tadeuszku, musisz przedrzeć się przez labirynt Dworku,
uważając by nie wpaść w żadną z much. Powodzenia!
(naciśnij spację by kontynuować)
                    """, 34, -3, myfont, 22)
                    pygame.display.update()
                    done = False
                    while not done:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    done = True
            elif block.name == "krawedzXzamek":
                if points['zamek'] == 0:
                    points['zamek'] = 1
                    score += 1
                    cr = 2
            elif block.name == "zycie":
                if lives==2:
                    lives = 3
                    block.kill()
                elif lives==1:
                    lives = 2
                    block.kill()
            elif block.name == "zamek" and self.change_y<0:
                if points['zamek'] == 0:
                    gameDisplay.blit(ramka, (20, 20))
                    texts("""
Instrukcja do zamku.
Powodzenia!
(naciśnij spację by kontynuować)
                    """, 34, -3, myfont, 22)
                    pygame.display.update()
                    done = False
                    while not done:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    done = True
                    self.change_x = 0
                    cr = 8
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        #########################################################################

        char_hit_list = pygame.sprite.spritecollide(self, chars, False)
        for character in char_hit_list:
            char = character
            text_field_att = True
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
    # cr = 0
    def __init__(self):
        super().__init__("grasscross.png")

        # lista obiektow w pokoju (nazwa wsporzedne x i y i obrazek do podstawienia) - DO ZMIANY
        walls = [["zameksign", 50, 190, zameksign],
                 ["lassign", 600, 190, lassign],
                 ["dworeksign", 410, 10, dworeksign],
                 ["dobrzynsign", 410, 500, dobrzynsign]
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)


class Room2(Room):
    """wszystko w 2. pokoju"""

    def __init__(self):
        super().__init__("grassroadend2.png")

        # DO ZMIANY:
        walls = [["krawedz", 0, 0, barX],
                 ["krawedz", 0, 580, barX],
                 ["mushroom", 680, 350, mushroom]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)
        self.char_list.add(wojski)


class Room3(Room):
    """wszystko w 3. pokoju"""

    def __init__(self):
        super().__init__("grassroadend.png")

        walls = [["krawedz", 0, 0, barY],
                 ["krawedz", 0, 0, barX],
                 ["krawedz", 0, 580, barX],
                 ["zamek", 250, 200, zamekP]
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)

        # #############################################################33

        self.char_list.add(zosia)
        self.char_list.add(hrabia)
        self.char_list.add(gerwazy)


class Room4(Room):
    """wszystko w 4. pokoju"""

    def __init__(self):
        super().__init__("grassroadend4.png")

        walls = [["krawedz", 0, 0, barY],
                 ["krawedz", 0, 0, barX],
                 ["krawedz", 780, 0, barY],
                 ["dworek", 270, 170, dworekP],
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)

        # #############################################################3

        self.char_list.add(sedzia)
        self.char_list.add(hrabia)


class Room5(Room):
    """wszystko w 5. pokoju"""

    def __init__(self):
        super().__init__("grassroadend3.png")

        walls = [["krawedz", 0, 0, barY],
                 ["krawedz", 0, 580, barX],
                 ["krawedz", 780, 0, barY]
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)

        # #############################################################3

        self.char_list.add(macko)


class Room6(Room):
    """wszystko w 6. pokoju"""

    def __init__(self):
        super().__init__("grass.png")

        # DO ZMIANY:
        walls = [["krawedz", 0, 580, barX],
                 ["krawedz", 780, 0, barY],
                 ["mushroom", 680, 350, mushroom]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)
        self.char_list.add(telimena)


class Room7(Room):
    """wszystko w 7. pokoju"""

    def __init__(self):
        super().__init__("grass.png")

        walls = [["krawedz", 0, 0, barY],
                 ["krawedz", 0, 0, barX],
                 ["krawedz", 780, 0, barY]
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)

        # #############################################################3

            self.animal_list.add(bear)


class wdworku(Room):
    """wszystko w dworku"""
    # cr = 7

    def __init__(self):
        super().__init__("floor.png")
        dwX = pygame.image.load("dwX.png")
        dwY = pygame.image.load("dwY.png")
        dwEnd =pygame.image.load("dwEnd.png")
        walls = [["krawedz", 0, 0, barY],
                 ["krawedz", 0, 0, barX],
                 ["krawedz", 0, 580, barX],
                 ["krawedz", 780, 0, barY],
                 ["krawedzEnd", 20, 20, dwEnd],
                 ["zycie", 40, 540, heart],
                     #         labirynt
                 ["krawedz", 680, 480, dwY],
                 ["krawedz", 580, 370, dwY],
                 ["krawedz", 480, 480, dwY],
                 ["krawedz", 380, 370, dwY],
                 ["krawedz", 280, 480, dwY],
                 ["krawedz", 180, 370, dwY],
                 ["krawedz", 80, 480, dwY],

                 ["krawedz", 680, 350, dwX],
                 ["krawedz", 580, 350, dwX],
                 ["krawedz", 480, 350, dwX],
                 ["krawedz", 380, 350, dwX],
                 ["krawedz", 280, 350, dwX],
                 ["krawedz", 180, 350, dwX],
                 ["krawedz", 80, 350, dwX],

                 ["krawedz", 680, 260, dwY],
                 ["krawedz", 580, 140, dwY],
                 ["krawedz", 480, 260, dwY],
                 ["krawedz", 380, 140, dwY],
                 ["krawedz", 280, 260, dwY],
                 ["krawedz", 180, 140, dwY],
                 ["krawedz", 80, 260, dwY],

                 ["krawedz", 580, 120, dwX],
                 ["krawedz", 480, 120, dwX],
                 ["krawedz", 380, 120, dwX],
                 ["krawedz", 280, 120, dwX],
                 ["krawedz", 180, 120, dwX],
                 ["krawedz", 80, 120, dwX],
                 ["krawedz", 0, 120, dwX],
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)

        # #############################################################3

        self.animal_list.add(mucha1)
        self.animal_list.add(mucha2)
        self.animal_list.add(mucha3)
        self.animal_list.add(mucha4)


class wzamku(Room):
    """wszystko w zamku"""
    # cr = 8

    def __init__(self):
        super().__init__("floor.png")

        walls = [["krawedz", 0, 0, barY],
                 ["krawedzXzamek", 0, 0, barX],
                 ["krawedz", 0, 580, barX],
                 ["krawedz", 780, 0, barY]
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)

        # #############################################################3


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
    room = wzamku()
    rooms.append(room)

    current_room_no = 0
    current_room = rooms[current_room_no]

    clock = pygame.time.Clock()

    # ------------------------------------------------------------------------------------------------------------------
    screen.fill(GREEN)
    font1 = pygame.font.SysFont("monotypecorsiva", 100)
    texts("""
GTA 1812
    """, 190, 200, font1, 0)
    pygame.display.update()
    pygame.time.wait(2500)
    # ------------------------------------------------------------------------------------------------------------------
    screen.fill(GREEN)
    font2 = pygame.font.SysFont("monotypecorsiva", 30)
    texts("""
Witaj!
Jestem kosmitą Brajankiem z planety Sepulka. Przybyłem na Ziemię,
by ją poznać i podbić, a potem odbudować Sepulkę na jej obraz
i podobieństwo. Mój dom jest teraz w stanie kosmicznego konfliktu.
Wojna trwa już 3921 lat i 4 miesiace. Bratobójcze walki Sepulków
sprawiły, że nas Sepulczan Krótkonosych została już tylko garstka.
Zawsze byłem pod wrażeniem Was, Ziemian, że potraficie żyć ze sobą
w zgodzie i pokoju. Aby zachować nasz gatunek
(nim Sepulczanie Szerokostopi wybiją nas całkowicie)
postanowiłem przylecieć na Ziemię, by znaleźć rozwiązanie na nasze
problemy i zbudować nasze społeczeństwo na bazie Waszego.
                                                                            strona 1/2

Naciśnij spację, by kontynuować
    """, 25, -30, font2, 33)
    pygame.display.update()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True
    # ------------------------------------------------------------------------------------------------------------------
    screen.fill(GREEN)
    font2 = pygame.font.SysFont("monotypecorsiva", 30)
    texts("""
Wybrałem Soplicowo, ponieważ tam wszystko jest uporządkowana
i zharmonizowane. Postanowiłem przebrać się za jednego
z tam bywających osobników. Jest to niejaki Tadeusz Soplica,
bratanek najważniejszej osoby we wsi - Sędziego. Aby zebrać
potrzebne mi informacje muszę najpierw wzbudzić zaufanie
w mieszkańcach Soplicowa i ich przyjaciołach. Muszą mi
uwierzyć, że jestem Tadeuszem. Będą mi zadawać różne pytania,
na które powinienem znać odpowiedź. I tutaj potrzebuję Twojej
pomocy. Pomóż mi odnaleźć wszystkie postacie i odpowiedzieć
na ich pytania, by w Sepulce znów nastał pokój!
Liczę na Ciebie!
                                                                            strona 2/2

Naciśnij spację, by rozpocząć przygodę!
        """, 25, -30, font2, 33)
    pygame.display.update()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True
    # ------------------------------------------------------------------------------------------------------------------
    done = False
    global lives
    lives = 3
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            global char
            global text_field_att
            if event.type == pygame.KEYDOWN:
                text_field_att = False
                if event.key == pygame.K_LEFT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, -5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 5)

            elif event.type == pygame.KEYUP:
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
            item.move(random.randint(-3, 3), random.randint(-3, 3))
        global cr
        if cr != 0:
            if current_room_no<6:
                player.changespeed(-1*player.speed[0],-1*player.speed[1])
            current_room_no = cr
            current_room = rooms[current_room_no]
            if cr == 7 or cr ==8:
                player.rect.y = 490
                player.rect.x = 740
            else:
                player.rect.y = 470
                player.rect.x = 390
            cr = 0
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
        if player.rect.x > 805:
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
        if player.rect.y > 605:
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

        # --- Drawing on screen ---
        screen.blit(current_room.room_background, [0, 0])
        global score
        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)  # wyswietlanie scian
        current_room.char_list.draw(screen)  # wyswietlanie postaci
        current_room.animal_list.draw(screen)  # wyswietlanie zwierzat
        if text_field_att and answers[char.name] == 0:  # wyswietlanie ramki i tekstow postaci
            screen.blit(ramka, (20, 20))
            global myfont
            texts(char.text, 34, -10, myfont, 22)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == char.answer:
                        score += 1
                        answers[char.name] = 1
                    elif event.key == pygame.K_a or event.key == pygame.K_b or event.key == pygame.K_c:
                        lives -= 1
            player.change_x = 0
            player.change_y = 0
        points = myfont.render("Wynik: " + str(score), 1, WHITE)  # WYNIK
        screen.blit(points, (720, 2))
        if lives > 2:
            screen.blit(heart, (650, 4))
            screen.blit(heart, (670, 4))
            screen.blit(heart, (690, 4))
        elif lives > 1:
            screen.blit(heart, (670, 4))  # ZYCIA
            screen.blit(heart, (690, 4))
        elif lives == 1:
            screen.blit(heart, (690, 4))  # ZYCIA
        else:
            # --- Game Over ---
            screen.fill(DARK_RED)
            font3 = pygame.font.SysFont("monotypecorsiva", 60)
            texts("""
Koniec Gry
            """, 300, 200, font3, 0)
            pygame.display.update()
            pygame.time.wait(3000)
            done = True
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
