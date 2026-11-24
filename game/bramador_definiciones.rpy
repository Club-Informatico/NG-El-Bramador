## ============================================================================
##  EL BRAMADOR · Una leyenda de Copiapó
##  Definiciones: personajes, imágenes, transformaciones, sonido y estilo.
## ============================================================================

init offset = 1


## ----------------------------------------------------------------------------
##  Personajes
## ----------------------------------------------------------------------------

define m = Character("Matías", color="#e2b46a")
define ro = Character("Rosario", color="#e7a0a8")
define c = Character("Celestino", color="#c9b48a")
define f = Character("Don Fermín", color="#b8c4d6")
define tr = Character("Doña Tránsito", color="#b9cf9d")
define u = Character("Ulises", color="#d9c27a")
define cab = Character("[nombre_caballero]", color="#d4a24a", what_color="#f3e6c8")

default nombre_caballero = "El forastero"

## La voz de la leyenda (prólogo) y los documentos se leen en modo NVL.
define leyenda = Character(None, kind=nvl, what_color="#efe2c4")
define papel = Character(None, kind=nvl, what_italic=True, what_color="#f2e6cf")


## ----------------------------------------------------------------------------
##  Variables de la historia
## ----------------------------------------------------------------------------

default escucho_ulises = False   # escuchó al Loco Ulises en la chingana
default contrato = False         # leyó el contrato y pidió copia
default conto_rosario = False    # le contó la verdad a Rosario
default consejo = False          # visitó a doña Tránsito
default dijo_nombre = False      # le dio su nombre completo al Caballero
default bebio = False            # aceptó el trago del Caballero

## Datos del final que se está mostrando.
default fin_num = 0
default fin_nombre = ""
default vistos = 0

## Finales vistos (se guardan entre partidas).
default persistent.finales = set()


## ----------------------------------------------------------------------------
##  Imágenes
## ----------------------------------------------------------------------------

image negro = Solid("#000000")

## Fondos
image bg cerro_noche = "images/bg/cerro_noche.webp"
image bg cerro_tarde = "images/bg/cerro_tarde.webp"
image bg chingana = "images/bg/chingana.webp"
image bg oficina = "images/bg/oficina.webp"
image bg rancho = "images/bg/rancho.webp"
image bg transito = "images/bg/transito.webp"
image bg campamento = "images/bg/campamento.webp"
image bg ladera = "images/bg/ladera.webp"
image bg puerta = "images/bg/puerta.webp"
image bg caverna = "images/bg/caverna.webp"
image bg calle_noche = "images/bg/calle_noche.webp"
image bg calle_alba = "images/bg/calle_alba.webp"
image bg mansion = "images/bg/mansion.webp"
image bg desierto_alba = "images/bg/desierto_alba.webp"

## Escenas especiales (CG)
image cg titulo = "images/cg/titulo.webp"
image cg derrotero = "images/cg/derrotero.webp"
image cg contrato = "images/cg/contrato.webp"
image cg avalancha = "images/cg/avalancha.webp"
image cg caballero = "images/cg/caballero.webp"

## Personajes
image rosario neutral = "images/sprites/rosario_neutral.png"
image rosario triste = "images/sprites/rosario_triste.png"
image rosario sonrisa = "images/sprites/rosario_sonrisa.png"
image celestino neutral = "images/sprites/celestino_neutral.png"
image celestino risa = "images/sprites/celestino_risa.png"
image celestino miedo = "images/sprites/celestino_miedo.png"
image fermin neutral = "images/sprites/fermin_neutral.png"
image fermin sonrisa = "images/sprites/fermin_sonrisa.png"
image transito neutral = "images/sprites/transito_neutral.png"
image ulises neutral = "images/sprites/ulises_neutral.png"
image ulises lucido = "images/sprites/ulises_lucido.png"
image caballero neutral = "images/sprites/caballero_neutral.png"
image caballero sonrisa = "images/sprites/caballero_sonrisa.png"
image caballero revelado = "images/sprites/caballero_revelado.png"


## ----------------------------------------------------------------------------
##  Transformaciones y transiciones
## ----------------------------------------------------------------------------

## El Caballero aparece despacio, como si se formara del humo de la fogata.
transform aparece(x=0.5):
    xalign x
    yalign 1.0
    alpha 0.0
    linear 2.0 alpha 1.0

## El bramido hace temblar la pantalla (suave y largo).
transform temblor_cerro:
    xalign 0.5
    yalign 0.5
    block:
        linear 0.06 xoffset 3 yoffset -2
        linear 0.06 xoffset -3 yoffset 2
        linear 0.06 xoffset 2 yoffset 1
        linear 0.06 xoffset -2 yoffset -1
        repeat 25
    linear 0.2 xoffset 0 yoffset 0

define fundido_lento = Dissolve(2.0)
define fundido_muy_lento = Dissolve(3.5)
define relampago = Fade(0.05, 0.0, 0.8, color="#f6e3b0")
define sangre_oro = Fade(0.4, 0.3, 1.2, color="#2a1604")


## ----------------------------------------------------------------------------
##  Sonido
## ----------------------------------------------------------------------------

init python:
    renpy.music.register_channel("ambiente", mixer="sfx", loop=True)
    renpy.music.register_channel("cerro", mixer="sfx", loop=False)

## Música (original)
define audio.tema = "audio/tema_bramador.ogg"
define audio.cueca = "audio/chingana.ogg"
define audio.caballero_tema = "audio/caballero.ogg"
define audio.tension = "audio/tension_cerro.ogg"
define audio.oscuro = "audio/final_oscuro.ogg"
define audio.luz = "audio/final_luz.ogg"

## El coro de las almas (adentro del cerro). Sin graves.
define audio.coro = "audio/bramido_coro.ogg"

## El bramido (recreado a partir del análisis de una grabación real del cerro).
## Cada bramido tiene dos versiones: completa y suave. La suave quita la nota
## más grave (~70 Hz); el oído sigue reconociendo el mismo tono por sus
## armónicos, pero con mucha menos vibración. Se elige al empezar la partida
## y se cambia en cualquier momento con la tecla B.
default persistent.bramido_suave = False

init python:
    def cerro_snd(nombre):
        if persistent.bramido_suave:
            return "audio/" + nombre + "_suave.ogg"
        return "audio/" + nombre + ".ogg"

    def alternar_bramido():
        persistent.bramido_suave = not persistent.bramido_suave
        if persistent.bramido_suave:
            renpy.notify("Bramido suave")
        else:
            renpy.notify("Bramido completo")

    config.keymap["alternar_bramido"] = ["b", "B"]
    config.underlay.append(renpy.Keymap(alternar_bramido=Function(alternar_bramido)))

## Efectos
define audio.viento = "audio/viento_desierto.ogg"
define audio.fogata = "audio/fogata.ogg"
define audio.arena = "audio/arena.ogg"
define audio.cascos = "audio/cascos.ogg"
define audio.piedra = "audio/piedra.ogg"
define audio.oro = "audio/oro.ogg"
define audio.golpes = "audio/golpes.ogg"
define audio.campana = "audio/campana.ogg"


## ----------------------------------------------------------------------------
##  Estilo de texto
## ----------------------------------------------------------------------------

init python:
    config.font_replacement_map["fonts/DejaVuSerif.ttf", False, True] = ("fonts/DejaVuSerif-Italic.ttf", False, False)
    config.font_replacement_map["fonts/DejaVuSerif.ttf", True, False] = ("fonts/DejaVuSerif-Bold.ttf", False, False)

style say_dialogue:
    font "fonts/DejaVuSerif.ttf"

style say_label:
    font "fonts/DejaVuSerif-Bold.ttf"

style nvl_dialogue:
    font "fonts/DejaVuSerif.ttf"

style centered_text:
    font "fonts/DejaVuSerif.ttf"
    color "#efe2c4"


## ----------------------------------------------------------------------------
##  Fondos del menú principal y de los menús internos
## ----------------------------------------------------------------------------
## gui.rpy ya define estas dos variables apuntando a gui/main_menu.png y
## gui/game_menu.png. Ren'Py vuelve a ejecutar los "define gui..." cada vez
## que aplica el idioma del proyecto, por eso se redefinen aquí con define:
## este archivo se carga después de gui.rpy y su valor es el que queda.
## (El Lint avisará que la variable "ya está definida en gui.rpy": es esperado.)

define gui.main_menu_background = "images/menu/menu_principal.png"
define gui.game_menu_background = "images/menu/menu_juego.png"
