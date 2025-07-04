import pygame
from Funciones import *
from Constantes import *

############################ Inicializar Pygame ################################

pygame.init()
inicializar_musica()
sonidos = cargar_sonidos()

############################ Configurar ventana ################################

pygame.display.set_caption("Buscaminas")
ventana_juego = pygame.display.set_mode((DIMENSIONES_VENTANA), pygame.RESIZABLE)

############################ Imagenes y recursos ###############################

imagen_fondo = pygame.image.load('Imagenes/Fondo.jpg')
imagen_fondo_puntajes = pygame.image.load('Imagenes/Puntajes.jpg')
icono = pygame.image.load('Imagenes/bomb.png')
pygame.display.set_icon(icono)
imagen_bomba = pygame.image.load('Imagenes/bomb.png')
imagen_bomba = pygame.transform.scale(imagen_bomba, (40, 40))
imagen_bandera = pygame.image.load('Imagenes/bandera.png')
imagen_bandera = pygame.transform.scale(imagen_bandera, (40, 40))

############################## Fuentes ################################

fuente_titulo_grande = pygame.font.SysFont("Impact", 72)
fuente_texto_boton = pygame.font.SysFont("Verdana", 25)
fuente_subtitulo_pantalla = pygame.font.SysFont("Verdana", 48)

############################## Banderas ################################ 

dificultad_actual = 0
pantalla_actual = "menu"
indice_hover_actual = -2
puntaje = 0
juego_terminado = False
juego_ejecutandose = True
                                    
tiempo_inicio = 0
tiempo_transcurrido = 0
timer_activo = False
banderas_colocadas = 0

minas_totales = 0
mostrar_todas_bombas = False
primer_click = True

######################### Funciones auxiliares ##############################

def configurar_dificultad(dificultad: int) -> tuple:
    """
    Configura la dificultad del juego de Buscaminas.

    Recibe:
        dificultad (int): Un entero que representa el nivel de dificultad.
                        0 para facil, 1 para intermedio, 2 para dificil.

    Devuelve:
        tuple: Una tupla que contiene tres enteros:
            - filas (int): Numero de filas del tablero.
            - columnas (int): Numero de columnas del tablero.
            - minas (int): Numero de minas en el tablero.
            
    """
    filas = 0
    columnas = 0
    minas = 0

    if dificultad == 0:
        filas, columnas, minas = (8, 8, 10)       
    elif dificultad == 1:
        filas, columnas, minas = (16, 16, 50)  
    else:
        filas, columnas, minas = (24, 24, 120)  

    return (filas, columnas, minas)


def inicializar_tablero(dificultad_actual: int) -> dict:
    """
    Inicializa el tablero del juego de Buscaminas.

    Recibe:
        dificultad_actual (int): El nivel de dificultad actual del juego.

    Devuelve:
        dict: Un diccionario que contiene:
            - matriz_minas (list): Matriz que indica la ubicacion de las minas.
            - matriz_numeros (list): Matriz que indica los Numeros alrededor de las minas.
            - matriz_estado (list): Matriz que indica el estado de cada celda (descubierta o no).
            - matriz_banderas (list): Matriz que indica si hay una bandera en cada celda.
            - minas_totales (int): Numero total de minas en el tablero.
            - tiempo_inicio (int): Tiempo de inicio del juego.
            - timer_activo (bool): Indica si el temporizador esta activo.
            - filas (int): Numero de filas del tablero.
            - columnas (int): Numero de columnas del tablero.
    """
    filas, columnas, cantidad_minas = configurar_dificultad(dificultad_actual)
    
    matriz_minas = inicializar_matriz(filas, columnas, cantidad_minas)
    matriz_numeros = generar_matriz_numeros(matriz_minas)
    
    matriz_estado = []
    
    for _ in range(filas):
        fila = []
        for _ in range(columnas):
            fila.append(False)
        matriz_estado.append(fila)
    
    matriz_banderas = []
    
    for _ in range(filas):
        fila = []
        for _ in range(columnas):
            fila.append(False)
        matriz_banderas.append(fila)
    
    return {
        'matriz_minas': matriz_minas,
        'matriz_numeros': matriz_numeros,
        'matriz_estado': matriz_estado,
        'matriz_banderas': matriz_banderas,
        'minas_totales': cantidad_minas,
        'tiempo_inicio': 0,
        'timer_activo': False,
        'filas': filas,
        'columnas': columnas
    }


def mostrar_pantalla_menu_principal(indice: int, ventana) -> None:
    """
    Muestra la pantalla del menu principal del juego.

    Recibe:
        indice (int): El indice del boton actualmente seleccionado.
        ventana: La ventana donde se dibuja el menu.
    
    Devuelve:
        None
    """
    ventana.blit(imagen_fondo, (0, 0))
    dibujar_titulo_centrado("BUSCAMINAS", 100, "grande")
    texto_dificultad = NOMBRES_DIFICULTAD[dificultad_actual]

    botones = [
        (crear_boton('jugar', ventana), "Jugar"),
        (crear_boton('dificultad', ventana), texto_dificultad),
        (crear_boton('puntajes', ventana), "Puntajes"),
        (crear_boton('salir', ventana), "Salir"),
    ]

    for i in range(len(botones)):
        dibujar_boton_en_pantalla(botones[i][0], botones[i][1], indice == i)


def mostrar_pantalla_juego() -> None:
    """
    Muestra la pantalla del juego de Buscaminas.

    Devuelve:
        None
    """
    ventana_juego.fill(COLOR_FONDO)
    
    ancho_ventana = ventana_juego.get_width()
    alto_ventana = ventana_juego.get_height()
    
    dibujar_titulo_centrado(f"Nivel {NOMBRES_DIFICULTAD[dificultad_actual]}", 50, "mediana")
    
    if estado_juego['timer_activo']:
        estado_juego['tiempo_transcurrido'] = (pygame.time.get_ticks() - estado_juego['tiempo_inicio']) // 1000
        texto_tiempo = fuente_texto_boton.render(f"Tiempo: {estado_juego['tiempo_transcurrido']}s", True, COLOR_TEXTO_NORMAL)
        ventana_juego.blit(texto_tiempo, (int(ancho_ventana * 0.80), int(alto_ventana * 0.4)))
    
    texto_banderas = fuente_texto_boton.render(f"Banderas: {banderas_colocadas}", True, COLOR_TEXTO_NORMAL)
    ventana_juego.blit(texto_banderas, (int(ancho_ventana * 0.80), int(alto_ventana * 0.45)))
    
    minas_restantes = estado_juego['minas_totales'] - banderas_colocadas
    texto_minas = fuente_texto_boton.render(f"Minas: {minas_restantes}", True, COLOR_TEXTO_NORMAL)
    ventana_juego.blit(texto_minas, (int(ancho_ventana * 0.80), int(alto_ventana * 0.5)))
    
    dibujar_matriz_buscaminas(ventana_juego, estado_juego['matriz_numeros'], estado_juego['matriz_estado'], 
                               estado_juego['matriz_banderas'], fuente_texto_boton, imagen_bomba, imagen_bandera, 
                               mostrar_todas_bombas)
    
    dibujar_boton_en_pantalla(crear_boton('reiniciar', ventana_juego), "Reiniciar", indice_hover_actual == 1)
    dibujar_boton_en_pantalla(crear_boton('volver', ventana_juego), "Volver", indice_hover_actual == 0)


def mostrar_pantalla_puntajes() -> None:
    """
    Muestra la pantalla de puntajes del juego.

    Devuelve:
        None
    """
    ventana_juego.blit(imagen_fondo_puntajes, (0, 0))
    mostrar_lista_puntajes(ventana=ventana_juego, fuente=fuente_texto_boton)
    dibujar_boton_en_pantalla(crear_boton('volver', ventana_juego), "Volver", indice_hover_actual == 0)


########################### Loop principal ##############################

while juego_ejecutandose:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego_ejecutandose = False

        elif evento.type == pygame.MOUSEMOTION:
            if pantalla_actual == "menu":
                indice_hover_actual = detectar_hover_en_menu_nuevo(evento.pos, ventana_juego)
            else:
                indice_hover_actual = detectar_hover_en_otras_pantallas(evento.pos, ventana_juego)

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: 
                reproducir_sonido(sonidos, "click")

                if pantalla_actual == "menu":
                    i = procesar_click_en_menu_nuevo(evento.pos, ventana_juego)

                    if i == 0:  
                        estado_juego = inicializar_tablero(dificultad_actual)
                        banderas_colocadas = 0
                        mostrar_todas_bombas = False
                        pantalla_actual = "juego"
                        juego_terminado = False

                    elif i == 1:  
                        dificultad_actual = (dificultad_actual + 1) % 3
                    elif i == 2:  
                        pantalla_actual = "puntajes"
                    elif i == 3:  
                        juego_ejecutandose = False

                elif pantalla_actual == "juego":
                    click_reiniciar, click_volver = procesar_click_en_otras_pantallas(evento.pos, ventana_juego)

                    if click_volver:
                        pantalla_actual = "menu"

                    elif click_reiniciar:
                        estado_juego = inicializar_tablero(dificultad_actual)
                        banderas_colocadas = 0
                        mostrar_todas_bombas = False
                        juego_terminado = False
                        primer_click = True
                        estado_juego['tiempo_inicio'] = 0
                        estado_juego['timer_activo'] = False
                    else:
                        fila, col = calcular_posicion_matriz(evento.pos, ventana_juego, estado_juego['filas'], estado_juego['columnas'])                        
                       
                        if fila < 0 or fila >= len(estado_juego['matriz_minas']):
                            continue                     
                        if col < 0 or col >= len(estado_juego['matriz_minas'][0]):
                            continue 
                       
                        if not estado_juego['matriz_estado'][fila][col] and not estado_juego['matriz_banderas'][fila][col]:
                            
                            if primer_click:
                                primer_click = False
                                
                                if estado_juego['matriz_numeros'][fila][col] == 'X':
                                    estado_juego['matriz_minas'], estado_juego['matriz_numeros'] = mover_bomba(estado_juego['matriz_minas'], fila, col)
                                   
                                    for i in range(len(estado_juego['matriz_estado'])):
                                        for j in range(len(estado_juego['matriz_estado'][0])):
                                            estado_juego['matriz_estado'][i][j] = False
                                   
                                    for i in range(len(estado_juego['matriz_banderas'])):
                                        for j in range(len(estado_juego['matriz_banderas'][0])):
                                            estado_juego['matriz_banderas'][i][j] = False
                            
                            if not estado_juego['timer_activo']:
                                
                                if estado_juego['matriz_numeros'][fila][col] != 'X':
                                    estado_juego['tiempo_inicio'] = pygame.time.get_ticks()
                                    estado_juego['timer_activo'] = True

                            descubrir_celda(estado_juego['matriz_estado'], estado_juego['matriz_numeros'], fila, col)
                            
                            if estado_juego['matriz_numeros'][fila][col] == 'X':  
                                reproducir_sonido(sonidos, "derrota")
                                mostrar_todas_bombas = True
                                juego_terminado = True
                                estado_juego['timer_activo'] = False
                                mostrar_pantalla_juego()
                                pygame.display.flip()
                                pygame.time.wait(1500)
                                tiempo_transcurrido = (pygame.time.get_ticks() - estado_juego['tiempo_inicio']) // 1000
                                nombre = pedir_nombre(ventana_juego, False)
                                
                                if nombre:
                                    puntaje = calcular_puntaje(dificultad_actual, tiempo_transcurrido)
                                    guardar_puntaje(nombre, puntaje, tiempo_transcurrido)
                                pantalla_actual = "menu"
                           
                            elif verificar_victoria(estado_juego['matriz_estado'], estado_juego['matriz_minas']):
                                reproducir_sonido(sonidos, "victoria")
                                juego_terminado = True
                                estado_juego['timer_activo'] = False
                                nombre = pedir_nombre(ventana_juego, True)

                elif pantalla_actual == "puntajes":
                    if procesar_click_en_otras_pantallas(evento.pos, ventana_juego):
                        pantalla_actual = "menu"

            elif evento.button == 3 and pantalla_actual == "juego":  
                fila, col = calcular_posicion_matriz(evento.pos,ventana_juego,estado_juego['filas'],estado_juego['columnas'])
   
                if fila < 0 or fila >= len(estado_juego['matriz_banderas']):
                    continue  

                if col < 0 or col >= len(estado_juego['matriz_banderas'][0]):
                    continue  

                if estado_juego['matriz_estado'][fila][col]:
                    continue 
            
                estado_juego['matriz_banderas'][fila][col] = not estado_juego['matriz_banderas'][fila][col]
                
                if estado_juego['matriz_banderas'][fila][col]:
                    banderas_colocadas += 1
                else:
                    banderas_colocadas -= 1

                reproducir_sonido(sonidos, "bandera")


    if juego_terminado and pantalla_actual == "juego":
        tiempo_transcurrido = (pygame.time.get_ticks() - estado_juego['tiempo_inicio']) // 1000
        nombre = pedir_nombre(ventana_juego, False)
       
        if nombre:
            puntaje = calcular_puntaje(dificultad_actual, tiempo_transcurrido)
            guardar_puntaje(nombre, puntaje, tiempo_transcurrido)
        cambiar_musica_de_fondo('Musica/Musica.mp3')
        mostrar_todas_bombas = False
        juego_terminado = False
        estado_juego['timer_activo'] = False
        pantalla_actual = "menu"


    if pantalla_actual == "menu":
        mostrar_pantalla_menu_principal(indice_hover_actual, ventana_juego)
    elif pantalla_actual == "puntajes":
        mostrar_pantalla_puntajes()
    elif pantalla_actual == "juego":
        mostrar_pantalla_juego()

    pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()
