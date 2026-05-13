from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
import time

# Aquí diseñamos la interfaz usando el lenguaje KV (es como el HTML de Kivy)
KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 15
    canvas.before:
        Color:
            rgba: 0.05, 0.05, 0.06, 1  # Fondo oscuro
        Rectangle:
            pos: self.pos
            size: self.size

    # --- CALCULADORA DE TIEMPO ---
    Label:
        text: 'CALCULADORA DE TIEMPO'
        font_size: '20sp'
        bold: True
        size_hint_y: None
        height: 30
        color: 0.78, 0.95, 0.22, 1  # Acento verde lima

    GridLayout:
        cols: 3
        spacing: 10
        size_hint_y: None
        height: 50
        TextInput:
            id: h1
            hint_text: 'Horas'
            input_filter: 'int'
            halign: 'center'
        TextInput:
            id: m1
            hint_text: 'Min'
            input_filter: 'int'
            halign: 'center'
        TextInput:
            id: s1
            hint_text: 'Seg'
            input_filter: 'int'
            halign: 'center'

    Label:
        text: 'TIEMPO A RESTAR'
        size_hint_y: None
        height: 30

    GridLayout:
        cols: 3
        spacing: 10
        size_hint_y: None
        height: 50
        TextInput:
            id: h2
            hint_text: 'Horas'
            input_filter: 'int'
            halign: 'center'
        TextInput:
            id: m2
            hint_text: 'Min'
            input_filter: 'int'
            halign: 'center'
        TextInput:
            id: s2
            hint_text: 'Seg'
            input_filter: 'int'
            halign: 'center'

    Button:
        text: 'CALCULAR'
        size_hint_y: None
        height: 50
        background_color: 0.78, 0.95, 0.22, 1
        color: 0, 0, 0, 1
        bold: True
        on_press: app.calcular()

    Label:
        id: result_calc
        text: '00:00:00'
        font_size: '35sp'
        bold: True
        color: 0.78, 0.95, 0.22, 1
        size_hint_y: None
        height: 60

    Widget:  # Espaciador para separar secciones

    # --- CRONÓMETRO ---
    Label:
        text: 'CRONÓMETRO'
        font_size: '20sp'
        bold: True
        size_hint_y: None
        height: 30
        color: 0.36, 0.68, 1, 1  # Acento azul

    Label:
        id: result_crono
        text: '00:00:00.000'
        font_size: '45sp'
        bold: True
        color: 0.36, 0.68, 1, 1

    BoxLayout:
        size_hint_y: None
        height: 50
        spacing: 10
        Button:
            id: btn_start
            text: 'INICIAR'
            background_color: 0.36, 0.68, 1, 1
            bold: True
            on_press: app.toggle_crono()
        Button:
            text: 'RESET'
            background_color: 1, 0.37, 0.37, 1
            bold: True
            on_press: app.reset_crono()
'''

class TiempoApp(App):
    def build(self):
        # Variables para el cronómetro
        self.crono_corriendo = False
        self.start_time = 0
        self.elapsed = 0
        self.evento_reloj = None
        
        return Builder.load_string(KV)

    # Lógica independiente de la calculadora
    def calcular(self):
        try:
            h1 = int(self.root.ids.h1.text or 0)
            m1 = int(self.root.ids.m1.text or 0)
            s1 = int(self.root.ids.s1.text or 0)
            h2 = int(self.root.ids.h2.text or 0)
            m2 = int(self.root.ids.m2.text or 0)
            s2 = int(self.root.ids.s2.text or 0)

            total_segundos1 = (h1 * 3600) + (m1 * 60) + s1
            total_segundos2 = (h2 * 3600) + (m2 * 60) + s2

            diff = total_segundos1 - total_segundos2

            if diff < 0:
                diff = 86400 + (diff % 86400)

            res_h = (diff // 3600) % 24
            res_m = (diff % 3600) // 60
            res_s = diff % 60

            self.root.ids.result_calc.text = f"{res_h:02d}:{res_m:02d}:{res_s:02d}"
        except Exception:
            self.root.ids.result_calc.text = "Error"

    # Lógica independiente del cronómetro
    def actualizar_crono(self, dt):
        self.elapsed = time.time() - self.start_time
        ms = int(self.elapsed * 1000)
        h = ms // 3600000
        m = (ms % 3600000) // 60000
        s = (ms % 60000) // 1000
        mil = ms % 1000
        self.root.ids.result_crono.text = f"{h:02d}:{m:02d}:{s:02d}.{mil:03d}"

    def toggle_crono(self):
        if not self.crono_corriendo:
            self.start_time = time.time() - self.elapsed
            # Actualiza la pantalla 20 veces por segundo
            self.evento_reloj = Clock.schedule_interval(self.actualizar_crono, 0.05)
            self.root.ids.btn_start.text = 'PAUSAR'
            self.crono_corriendo = True
        else:
            if self.evento_reloj:
                self.evento_reloj.cancel()
            self.root.ids.btn_start.text = 'CONTINUAR'
            self.crono_corriendo = False

    def reset_crono(self):
        if self.evento_reloj:
            self.evento_reloj.cancel()
        self.crono_corriendo = False
        self.elapsed = 0
        self.root.ids.result_crono.text = '00:00:00.000'
        self.root.ids.btn_start.text = 'INICIAR'

if __name__ == '__main__':
    TiempoApp().run()