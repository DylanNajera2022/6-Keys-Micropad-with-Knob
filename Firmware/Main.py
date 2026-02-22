import board
import busio
import adafruit_ssd1306
import gc

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.modules.macros import Macros
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.modules import Module # Importante para crear el módulo de pantalla

# Limpieza de memoria inicial
gc.collect()

# ================= 1. CONFIGURACIÓN OLED =================
oled = None
try:
    i2c = busio.I2C(board.D5, board.D4)
    oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
    oled.rotation = 2
    
    # Función auxiliar para dibujar
    def dibujar(titulo, texto):
        if oled:
            try:
                oled.fill(0)
                oled.text(titulo, 35, 2, 1)
                oled.hline(0, 12, 128, 1)
                # Centrar texto
                x = 64 - (len(texto) * 3)
                oled.text(texto, x, 20, 1)
                oled.show()
            except:
                pass
    
    dibujar("MACROPAD", "Listo")

except Exception as e:
    print("Error OLED:", e)
    oled = None
    def dibujar(t, x): pass

# ================= 2. MÓDULO DE PANTALLA (LA SOLUCIÓN) =================
class OledModule(Module):
    def __init__(self):
        self.nombres = {
            0: "CTRL+Z",
            1: "CTRL+Y",
            2: "CTRL+C",
            3: "CTRL+V",
            4: "CTRL+S",
            5: "ALT+TAB"
        }

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    # Esta función intercepta la tecla justo cuando se presiona
    def process_key(self, keyboard, key, is_pressed, int_coord):
        if is_pressed:
            # int_coord es el número de pin (0 a 5)
            nombre = self.nombres.get(int_coord, "TECLA")
            dibujar("EJECUTANDO", nombre)
        
        # IMPORTANTE: Devolvemos la tecla para que KMK la mande a la PC
        return key

# ================= 3. CONFIGURACIÓN TECLADO =================
keyboard = KMKKeyboard()

# Añadimos los módulos
macros = Macros()
encoder_handler = EncoderHandler()
oled_module = OledModule() # Nuestro módulo de pantalla

# El orden importa: OledModule debe ir aquí
keyboard.modules = [macros, encoder_handler, oled_module]
keyboard.extensions.append(MediaKeys())

# ================= 4. HARDWARE =================
keyboard.matrix = KeysScanner(
    pins=[board.A3, board.TX, board.A2, board.RX, board.A0, board.A1],
    value_when_pressed=False,
    pull=True,
)

keyboard.keymap = [[
    KC.LCTL(KC.Z), KC.LCTL(KC.Y), KC.LCTL(KC.C),
    KC.LCTL(KC.V), KC.LCTL(KC.S), KC.LALT(KC.TAB)
]]

encoder_handler.pins = ((board.MISO, board.MOSI, board.SCK, False),)
encoder_handler.map = [[(KC.VOLU, KC.VOLD, KC.MPLY)]]

if __name__ == "__main__":
    gc.collect()
    keyboard.go()
