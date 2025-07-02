import os
import pygame
import random
from Constantes import *

# ------------------- CREACION DE BOTONES ------------------- #

def calcular_posicion_centrada_x(ancho):
   
    return (ANCHO_VENTANA - ancho) // 2


def crear_boton(tipo_de_valor: str, ventana: pygame.Surface) -> pygame.Rect:
    
    ancho_ventana = ventana.get_width()
    alto_ventana = ventana.get_height()
    ancho = int(ancho_ventana * 0.2)
    alto = int(alto_ventana * 0.07)
    x_centro = (ancho_ventana - ancho) // 2

    posiciones = {
        'jugar':      (x_centro, int(alto_ventana * 0.38)),
        'dificultad': (x_centro, int(alto_ventana * 0.50)),
        'puntajes':   (x_centro, int(alto_ventana * 0.63)),
        'salir':      (x_centro, int(alto_ventana * 0.79)),
        'reiniciar': (int(ancho_ventana * 0.02), int(alto_ventana * 0.35)),
        'volver':     (int(ancho_ventana * 0.02), int(alto_ventana * 0.45))
    }

    x, y = posiciones.get(tipo_de_valor, (x_centro, int(alto_ventana * 0.5)))
   
    return pygame.Rect(x, y, ancho, alto)

# ------------------- DETECCION DE CLICKS Y HOVER ------------------- #

def calcular_posicion_matriz(pos, superficie, filas, columnas):
    x_mouse, y_mouse = pos
    ancho_ventana, alto_ventana = superficie.get_size()

    tamaño_casilla_preferido = 40
    margen = 130
    ancho_disponible = ancho_ventana - 2 * margen
    alto_disponible = alto_ventana - 2 * margen

    tamaño_casilla = tamaño_casilla_preferido

    if columnas * tamaño_casilla > ancho_disponible:
        tamaño_casilla = ancho_disponible // columnas
    if filas * tamaño_casilla > alto_disponible:
        tamaño_casilla = min(tamaño_casilla, alto_disponible // filas)

    ancho_total_matriz = columnas * tamaño_casilla
    alto_total_matriz = filas * tamaño_casilla
    x_inicial = (ancho_ventana - ancho_total_matriz) // 2
    y_inicial = (alto_ventana - alto_total_matriz) // 2

    # Verificar si el click está dentro del área del tablero
    if not (x_inicial <= x_mouse < x_inicial + ancho_total_matriz and y_inicial <= y_mouse < y_inicial + alto_total_matriz):
        return -1, -1  # Click fuera del tablero

    col = (x_mouse - x_inicial) // tamaño_casilla
    fila = (y_mouse - y_inicial) // tamaño_casilla

    return fila, col

def procesar_click_en_menu_nuevo(posicion, ventana):
    
    tipos_de_valor = ['jugar', 'dificultad', 'puntajes', 'salir']
    botones = []
    
    for tipo in tipos_de_valor:
        boton = crear_boton(tipo, ventana)
        botones.append(boton)
    
    indice = -1
    for i in range(len(botones)):
        if botones[i].collidepoint(posicion):
            indice = i
            break
    
    return indice

def detectar_hover_en_menu_nuevo(posicion, ventana):
    
    tipos_de_valor = ['jugar', 'dificultad', 'puntajes', 'salir']
    botones = []
    
    for tipo in tipos_de_valor:
        boton = crear_boton(tipo, ventana)
        botones.append(boton)
    
    indice = -1
    for i in range(len(botones)):
        if botones[i].collidepoint(posicion):
            indice = i
            break
    
    return indice


def procesar_click_en_otras_pantallas(posicion, ventana):
    boton_volver = crear_boton('volver', ventana)
    boton_reiniciar = crear_boton('reiniciar', ventana)

    return (boton_reiniciar.collidepoint(posicion),boton_volver.collidepoint(posicion))


def detectar_hover_en_otras_pantallas(posicion, ventana):
    boton_reiniciar = crear_boton('reiniciar', ventana)
    boton_volver = crear_boton('volver', ventana)
    
    indice = -2
    if boton_volver.collidepoint(posicion):
        indice = 0
    if boton_reiniciar.collidepoint(posicion):
        indice = 1
    
    return indice
                             

# ------------------- INTERFAZ ------------------- #

def dibujar_boton_en_pantalla(rect, texto, hover):
   
    color = COLOR_BOTON_ENCIMA if hover else COLOR_BOTON_NORMAL                             # CAMBIAR
    pygame.draw.rect(pygame.display.get_surface(), color, rect)
    pygame.draw.rect(pygame.display.get_surface(), COLOR_TEXTO_NORMAL, rect, 2)
    fuente = pygame.font.SysFont("Verdana", 25)
    texto_surf = fuente.render(texto, True, COLOR_TEXTO_NORMAL)
    texto_rect = texto_surf.get_rect(center=rect.center)
    pygame.display.get_surface().blit(texto_surf, texto_rect)

def dibujar_titulo_centrado(texto, y, tipo_fuente):

    superficie = pygame.display.get_surface()
    ancho_ventana = superficie.get_width()
    alto_ventana = superficie.get_height()


    if tipo_fuente == "grande":
        tamaño_fuente = int(ancho_ventana * 0.06)
        fuente = pygame.font.SysFont("Impact", tamaño_fuente)
    elif tipo_fuente == "mediana":
        tamaño_fuente = int(ancho_ventana * 0.04)
        fuente = pygame.font.SysFont("Verdana", tamaño_fuente)
    else:
        tamaño_fuente = int(ancho_ventana * 0.025)
        fuente = pygame.font.SysFont("Verdana", tamaño_fuente)

    texto_surf = fuente.render(texto, True, COLOR_TITULO_PRINCIPAL)

    desplazamiento_y = int(alto_ventana * 0.05)
    rect = texto_surf.get_rect(center=(ancho_ventana // 2, y + desplazamiento_y))

    superficie.blit(texto_surf, rect)

# ------------------- MATRIZ BUSCAMINAS ------------------- #

def inicializar_matriz(filas, columnas, minas):
   
    matriz = []
   
    for _ in range(filas):
        fila = [''] * columnas
        matriz.append(fila)
    
    cantidad = 0
    
    while cantidad < minas:
        f = random.randint(0, filas - 1)
        c = random.randint(0, columnas - 1)
        if matriz[f][c] != 'X':
            matriz[f][c] = 'X'
            cantidad += 1
    
    return matriz

def generar_matriz_numeros(matriz):
   
    filas, columnas = len(matriz), len(matriz[0])
    numeros = []
    
    for i in range(filas):
        fila_numeros = []
        for j in range(columnas):
            if matriz[i][j] == 'X':
                fila_numeros.append('X')
            else:
                cuenta = 0
                vecinos = [
                    (i-1, j-1), (i-1, j), (i-1, j+1),
                    (i, j-1),             (i, j+1),
                    (i+1, j-1), (i+1, j), (i+1, j+1)
                ]
                for ni, nj in vecinos:
                   
                    if ni < 0 or ni >= filas:
                        continue
                   
                    if nj < 0 or nj >= columnas:
                        continue
                   
                    if matriz[ni][nj] == 'X':
                        cuenta += 1
                fila_numeros.append(cuenta)
        numeros.append(fila_numeros)
  
    return numeros


def dibujar_matriz_buscaminas(superficie, numeros, estado, banderas, fuente, imagen_bomba, imagen_bandera, mostrar_todas_bombas=False):
   
    # Obtener dimensiones de la ventana
    ancho_ventana = superficie.get_width()
    alto_ventana = superficie.get_height()
    
    # Dimensiones de la matriz
    filas = len(numeros)
    columnas = len(numeros[0])
    
    # Tamaño preferido de cada casilla
    tamaño_casilla_preferido = 40
    
    # Calcular el tamaño total de la matriz con tamaño preferido
    ancho_total_preferido = columnas * tamaño_casilla_preferido
    alto_total_preferido = filas * tamaño_casilla_preferido
    
    # Verificar si la matriz cabe en la ventana (dejando un margen)
    margen = 130
    ancho_disponible = ancho_ventana - (2 * margen)
    alto_disponible = alto_ventana - (2 * margen)
    
    # Calcular el tamaño de casilla ajustado si es necesario
    tamaño_casilla = tamaño_casilla_preferido
    
    if ancho_total_preferido > ancho_disponible:
        tamaño_por_ancho = ancho_disponible // columnas
        tamaño_casilla = tamaño_por_ancho
    
    if alto_total_preferido > alto_disponible:
        tamaño_por_alto = alto_disponible // filas
        if tamaño_por_alto < tamaño_casilla:
            tamaño_casilla = tamaño_por_alto
    
    # Calcular el tamaño total real de la matriz
    ancho_total_matriz = columnas * tamaño_casilla
    alto_total_matriz = filas * tamaño_casilla
    
    # Calcular posición inicial para centrar la matriz
    x_inicial = (ancho_ventana - ancho_total_matriz) // 2
    y_inicial = (alto_ventana - alto_total_matriz) // 2
    
    # Dibujar cada casilla
    for i in range(filas):
        for j in range(columnas):
            # Calcular posición de la casilla
            x = x_inicial + (j * tamaño_casilla)
            y = y_inicial + (i * tamaño_casilla)
            
            # Crear rectángulo de la casilla
            rect = pygame.Rect(x, y, tamaño_casilla, tamaño_casilla)
            
            # Dibujar fondo de la casilla
            if estado[i][j] or (mostrar_todas_bombas and numeros[i][j] == 'X'):
                pygame.draw.rect(superficie, COLOR_CASILLA_DESCUBIERTA, rect)
            else:
                pygame.draw.rect(superficie, COLOR_CASILLA_OCULTA, rect)
            
            # Dibujar borde
            pygame.draw.rect(superficie, COLOR_CASILLA_BORDE, rect, 1)
            
            # Dibujar contenido de la casilla
            if estado[i][j] or (mostrar_todas_bombas and numeros[i][j] == 'X'):
                valor = numeros[i][j]
                if valor == 'X':
                    if tamaño_casilla != tamaño_casilla_preferido:
                        imagen_escalada = pygame.transform.scale(imagen_bomba, (tamaño_casilla - 4, tamaño_casilla - 4))
                        superficie.blit(imagen_escalada, (x + 2, y + 2))
                    else:
                        superficie.blit(imagen_bomba, rect)
                elif valor > 0:
                    if tamaño_casilla != tamaño_casilla_preferido:
                        tamaño_fuente = tamaño_casilla // 2
                        fuente_escalada = pygame.font.Font(None, tamaño_fuente)
                        texto = fuente_escalada.render(str(valor), True, (0, 0, 0))
                    else:
                        texto = fuente.render(str(valor), True, (0, 0, 0))
                    superficie.blit(texto, texto.get_rect(center=rect.center))
            else:
                if banderas[i][j]:
                    if tamaño_casilla != tamaño_casilla_preferido:
                        imagen_escalada = pygame.transform.scale(imagen_bandera, (tamaño_casilla - 4, tamaño_casilla - 4))
                        superficie.blit(imagen_escalada, (x + 2, y + 2))
                    else:
                        superficie.blit(imagen_bandera, rect)

def descubrir_celda(matriz_estado, matriz_numeros, fila, columna):
   
    if matriz_estado[fila][columna] or matriz_numeros[fila][columna] == 'X':
        pass  # No hacer nada si ya esta descubierta o es bomba
    else:
        matriz_estado[fila][columna] = True

        if matriz_numeros[fila][columna] == 0:
            vecinos = [
                (fila - 1, columna - 1), (fila - 1, columna), (fila - 1, columna + 1),
                (fila, columna - 1),                            (fila, columna + 1),
                (fila + 1, columna - 1), (fila + 1, columna), (fila + 1, columna + 1)
            ]
            for ni, nj in vecinos:
                if ni < 0 or ni >= len(matriz_estado):
                    continue
                if nj < 0 or nj >= len(matriz_estado[0]):
                    continue
                descubrir_celda(matriz_estado, matriz_numeros, ni, nj)
    return


def verificar_victoria(matriz_estado, matriz_minas):
   
    victoria = True
    for i in range(len(matriz_estado)):
        for j in range(len(matriz_estado[0])):
            if not matriz_estado[i][j] and matriz_minas[i][j] != 'X':    
                victoria = False
    return victoria

def pedir_nombre(ventana, victoria):
    font = pygame.font.SysFont(None, 40)
    nombre = ""
    activo = True
    color = pygame.Color('dodgerblue2')


    while activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    activo = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 15 and event.unicode.isprintable():
                        nombre += event.unicode


        ancho = ventana.get_width()
        alto = ventana.get_height()

        ancho_input = 300
        alto_input = 40
        input_rect = pygame.Rect(
            (ancho - ancho_input) // 2,
            (alto - alto_input) // 2,
            ancho_input,
            alto_input
        )

        if victoria == True:
            fondo_color = (66, 245, 69)
            ventana.fill(fondo_color)

            mensaje = "GANASTE - Ingrese su nombre y presione Enter:"
            texto = font.render(mensaje, True, (0, 0, 0))
            texto_rect = texto.get_rect(center=(ancho // 2, input_rect.y - 25))
            ventana.blit(texto, texto_rect)

            pygame.draw.rect(ventana, color, input_rect, 2)
            texto_nombre = font.render(nombre, True, (0, 0, 0))
            ventana.blit(texto_nombre, (input_rect.x + 5, input_rect.y + 5))

            pygame.display.flip()
        else:
            fondo_color = (252, 0, 29)
            ventana.fill(fondo_color)

            mensaje = "PERDISTE - Ingrese su nombre y presione Enter:"
            texto = font.render(mensaje, True, (0, 0, 0))
            texto_rect = texto.get_rect(center=(ancho // 2, input_rect.y - 25))
            ventana.blit(texto, texto_rect)

            pygame.draw.rect(ventana, color, input_rect, 2)
            texto_nombre = font.render(nombre, True, (0, 0, 0))
            ventana.blit(texto_nombre, (input_rect.x + 5, input_rect.y + 5))

            pygame.display.flip()
            
    return nombre


def mover_bomba(matriz_minas, fila_bomba, col_bomba):
    
    filas = len(matriz_minas)
    columnas = len(matriz_minas[0])
    
    matriz_minas[fila_bomba][col_bomba] = ''
    
    while True:
        f = random.randint(0, filas - 1)
        c = random.randint(0, columnas - 1)
        if matriz_minas[f][c] != 'X' and (f != fila_bomba or c != col_bomba):  
            matriz_minas[f][c] = 'X'
            break
    
    matriz_numeros = generar_matriz_numeros(matriz_minas)
    
    return (matriz_minas, matriz_numeros)

# ------------------- PUNTAJES ------------------- #

def calcular_puntaje(nivel, tiempo):
    '''
    
    '''
    puntaje_base = 0

    if nivel == 0:
        if tiempo < 150:
            puntaje_base += 7
        else:
            if tiempo < 250:
                puntaje_base = 6
            else:
                if tiempo < 350:
                    puntaje_base += 4
                else:
                    puntaje_base += 2
    if nivel == 1:
        if tiempo < 150:
            puntaje_base += 8
        else:
            if tiempo < 250:
                puntaje_base = 7
            else:
                if tiempo < 350:
                    puntaje_base += 6
                else:
                    puntaje_base += 2
    if nivel == 2:
        if tiempo < 150:
            puntaje_base += 10
        else:
            if tiempo < 250:
                puntaje_base = 9
            else:
                if tiempo < 350:
                    puntaje_base += 8
                else:
                    puntaje_base += 4
    return puntaje_base


def guardar_puntaje(nombre, puntaje, tiempo):
    '''
    Recibe tres parametros, el nombre y el tiempo
    el cual seran guardados en el archivo csv
    '''
    puntajes = leer_puntajes()
    puntajes.append((nombre, puntaje, tiempo))
    puntajes.sort(key=lambda x: x[1], reverse=True)
    puntajes = puntajes[:10]
   
    with open(ARCHIVO_PUNTAJES, 'w') as archivo:
        archivo.write("Nombre,Puntaje,Tiempo\n")
        for nombre, puntaje, tiempo in puntajes:
            archivo.write(f"{nombre},{puntaje},{tiempo}\n")


def leer_puntajes():
    '''
    No recibe parametros, lee el archivo txt de los puntajes
    '''
    if not os.path.exists(ARCHIVO_PUNTAJES):
        return []
    with open(ARCHIVO_PUNTAJES, 'r') as archivo:
        lineas = archivo.readlines()
        puntajes = []
        for linea in lineas[1:]:  
            partes = linea.strip().split(',')
            if len(partes) == 3 and partes[1].isdigit() and partes[2].isdigit():
                nombre, puntaje, tiempo = partes
                puntajes.append((nombre, int(puntaje), int(tiempo)))
        return puntajes


def mostrar_lista_puntajes(ventana, fuente):
    
    puntajes = leer_puntajes()
    ancho_cuadro = 500
    alto_cuadro = max(300, 80 + 40 * len(puntajes)) 
    cuadro_x = (ANCHO_VENTANA - ancho_cuadro) // 2
    cuadro_y = (ALTO_VENTANA - alto_cuadro) // 2
    cuadro = pygame.Surface((ancho_cuadro, alto_cuadro))
    cuadro.fill((230, 230, 230)) 
    pygame.draw.rect(cuadro, (0, 0, 0), cuadro.get_rect(), 2)
    ventana.blit(cuadro, (cuadro_x, cuadro_y))
    
    fuente_titulo = pygame.font.SysFont("Verdana", 36, bold=True)
    titulo = "Top 10 Puntajes"
    texto_titulo = fuente_titulo.render(titulo, True, (0, 0, 0))
    x_titulo = cuadro_x + (ancho_cuadro - texto_titulo.get_width()) // 2
    ventana.blit(texto_titulo, (x_titulo, cuadro_y + 20))

    if not puntajes:
        mensaje = fuente.render("No hay puntajes", True, (100, 100, 100))
        x_msg = cuadro_x + (ancho_cuadro - mensaje.get_width()) // 2
        ventana.blit(mensaje, (x_msg, cuadro_y + 100))
        return

    colores_podio = [(255, 215, 0), (192, 192, 192), (205, 127, 50)] 
    y = cuadro_y + 80  
    posicion = 1  

    for nombre, puntaje, tiempo in puntajes:
        rect_puntaje = pygame.Rect(cuadro_x + 10, y, ancho_cuadro - 20, 35)
        pygame.draw.rect(ventana, (255, 255, 255), rect_puntaje) 
        pygame.draw.rect(ventana, (0, 0, 0), rect_puntaje, 1)  
        
      
        color_texto_linea = colores_podio[posicion - 1] if posicion <= 3 else (0, 0, 0)
        linea = f"{posicion}. {nombre[:12]} - Pts: {puntaje} - {tiempo}s"
        texto = fuente.render(linea, True, color_texto_linea)

        ventana.blit(texto, (cuadro_x + 20, y + 5)) 
        y += 40  
        posicion += 1 

        
# ------------------- MUSICA ------------------- #

def inicializar_musica():
    '''
    No recibe ningun parametro
    carga la musica, la reproduce en bucle infinito
    y le establace un volumen al 20%
    '''
    pygame.mixer.init()
    pygame.mixer.music.load('Musica/Musica.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

def cargar_sonidos():
    '''
    No recibe ningun parametro,
    carga la respectiva musica
    retorna los sonidos
    
    '''
    sonidos = {
        "click": pygame.mixer.Sound('Musica/click.mp3'),
        "victoria": pygame.mixer.Sound('Musica/victoria.mp3'),
        "derrota": pygame.mixer.Sound('Musica/derrota.mp3'),
    }
   
    for s in sonidos.values():
        s.set_volume(0.4)
    return sonidos

def reproducir_sonido(sonidos, tipo):
    '''
    Recibe dos parametros
    el sonido a reproducir y el tipo de sonido
    '''

    if tipo in sonidos:
        sonidos[tipo].play()

def cambiar_musica_de_fondo(archivo_mp3= 'Musica/Musica.mp3'):
    '''
    Recibe un parametro opcional, el mismo recibe la musica
    para,carga y reproduce la musica

    '''
    pygame.mixer.music.stop()
    pygame.mixer.music.load(archivo_mp3)
    pygame.mixer.music.play(-1)
