import pygame as pg, random as rnd

richtungen = {pg.K_DOWN:(0,1), pg.K_UP:(0,-1), pg.K_LEFT:(-1,0), pg.K_RIGHT:(1,0)}
spielerfigur = pg.image.load("Bilder/Münze-1.png")
bildgroessen = spielerfigur.get_rect()
BREITE = 1000
HÖHE = 600
tempo = 20
score = 0
f = open('Dateien/Münzen.dat', 'r')
line = f.read()
coins = int(line)

#defienieren

def button2():
    global GRÖSE
    global score
    global snake
    global richt_x
    global richt_y
    global bonus_x
    global bonus_y
    global bon_x
    global bon_y
    global snake2
    global x
    global y
    global Münzen
    global coin_x
    global coin_y
    global Game_Over
    global Start
    global tempo    
    GRÖSE = 20
    score = 0
    snake = [(BREITE//2, HÖHE//2)]
    richt_x, richt_y = 1, 0
    bonus_x, bonus_y = 300, 300
    bon_x, bon_y = 800, 300
    snake2 = 1
    x,y = snake[-1]
    x,y = x + richt_x * GRÖSE, y + richt_y * GRÖSE
    bonus_x, bonus_y = rnd.randrange(BREITE) // GRÖSE * GRÖSE, rnd.randrange(HÖHE) // GRÖSE * GRÖSE
    bon_x, bon_y = rnd.randrange(BREITE) // GRÖSE * GRÖSE, rnd.randrange(HÖHE) // GRÖSE * GRÖSE
    coin_x, coin_y = rnd.randrange(BREITE) // GRÖSE * GRÖSE, rnd.randrange(HÖHE) // GRÖSE * GRÖSE
    tempo = 5
    
    Game_Over = 0
    Start = 1

def draw_coin():
    global spielerfigur
    global bildgroessen
    spielerfigur = pg.image.load("Bilder/Münze-1.png")
    bildgroessen = spielerfigur.get_rect()

def Coins_Write():
    g = open('Dateien/Münzen.dat', 'w')
    h = g.write(str(coins))
    g.close()
    
    
#erste definitionen ausführen
Game_Over = 2
Start = 0
snake2 = 0

#weiter defieniere
def message(austext, Grose, Schrift, Farbe, Stelle):
    schrift = pg.font.SysFont(Schrift, Grose, True, False)
    text = schrift.render(austext, True, Farbe)
    screen.blit(text, Stelle)

def button(bx, by, lange2, hohe2, farbe_normal, farbe_aktiv):
    global aktiv
    if maus[0] > bx and maus[0] < bx+lange2 and maus[1] > by and maus[1] < by+hohe2:
        pg.draw.rect(screen, farbe_aktiv, (bx, by, lange2, hohe2))
        if klick[0] == 0:
            aktiv = False
        if klick[0] == 1 and aktiv == False:
            aktiv == True
            button2()
    else:
        pg.draw.rect(screen, farbe_normal, (bx, by, lange2, hohe2))


a = 0
pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])

# Fenster Schleife wird gesetzt
weitermachen = True
clock = pg.time.Clock()

#Musik
hallo = pg.mixer.music.load('Musik/Heaven_and_Hell.ogg')
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(.1)


#Schleife
while weitermachen:
    clock.tick(tempo)
    screen.fill((0,0,0))
    maus = pg.mouse.get_pos()
    klick = pg.mouse.get_pressed()

    # Ereignisse
    for ereignis in pg.event.get():
        if ereignis.type == pg.QUIT:
            weitermachen = False
        if ereignis.type == pg.KEYDOWN and ereignis.key in richtungen:
            richt_x, richt_y = richtungen[ereignis.key]

    #Game Over
    if snake2 == 1:
        x,y = snake[-1]
        x,y = x + richt_x * GRÖSE, y + richt_y * GRÖSE


    if Game_Over == 0:
        if x < 0 or x + GRÖSE > BREITE or y + GRÖSE > HÖHE or y < 0 or (x,y) in snake:
            Game_Over = 1
            Start = 0
        
    if Game_Over == 1:
        tempo = 20
        message('Game Over', 50, 'Arial', [255, 0, 0], [380, 280])

        f = open('Dateien/HS.dat', 'r')
        line = f.read()
        k = int(line)
        button(430, 350, 160, 60,[155, 0, 0], [255, 0, 0])
        message('Restart', 40, 'Arial', [0, 0, 0], [438, 360])


    if Start == 0:
        message("Highscore: " + str(line), 35, 'Arial', [255, 255, 255], [750, 0])


        if snake2 == 1:
            del snake[0]
            del bon_x
            del bon_y
            del bonus_x
            del bonus_y
            snake2 = 0

            if score > k:
                g = open('Dateien/HS.dat', 'w')
                h = g.write(str(score))
                g.close()
        f.close()
        if Start == 0 and Game_Over == 2:
            button(420, 250, 160, 60,[155, 0, 0], [255, 0, 0])
            message('Start', 40, 'Arial', [0, 0, 0], [450, 260])
        


    #Eigentliches Spiel
    if Game_Over == 0:
        snake.append((x,y))

    if snake2 == 1:
        if x == bonus_x and y == bonus_y:
            score += 1
            tempo += 1
            bonus_x = rnd.randrange(BREITE) // GRÖSE * GRÖSE
            bonus_y = rnd.randrange(HÖHE) // GRÖSE * GRÖSE
        elif x == bon_x and y == bon_y:
            score += 5
            tempo += 2
            bon_x = rnd.randrange(BREITE) // GRÖSE * GRÖSE
            bon_y = rnd.randrange(HÖHE) // GRÖSE * GRÖSE
            a = 1
        elif a == 1:
            a = 0
        else:
            del snake[0]

        if x == coin_x and y == coin_y:
            coin_x = rnd.randrange(BREITE) // GRÖSE * GRÖSE
            coin_y = rnd.randrange(HÖHE) // GRÖSE * GRÖSE
            coins += 1
            effect = pg.mixer.Sound('Musik/Coin.ogg')
            effect.play()
        

        for x,y in snake:
            pg.draw.rect(screen,(0,255,255),(x,y,GRÖSE, GRÖSE))
        pg.draw.rect(screen,(255,0,0),(bonus_x,bonus_y,GRÖSE, GRÖSE))
        pg.draw.rect(screen,(0,255,0),(bon_x,bon_y,GRÖSE, GRÖSE))
        screen.blit(spielerfigur, (coin_x , coin_y))
    message("Punkte: " + str(score), 35, 'Arial', [255, 255, 255], [0, 0])
    message("Münzen: " + str(coins), 35, 'Arial', [255, 255, 255], [750, 565])
    Coins_Write()

    #sonstige Funktionen
    gameicon = pg.image.load('Bilder/icon.png')
    pg.display.set_icon(gameicon)

    pg.display.set_caption("Pixel Eating")

    pg.display.flip()
        
pg.quit()
