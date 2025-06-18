import pygame
from Constantes import *
from Variables import *

# ============================================================================
# FUNCIONES PARA CREACION DE BOTONES 
# ============================================================================

def calcular_posicion_centrada_x(ancho_elemento) -> int:
    """Calcula la posicion centrada en el eje X para un elemento dado.
    
    
    
    """
    posicion_x = (ANCHO_VENTANA - ancho_elemento) // 2
   
    return posicion_x

def crear_boton_jugar(posicion_y_boton_jugar=int(220)) -> pygame.Rect:
    """Crea un boton 'Jugar' para iniciar el juego con la dificultad seleccionada.
    
    
    
    """
    posicion_x_centrada = calcular_posicion_centrada_x(ANCHO_BOTON_MENU)
    boton = pygame.Rect(posicion_x_centrada, posicion_y_boton_jugar, ANCHO_BOTON_MENU, ALTO_BOTON_MENU)
   
    return boton

def crear_boton_dificultad(posicion_y_boton_dificultad=int(300)) -> pygame.Rect:
    """Crea un boton 'Dificultad' para cambiar entre los niveles de dificultad.
    
    
    """
    posicion_x_centrada = calcular_posicion_centrada_x(ANCHO_BOTON_MENU)
    boton = pygame.Rect(posicion_x_centrada, posicion_y_boton_dificultad, ANCHO_BOTON_MENU, ALTO_BOTON_MENU)
   
    return boton

def crear_boton_puntajes(posicion_y_boton_puntajes=380) -> pygame.Rect:
    """Crea un boton 'Puntajes' para mostrar la pantalla de puntajes.
    
    
    
    """
    posicion_x_centrada = calcular_posicion_centrada_x(ANCHO_BOTON_MENU)
    boton = pygame.Rect(posicion_x_centrada, posicion_y_boton_puntajes, ANCHO_BOTON_MENU, ALTO_BOTON_MENU)
   
    return boton

def crear_boton_salir_nuevo(posicion_y_boton_salir=500) -> pygame.Rect:
    """Crea un boton 'Salir' para cerrar el juego.
    
    
    
    """
    posicion_x_centrada = calcular_posicion_centrada_x(ANCHO_BOTON_MENU)
    boton = pygame.Rect(posicion_x_centrada, posicion_y_boton_salir, ANCHO_BOTON_MENU, ALTO_BOTON_MENU)
  
    return boton

def crear_boton_volver_menu() -> pygame.Rect:
    """Crea un boton 'Volver' para regresar al menú principal.
    
    
    
    """
    posicion_x_esquina = 50
    posicion_y_esquina = 50
    boton = pygame.Rect(posicion_x_esquina, posicion_y_esquina, ANCHO_BOTON_VOLVER, ALTO_BOTON_VOLVER)
  
    return boton

# ============================================================================
# FUNCIONES DE PROCESAMIENTO DE EVENTOS 
# ============================================================================

def procesar_click_en_menu_nuevo(posicion_mouse=any) -> int:
    """Detecta en que boton del nuevo menu se ha hecho clic.
    
    
    
    
    """
    botones = [
        crear_boton_jugar(),
        crear_boton_dificultad(),
        crear_boton_puntajes(),
        crear_boton_salir_nuevo()
    ]
    indice = -1
    for i, boton in enumerate(botones):
        if boton.collidepoint(posicion_mouse):
            indice = i
            break
   
    return indice

def detectar_hover_en_menu_nuevo(posicion_mouse=any) -> int:
    """Detecta en que boton del nuevo menu se encuentra el mouse.
    
    
    
    """
    botones = [
        crear_boton_jugar(),
        crear_boton_dificultad(),
        crear_boton_puntajes(),
        crear_boton_salir_nuevo()
    ]
    indice = -1
    for i, boton in enumerate(botones):
        if boton.collidepoint(posicion_mouse):
            indice = i
            break
 
    return indice

def procesar_click_en_otras_pantallas(posicion_mouse=any) -> bool:
    """Detecta si se ha hecho clic en el boton 'Volver' en otras pantallas.
    
    
    """
    boton_volver = crear_boton_volver_menu()
    accion = False
    if boton_volver.collidepoint(posicion_mouse):
        accion = True
  
    return accion

def detectar_hover_en_otras_pantallas(posicion_mouse=any) -> int:
    """Detecta si el mouse esta sobre el boton 'Volver' en otras pantallas.
    
    
    
    """
    boton_volver = crear_boton_volver_menu()
    indice = -1
    if boton_volver.collidepoint(posicion_mouse):
        indice = 0
 
    return indice
