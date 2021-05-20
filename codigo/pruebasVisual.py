
import pygame 
import sys
import time

pygame.init()
pygame.display.set_caption("Torres de Hanoi")  
WIN = pygame.display.set_mode((1100, 700))
clock = pygame.time.Clock()

juego_realizado = False
FPS = 60

#listado de colores 
blanco = (255, 255, 255)
negro = (0, 0, 0)
ROJO = (255, 0, 0)
gold = (239, 229, 51)
azul = (78,162,196) 
gris = (170, 170, 170)
verde = (77, 206, 145)
pasos_H = 0
n_disco = 3
disco = []
towers_midx = [250, 550, 850]
indicador = 0
validador = False
floater = 0

#--------------------------------------------------------------------------------------- metodos -----------------------------------------------

def blit_text(WIN, text, midtop, aa=True, font=None, tipo_letra = None, size = None, color=(255,0,0)):
    if font is None:                                   
        font = pygame.font.SysFont(tipo_letra, size)   
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    WIN.blit(font_surface, font_rect)

def menu_inicial(): 
    global WIN, n_disco, juego_realizado
    menu_done = False
    while not menu_done: 
        background = pygame.image.load("fondo.jpg").convert()                
        WIN.blit(background,[0,0])
        blit_text(WIN, 'Cantidad de Discos', (600, 50), tipo_letra='sans serif', size=70, color=negro)
        blit_text(WIN, str(n_disco), (550, 150), tipo_letra='sans serif', size=700, color=ROJO)
        blit_text(WIN, 'presiona la tecla enter para continuar', (600, 650), tipo_letra='sans_serif', size=70, color=negro)
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_done = True
                    juego_realizado = True
                if event.key == pygame.K_RETURN:
                    menu_done = True
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_disco += 1
                    if n_disco > 6:
                        n_disco = 6
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disco -= 1
                    if n_disco < 1:
                        n_disco = 1
            if event.type == pygame.QUIT:
                menu_done = True
                juego_realizado = True
        pygame.display.flip()
        clock.tick(60)

def juego_terminado():
    global WIN, pasos_H
    background = pygame.image.load("fondo.jpg").convert()                
    WIN.blit(background,[0,0])
    min_pasos_H = 2**n_disco-1
    
    blit_text(WIN, 'Ganaste', (560, 50), tipo_letra='sans serif', size=380, color=gold)
    blit_text(WIN, 'Pasos:  '+ str(pasos_H), (320, 360), tipo_letra='mono', size=50, color=negro)
    blit_text(WIN, 'minimo'+str(min_pasos_H), (50, 800), tipo_letra='mono', size=30, color=ROJO)
    if min_pasos_H==pasos_H:
        blit_text(WIN, 'Ganaste', (560, 50), tipo_letra='mono', size=50, color=verde
    )
    pygame.display.flip()
    time.sleep(2)    
    pygame.quit()   
    sys.exit()  

def dibujar_Torres():
    global WIN
    for xpos in range(100, 950, 300):
        pygame.draw.rect(WIN, ROJO, pygame.Rect(xpos, 500, 270 , 20))
        pygame.draw.rect(WIN, ROJO, pygame.Rect(xpos+140, 200, 10, 290))
    blit_text(WIN, '1', (towers_midx[0], 603), tipo_letra='mono', size=60, color=negro)
    blit_text(WIN, '2', (towers_midx[1], 603), tipo_letra='mono', size=60, color=negro)
    blit_text(WIN, '3', (towers_midx[2], 603), tipo_letra='mono', size=60, color=negro)

    


def crear_Disco():
    global n_disco, disco
    disco = []
    height = 20
    ypos = 480- height
    width = n_disco * 23
    for i in range(n_disco):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height)
        disk['rect'].midtop = (244, ypos)
        disk['val'] = n_disco-i
        disk['tower'] = 0
        disco.append(disk)
        ypos -= height+3
        width -= 23


def dibujar_disco():
    global WIN, disco
    for disk in disco:
        pygame.draw.rect(WIN, blanco, disk['rect'])
    return

def draw_ptr():
    ptr_points = [(towers_midx[indicador]-7 ,540), (towers_midx[indicador]+7, 540), (towers_midx[indicador], 533)]
    
    pygame.draw.polygon(WIN, ROJO, ptr_points)
    return

def verificador():
    global disco
    over = True
    for disk in disco:
        if disk['tower'] != 2:
            over = False
    if over:
        time.sleep(0.2)
        juego_terminado()

def reset():
    global pasos_H,indicador,validador,floater
    pasos_H = 0
    indicador = 0
    validador = False
    floater = 0
    menu_inicial()
    crear_Disco()


menu_inicial()
crear_Disco()

#mis eventos___________________________________________________________________________________________________
while not juego_realizado:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego_realizado = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                reset()
            if event.key == pygame.K_q:
                juego_realizado = True
            if event.key == pygame.K_RIGHT:
                indicador = (indicador+1)%3
                if validador:
                    disco[floater]['rect'].midtop = (towers_midx[indicador], 100)
                    disco[floater]['tower'] = indicador
            if event.key == pygame.K_LEFT:
                indicador = (indicador-1)%3
                if validador:
                    disco[floater]['rect'].midtop = (towers_midx[indicador], 100)
                    disco[floater]['tower'] = indicador
            if event.key == pygame.K_UP and not validador:
                for disk in disco[::-1]:
                    if disk['tower'] == indicador:
                        validador = True
                        floater = disco.index(disk)
                        disk['rect'].midtop = (towers_midx[indicador], 100)
                        break
            if event.key == pygame.K_DOWN and validador:
                for disk in disco[::-1]:
                    if disk['tower'] == indicador and disco.index(disk)!=floater:
                        if disk['val']>disco[floater]['val']:
                            validador = False
                            disco[floater]['rect'].midtop = (towers_midx[indicador], disk['rect'].top-23)
                            pasos_H += 1
                        break
                else: 
                    validador = False
                    disco[floater]['rect'].midtop = (towers_midx[indicador], 492-23)
                    pasos_H += 1
    background = pygame.image.load("fondo.jpg").convert()                
    WIN.blit(background,[0,0])
    dibujar_Torres()
    dibujar_disco()
    draw_ptr()
    blit_text(WIN, 'Pasos: '+str(pasos_H), (500, 20), tipo_letra='mono', size=80, color=negro)
    pygame.display.flip()
    if not validador:verificador()
    clock.tick(FPS)


    