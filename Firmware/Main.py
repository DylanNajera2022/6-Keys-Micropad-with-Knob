# You import all the IOs of your board
import board
from kmk.modules.encoder import Encoder

# These are imports from the kmk library
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros

# This is the main instance of your keyboard
keyboard = KMKKeyboard()

# Add the macro extension
macros = Macros()
keyboard.modules.append(macros)

# Define your pins here!
PINS = [
    board.GP29, # Switch 1
    board.GP0,  # Switch 2
    board.GP28, # Switch 3
    board.GP1,  # Switch 4
    board.GP26, # Switch 5
    board.GP27, # Switch 6
    board.GP02  # Switch 7 (Perilla)
]

encoder_handler = Encoder(
    pin_a=board.GP04,  # Pin A para la rotación 
    pin_b=board.GP03,  # Pin B para la rotación 
    divisor=2,       # Ajusta la sensibilidad: 1=más sensible, 4=menos
)
keyboard.modules.append(encoder_handler)

# Tell kmk we are not using a key matrix
keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# Here you define the buttons corresponding to the pins
# Look here for keycodes: https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/keycodes.md
# And here for macros: https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/macros.md
keyboard.keymap = [
    [
        KC.UNDO,               # Botón 1: Deshacer (GP29)
        KC.REDO,               # Botón 2: Rehacer (GP0)
        KC.LCTL(KC.C),         # Botón 3: Copiar (GP28)
        KC.LCTL(KC.V),         # Botón 4: Pegar (GP1)
        KC.LCTL(KC.S),         # Botón 5: Guardado Rápido (GP26)
        KC.LALT(KC.TAB),       # Botón 6: Cambiar de Pantalla (GP27)
        KC.TRNS,               # Botón 7: Transparente (GP02). La función la maneja encoder_handler.map_config
    ]
]

encoder_handler.map_config = [
    (
        encoder_handler.pins.pin_a, # Esto identifica al primer (y único) encoder
        KC.VOLU,                    # Giro a la Derecha = Subir Volumen
        KC.VOLD,                    # Giro a la Izquierda = Bajar Volumen
        KC.MPLY,                    # Botón del Encoder = Play/Pause
    )
]

# Start kmk!
if __name__ == '__main__':
    keyboard.go()