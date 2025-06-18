import pygame
from Funciones import *
from Constantes import *
from Variables import *

# ============================================================================
# INICIALIZACION DE PYGAME Y RECURSOS
# ============================================================================

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Musica/Musica.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

pygame.display.set_caption("Buscaminas")
ventana_juego = pygame.display.set_mode(DIMENSIONES_VENTANA)

imagen_fondo = pygame.image.load('Imagenes/Fondo.jpg')
imagen_fondo_puntajes = pygame.image.load('Imagenes/Puntajes.jpg')
icono = pygame.image.load('Imagenes/Icono.jpg')
pygame.display.set_icon(icono)

# ============================================================================
# CONFIGURACION DE FUENTES
# ============================================================================

fuente_titulo_grande = pygame.font.SysFont("Impact", 72)
fuente_texto_boton = pygame.font.SysFont("Verdana", 25)
fuente_subtitulo_pantalla = pygame.font.SysFont("Arial", 48, bold=True)

# ============================================================================
# FUNCIONES DE PANTALLAS
# ============================================================================

def dibujar_boton_en_pantalla(rectangulo_boton, texto_boton, mouse_esta_encima):
    """
    """
    if mouse_esta_encima:
        color_boton_actual = COLOR_BOTON_ENCIMA 
    else:
        color_boton_actual = COLOR_BOTON_NORMAL
    pygame.draw.rect(ventana_juego, color_boton_actual, rectangulo_boton)
    pygame.draw.rect(ventana_juego, COLOR_TEXTO_NORMAL, rectangulo_boton, 2)
    superficie_texto = fuente_texto_boton.render(texto_boton, True, COLOR_TEXTO_NORMAL)
    rectangulo_texto = superficie_texto.get_rect(center=rectangulo_boton.center)
    ventana_juego.blit(superficie_texto, rectangulo_texto)


def dibujar_titulo_centrado(texto_titulo, posicion_y, tipo_fuente):
    """
    """
    if tipo_fuente == "grande":
        fuente_seleccionada = fuente_titulo_grande
    elif tipo_fuente == "mediana":
        fuente_seleccionada = fuente_subtitulo_pantalla
    else:
        fuente_seleccionada = fuente_texto_boton
    superficie_titulo = fuente_seleccionada.render(texto_titulo, True, COLOR_TITULO_PRINCIPAL)
    rectangulo_titulo = superficie_titulo.get_rect(center=(ANCHO_VENTANA // 2, posicion_y))
    ventana_juego.blit(superficie_titulo, rectangulo_titulo)


def mostrar_pantalla_menu_principal(indice_boton_hover):
    """
    """
    ventana_juego.blit(imagen_fondo, (0, 0)) 
    dibujar_titulo_centrado("BUSCAMINAS", 100, "grande")
    
    texto_dificultad = f"{nombres_dificultad[dificultad_actual]}"
    
    botones = [
        (crear_boton_jugar(), "Jugar"),
        (crear_boton_dificultad(), texto_dificultad),
        (crear_boton_puntajes(), "Puntajes"),
        (crear_boton_salir_nuevo(), "Salir")
    ]
    
    indice = 0
    
    for boton, texto in botones:
        dibujar_boton_en_pantalla(boton, texto, indice_boton_hover == indice)
        indice += 1


def mostrar_pantalla_juego(nombre_dificultad, indice_boton_hover):
    """
    """
    ventana_juego.fill(COLOR_FONDO)
    
    titulo_pantalla = f"Nivel {nombre_dificultad.capitalize()}"
    
    dibujar_titulo_centrado(titulo_pantalla, 200, "mediana")
    
    mensaje_temporal = "Aca va el juego"
    superficie_mensaje = fuente_texto_boton.render(mensaje_temporal, True, COLOR_TEXTO_NORMAL)
    rectangulo_mensaje = superficie_mensaje.get_rect(center=(ANCHO_VENTANA // 2, 300))
    
    ventana_juego.blit(superficie_mensaje, rectangulo_mensaje)
    
    boton_volver = crear_boton_volver_menu()
    dibujar_boton_en_pantalla(boton_volver, "Volver", indice_boton_hover == 0)


def mostrar_pantalla_puntajes(indice_boton_hover):
    """
    """
    ventana_juego.blit(imagen_fondo_puntajes, (0, 0))
    
    dibujar_titulo_centrado("Puntajes", 200, "mediana")
    
    mensaje_puntajes = "Aca van los puntajes"
    superficie_mensaje = fuente_texto_boton.render(mensaje_puntajes, True, COLOR_TEXTO_NORMAL)
    rectangulo_mensaje = superficie_mensaje.get_rect(center=(ANCHO_VENTANA // 2, 300))
    
    ventana_juego.blit(superficie_mensaje, rectangulo_mensaje)
    
    boton_volver = crear_boton_volver_menu()
    dibujar_boton_en_pantalla(boton_volver, "Volver", indice_boton_hover == 0)

# ============================================================================
# LOOP PRINCIPAL DEL JUEGO
# ============================================================================

while juego_ejecutandose:
    for evento_actual in pygame.event.get():
        if evento_actual.type == pygame.QUIT:
            juego_ejecutandose = False
        elif evento_actual.type == pygame.MOUSEMOTION:
            posicion_mouse_actual = evento_actual.pos
            if pantalla_actual == "menu":
                indice_hover_actual = detectar_hover_en_menu_nuevo(posicion_mouse_actual)
            else:
                indice_hover_actual = detectar_hover_en_otras_pantallas(posicion_mouse_actual)
        elif evento_actual.type == pygame.MOUSEBUTTONDOWN:
            if evento_actual.button == 1:
                posicion_click = evento_actual.pos
                if pantalla_actual == "menu":
                    indice_boton_clickeado = procesar_click_en_menu_nuevo(posicion_click)
                    if indice_boton_clickeado == 0:  # Jugar
                        pantalla_actual = ["facil", "medio", "dificil"][dificultad_actual]
                        indice_hover_actual = -1
                    elif indice_boton_clickeado == 1:  # Dificultad
                        dificultad_actual = (dificultad_actual + 1) % 3
                    elif indice_boton_clickeado == 2:  # Puntajes
                        pantalla_actual = "puntajes"
                        indice_hover_actual = -1
                    elif indice_boton_clickeado == 3:  # Salir
                        juego_ejecutandose = False
                else:
                    if procesar_click_en_otras_pantallas(posicion_click):
                        pantalla_actual = "menu"
                        indice_hover_actual = -1

    if pantalla_actual == "menu":
        mostrar_pantalla_menu_principal(indice_hover_actual)
    elif pantalla_actual == "puntajes":
        mostrar_pantalla_puntajes(indice_hover_actual)
    else:
        mostrar_pantalla_juego(pantalla_actual, indice_hover_actual)

    pygame.display.flip()

# ============================================================================
# CIERRE DEL JUEGO
# ============================================================================

pygame.mixer.music.stop()
pygame.quit()

