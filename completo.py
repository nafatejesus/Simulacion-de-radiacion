import tkinter as tk
from tkinter import ttk
import math
import random
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =====================================================================
# PARTE 1: CÓDIGO BASE DE TU COMPAÑERO (Módulo Luz Incidente)
# =====================================================================
class ModuloLuzIncidente:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación: Interacción Radiación Electromagnética con la Materia")
        self.root.geometry("1200x650")
        self.root.configure(bg="#1e1e1e")
        
        self.laser_encendido = False
        self.wavelength = 520.0
        self.intensidad = 50.0
        self.fase_onda = 0.0
        
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")
        self.estilo.configure(".", background="#1e1e1e", foreground="white")
        self.estilo.configure("TLabel", background="#1e1e1e", foreground="white", font=("Arial", 10))
        
        self.crear_titulo()
        self.crear_paneles_completos()
        self.crear_controles_linterna()
        self.bucle_animacion()

    def crear_titulo(self):
        titulo = tk.Label(
            self.root, 
            text="SIMULACIÓN DE LA INTERACCIÓN DE LA RADIACIÓN ELECTROMAGNÉTICA CON LA MATERIA",
            font=("Arial", 14, "bold"), bg="#1e1e1e", fg="#00ffcc", pady=10
        )
        titulo.pack(side=tk.TOP, fill=tk.X)

    def crear_paneles_completos(self):
        contenedor = tk.Frame(self.root, bg="#1e1e1e")
        contenedor.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        f_izq = tk.LabelFrame(contenedor, text=" Propagación y Frontera del Material ", bg="#1e1e1e", fg="white", font=("Arial", 9, "bold"))
        f_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_izq = tk.Canvas(f_izq, bg="black", highlightthickness=0)
        self.canvas_izq.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        f_cen = tk.LabelFrame(contenedor, text=" Átomo (Niveles de Energía) ", bg="#1e1e1e", fg="white", font=("Arial", 9, "bold"))
        f_cen.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_cen = tk.Canvas(f_cen, bg="#0a0a0a", highlightthickness=0)
        self.canvas_cen.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def crear_controles_linterna(self):
        f_controles = tk.LabelFrame(self.root, text=" Panel de Controles ", bg="#252526", fg="#00ffcc", font=("Arial", 10, "bold"))
        f_controles.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)
        
        f_col1 = tk.Frame(f_controles, bg="#252526")
        f_col1.pack(side=tk.LEFT, padx=20, pady=10)
        self.btn_laser = tk.Button(
            f_col1, text="Encender Láser", font=("Arial", 11, "bold"),
            bg="#cc0000", fg="white", activebackground="#ff3333",
            command=self.conmutar_laser, width=14, height=2
        )
        self.btn_laser.pack()

        f_col2 = tk.Frame(f_controles, bg="#252526")
        f_col2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        f_wave_hdr = tk.Frame(f_col2, bg="#252526")
        f_wave_hdr.pack(fill=tk.X, anchor="w", pady=(0, 5))
        
        self.lbl_wave = ttk.Label(f_wave_hdr, text=f"Longitud de onda (λ): {self.wavelength:.0f} nm")
        self.lbl_wave.pack(side=tk.LEFT)
        
        colores_rapidos = [("Rojo", 650, "#cc0000"), ("Verde", 520, "#00aa00"), ("Azul", 450, "#0044ff")]
        for color, nm, hex_c in colores_rapidos:
            b = tk.Button(f_wave_hdr, text=color, bg=hex_c, fg="white", font=("Arial", 8, "bold"),
                          command=lambda n=nm: self.fijar_color_rapido(n))
            b.pack(side=tk.RIGHT, padx=2)
            
        self.sl_wavelen = ttk.Scale(f_col2, from_=400, to=700, command=self.act_wavelength)
        self.sl_wavelen.set(self.wavelength)
        self.sl_wavelen.pack(fill=tk.X, pady=(0, 10))
        
        self.lbl_int = ttk.Label(f_col2, text=f"Intensidad: {self.intensidad:.0f} %")
        self.lbl_int.pack(anchor="w")
        self.sl_intensidad = ttk.Scale(f_col2, from_=0, to=100, command=self.act_intensidad)
        self.sl_intensidad.set(self.intensidad)
        self.sl_intensidad.pack(fill=tk.X)

    def conmutar_laser(self):
        self.laser_encendido = not self.laser_encendido
        if self.laser_encendido:
            self.btn_laser.config(text="Apagar Láser", bg="#00aa00", activebackground="#33cc33")
        else:
            self.btn_laser.config(text="Encender Láser", bg="#cc0000", activebackground="#ff3333")

    def fijar_color_rapido(self, nm):
        self.sl_wavelen.set(nm)
        self.act_wavelength(nm)

    def act_wavelength(self, val):
        self.wavelength = float(val)
        self.lbl_wave.config(text=f"Longitud de onda (λ): {self.wavelength:.0f} nm")

    def act_intensidad(self, val):
        self.intensidad = float(val)
        self.lbl_int.config(text=f"Intensidad: {self.intensidad:.0f} %")

    def wavelength_to_hex(self, wl):
        r, g, b = 0.0, 0.0, 0.0
        if 400 <= wl < 440:
            r = -(wl - 440) / (440 - 400); b = 1.0
        elif 440 <= wl < 490:
            g = (wl - 440) / (490 - 440); b = 1.0
        elif 490 <= wl < 580:
            r = 0.0; g = 1.0; b = -(wl - 580) / (580 - 490)
        elif 580 <= wl < 645:
            r = (wl - 580) / (645 - 580); g = 1.0 - (wl - 580)/(645 - 580)
        elif 645 <= wl <= 700:
            r = 1.0; g = 0.0; b = 0.0
            
        factor = 1.0
        if 400 <= wl < 420: factor = 0.3 + 0.7*(wl - 400)/(420 - 400)
        elif 700 >= wl > 650: factor = 0.3 + 0.7*(700 - wl)/(700 - 650)
            
        ir = int(max(0, min(255, r * factor * 255)))
        ig = int(max(0, min(255, g * factor * 255)))
        ib = int(max(0, min(255, b * factor * 255)))
        return f"#{ir:02x}{ig:02x}{ib:02x}"

    def bucle_animacion(self):
        self.canvas_izq.delete("all")
        w = self.canvas_izq.winfo_width()
        h = self.canvas_izq.winfo_height()
        
        if w > 1:
            cy = h / 2
            offset_y = h / 3.5  
            x_barrera = w * 0.55  
            color_actual = self.wavelength_to_hex(self.wavelength)
            
            self.canvas_izq.create_rectangle(x_barrera, 0, w, h, fill="#1a202c", outline="")
            self.canvas_izq.create_line(x_barrera, 0, x_barrera, h, fill="#4a5568", width=2, dash=(4, 4))
            
            self.canvas_izq.create_text(x_barrera - 80, cy - offset_y - 25, text="Onda Reflejada", fill="#a0aec0", font=("Arial", 10, "bold"))
            self.canvas_izq.create_text(x_barrera + 80, cy - 25, text="Onda Absorbida", fill="#a0aec0", font=("Arial", 10, "bold"))
            self.canvas_izq.create_text(x_barrera + 80, cy + offset_y - 25, text="Onda Transmitida", fill="#a0aec0", font=("Arial", 10, "bold"))
            
            self.canvas_izq.create_rectangle(15, cy - 20, 65, cy + 20, fill="#555555", outline="#888888", width=1.5)
            self.canvas_izq.create_polygon(65, cy - 20, 105, cy - 35, 105, cy + 35, 65, cy + 20, fill="#333333", outline="#888888", width=1.5)
            color_switch = "#00ff00" if self.laser_encendido else "#aa0000"
            self.canvas_izq.create_rectangle(30, cy - 25, 45, cy - 20, fill=color_switch, outline="")
            
            if self.laser_encendido:
                self.canvas_izq.create_oval(100, cy - 35, 110, cy + 35, fill=color_actual, outline="")
                
                amp_universal = (self.intensidad / 100.0) * (h / 8)
                k_incidente = (2 * math.pi) / max(10, (750 - self.wavelength)) 
                fase_en_frontera = k_incidente * (x_barrera - 105) - self.fase_onda

                puntos_inc, puntos_ref, puntos_abs, puntos_trans = [], [], [], []
                
                for x in range(105, int(x_barrera), 2):
                    y = cy + amp_universal * math.sin(k_incidente * (x - 105) - self.fase_onda)
                    puntos_inc.append((x, y))
                    
                cy_ref = cy - offset_y
                for x in range(105, int(x_barrera), 2):
                    y = cy_ref + amp_universal * math.sin(k_incidente * (x_barrera - x) + fase_en_frontera + math.pi)
                    puntos_ref.append((x, y))

                cy_abs = cy
                for x in range(int(x_barrera), w, 2):
                    y = cy_abs + amp_universal * math.sin(k_incidente * (x - x_barrera) + fase_en_frontera)
                    puntos_abs.append((x, y))

                cy_trans = cy + offset_y
                for x in range(int(x_barrera), w, 2):
                    y = cy_trans + amp_universal * math.sin(k_incidente * (x - x_barrera) + fase_en_frontera)
                    puntos_trans.append((x, y))
                    
                self.canvas_izq.create_line(x_barrera, cy_ref, x_barrera, cy_trans, fill=color_actual, dash=(2, 2))
                self.canvas_izq.create_oval(x_barrera-4, cy_ref-4, x_barrera+4, cy_ref+4, fill=color_actual)
                self.canvas_izq.create_oval(x_barrera-4, cy_abs-4, x_barrera+4, cy_abs+4, fill=color_actual)
                self.canvas_izq.create_oval(x_barrera-4, cy_trans-4, x_barrera+4, cy_trans+4, fill=color_actual)

                if len(puntos_inc) > 1: self.canvas_izq.create_line(puntos_inc, fill=color_actual, width=3) 
                if len(puntos_ref) > 1: self.canvas_izq.create_line(puntos_ref, fill=color_actual, width=2) 
                if len(puntos_abs) > 1: self.canvas_izq.create_line(puntos_abs, fill=color_actual, width=2) 
                if len(puntos_trans) > 1: self.canvas_izq.create_line(puntos_trans, fill=color_actual, width=2) 
                
                self.fase_onda += 0.35 
        
        self.root.after(16, self.bucle_animacion)


# =====================================================================
# PARTE 2: LÓGICA MATEMÁTICA Y ANIMACIÓN DEL ÁTOMO
# =====================================================================
def curva_gaussiana(x, mu, sigma, amplitud):
    return amplitud * np.exp(-0.5 * ((x - mu) / sigma)**2)

def integrar_panel_central_atomo(app):
    app.banda_absorcion_min = 500.0  
    app.banda_absorcion_max = 550.0
    app.electron_excitado = False
    app.contador_tiempo_simulado = 0.0
    
    # Mantenemos las variables ocultas para que el átomo siga funcionando
    app.tiempo_vida_simulado = 5000.0  
    
    app.foton_activo = False
    app.foton_x, app.foton_y, app.foton_angulo, app.foton_velocidad, app.foton_fase = 0.0, 0.0, 0.0, 5.0, 0.0

    # (UI Omitida: Se quitaron los controles de tiempo de vida y rendimiento cuántico)

    def loop_renderizado_atomo():
        app.canvas_cen.delete("all")
        w = app.canvas_cen.winfo_width()
        h = app.canvas_cen.winfo_height()
        
        if w > 1:
            cx, cy = w / 2, h / 2
            r_fundamental, r_excitado = 40.0, 90.0
            
            if app.laser_encendido and (app.banda_absorcion_min <= app.wavelength <= app.banda_absorcion_max):
                if not app.electron_excitado:
                    app.electron_excitado = True
                    app.contador_tiempo_simulado = 0.0
            else:
                if not app.laser_encendido:
                    app.electron_excitado = False
            
            if app.electron_excitado:
                app.contador_tiempo_simulado += 35.0
                if app.contador_tiempo_simulado >= app.tiempo_vida_simulado:
                    app.electron_excitado = False
                    app.contador_tiempo_simulado = 0.0
                    app.foton_activo = True
                    app.foton_x, app.foton_y = cx, cy
                    app.foton_angulo = random.uniform(0, 2 * math.pi)

            color_n1 = "#4a5568"
            color_n2 = "#00f0ff" if app.electron_excitado else "#2d3748"
            
            app.canvas_cen.create_oval(cx - r_fundamental, cy - r_fundamental, cx + r_fundamental, cy + r_fundamental, outline=color_n1, width=2, dash=(2, 2))
            app.canvas_cen.create_oval(cx - r_excitado, cy - r_excitado, cx + r_excitado, cy + r_excitado, outline=color_n2, width=3)
            app.canvas_cen.create_oval(cx - 15, cy - 15, cx + 15, cy + 15, fill="#cc0000", outline="#ff3333")
            app.canvas_cen.create_text(cx, cy, text="+", fill="white", font=("Arial", 12, "bold"))
            app.canvas_cen.create_text(cx - r_fundamental - 20, cy, text="n=1", fill="#a0aec0", font=("Arial", 9))
            app.canvas_cen.create_text(cx - r_excitado - 20, cy, text="n=2", fill=color_n2, font=("Arial", 9, "bold"))
            
            r_actual = r_excitado if app.electron_excitado else r_fundamental
            color_electron = "#ffff00" if app.electron_excitado else "#00ffcc"
            angulo_electron = app.fase_onda * 0.1
            ex = cx + r_actual * math.cos(angulo_electron)
            ey = cy + r_actual * math.sin(angulo_electron)
            app.canvas_cen.create_oval(ex - 7, ey - 7, ex + 7, ey + 7, fill=color_electron, outline="white", width=1)
            
            if app.foton_activo:
                app.foton_x += app.foton_velocidad * math.cos(app.foton_angulo)
                app.foton_y += app.foton_velocidad * math.sin(app.foton_angulo)
                app.foton_fase += 0.8
                
                puntos_foton = []
                for i in range(30):
                    t = i - 15
                    basex = app.foton_x + t * math.cos(app.foton_angulo)
                    basey = app.foton_y + t * math.sin(app.foton_angulo)
                    perpx, perpy = -math.sin(app.foton_angulo), math.cos(app.foton_angulo)
                    amp_foton = 6 * math.sin((i / 30) * math.pi)
                    osc = amp_foton * math.sin(app.foton_fase + i * 0.5)
                    puntos_foton.append((basex + perpx * osc, basey + perpy * osc))
                
                if len(puntos_foton) > 1:
                    app.canvas_cen.create_line(puntos_foton, fill="#ff6600", width=2)
                    
                if app.foton_x < 0 or app.foton_x > w or app.foton_y < 0 or app.foton_y > h:
                    app.foton_activo = False

            if app.electron_excitado:
                app.canvas_cen.create_text(cx, h - 30, text=f"Estado Excitado: {app.contador_tiempo_simulado/1000:.2f} ns", fill="#ffff00", font=("Arial", 10, "bold"))
                
        app.root.after(35, loop_renderizado_atomo)
    loop_renderizado_atomo()


# =====================================================================
# PARTE 3: INTEGRACIÓN FINAL Y PANEL DERECHO (GRÁFICAS)
# =====================================================================
def iniciar_programa_completo():
    root = tk.Tk()
    app = ModuloLuzIncidente(root) 
    
    app.canvas_der = tk.Frame(root, bg="#1e1e1e")
    for widget in root.pack_slaves():
        if isinstance(widget, tk.Frame) and len(widget.pack_slaves()) > 0:
            app.canvas_der.pack(in_=widget, side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            break
            
    integrar_panel_central_atomo(app)
    
    bg_color = "#000000"       
    borde_verde = "#00FF00"    
    
    frame_arriba = tk.Frame(app.canvas_der, bg=bg_color)
    frame_medio = tk.Frame(app.canvas_der, bg=bg_color, height=160) 
    frame_abajo = tk.Frame(app.canvas_der, bg=bg_color)

    frame_arriba.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    frame_medio.pack(side=tk.TOP, fill=tk.X, pady=5)
    frame_abajo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    fig_abs = Figure(figsize=(4, 2.0), dpi=100)
    fig_abs.patch.set_facecolor(bg_color)
    ax_abs = fig_abs.add_subplot(111, facecolor=bg_color)
    
    fig_flu = Figure(figsize=(4, 2.0), dpi=100)
    fig_flu.patch.set_facecolor(bg_color)
    ax_flu = fig_flu.add_subplot(111, facecolor=bg_color)

    for ax, titulo in zip([ax_abs, ax_flu], ['Espectro de Absorción', 'Espectro de Fluorescencia']):
        ax.set_title(titulo, color=borde_verde, fontsize=10, fontweight='bold', pad=6)
        ax.tick_params(colors=borde_verde, labelsize=8)
        ax.spines['bottom'].set_color(borde_verde)
        ax.spines['left'].set_color(borde_verde)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylim(0, 1.1)
        ax.set_xlim(400, 750)

    fig_abs.subplots_adjust(bottom=0.18, top=0.8, left=0.15, right=0.95)
    fig_flu.subplots_adjust(bottom=0.18, top=0.8, left=0.15, right=0.95)

    canvas_abs = FigureCanvasTkAgg(fig_abs, master=frame_arriba)
    canvas_abs.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    canvas_flu = FigureCanvasTkAgg(fig_flu, master=frame_abajo)
    canvas_flu.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    canvas_luz = tk.Canvas(frame_medio, bg=bg_color, height=160, highlightthickness=1, highlightbackground=borde_verde)
    canvas_luz.pack(fill=tk.BOTH, expand=True)

    x_vals = np.linspace(400, 750, 200)
    linea_abs, = ax_abs.plot(x_vals, np.zeros_like(x_vals), linewidth=2.5)
    linea_flu, = ax_flu.plot(x_vals, np.zeros_like(x_vals), linewidth=2.5)

    ultima_onda, ultima_intensidad, ultimo_estado_laser = -1, -1, None
    tiempo_fase = 0.0

    def monitorear_cambios():
        nonlocal ultima_onda, ultima_intensidad, ultimo_estado_laser, tiempo_fase
        
        onda_actual = app.wavelength
        intensidad_actual = app.intensidad
        laser_activo = app.laser_encendido
        
        desplazamiento_stokes = 60
        onda_emitida = onda_actual + desplazamiento_stokes
        
        if (onda_actual != ultima_onda) or (intensidad_actual != ultima_intensidad) or (laser_activo != ultimo_estado_laser):
            color_abs = app.wavelength_to_hex(min(onda_actual, 700))
            color_flu = app.wavelength_to_hex(min(onda_emitida, 700))
            
            altura_grafica = intensidad_actual / 100.0 if laser_activo else 0.0
                
            abs_y = curva_gaussiana(x_vals, mu=onda_actual, sigma=15, amplitud=altura_grafica)
            flu_y = curva_gaussiana(x_vals, mu=onda_emitida, sigma=25, amplitud=altura_grafica * 0.8)
            
            linea_abs.set_ydata(abs_y)
            linea_abs.set_color(color_abs)
            linea_flu.set_ydata(flu_y)
            linea_flu.set_color(color_flu)
            
            canvas_abs.draw()
            canvas_flu.draw()
            
            ultima_onda, ultima_intensidad, ultimo_estado_laser = onda_actual, intensidad_actual, laser_activo

        canvas_luz.delete("all")
        w = canvas_luz.winfo_width()
        h = canvas_luz.winfo_height()
        
        if w > 1:
            color_fluorescencia = app.wavelength_to_hex(min(onda_emitida, 700))
            
            if laser_activo:
                tiempo_fase += 0.4
                amplitud = max(2, (intensidad_actual / 100.0) * 10)
                y_centro = h / 2
                
                num_rayos = 5
                paso_angular = 25 
                
                for i in range(num_rayos):
                    y_fin = y_centro + (i - (num_rayos // 2)) * paso_angular
                    puntos_flu = []
                    
                    # AHORA INICIA EXACTAMENTE DESDE X = 0 HASTA EL FINAL
                    for cx in range(0, int(w), 4):
                        factor_x = cx / w
                        base_y = y_centro + factor_x * (y_fin - y_centro)
                        fase_flu = cx * 0.1 + tiempo_fase + (i * 0.5)
                        puntos_flu.extend([cx, base_y + (amplitud * 0.6) * math.sin(fase_flu)])
                        
                    if len(puntos_flu) >= 4:
                        canvas_luz.create_line(puntos_flu, fill=color_fluorescencia, width=1.5)
                        
            else:
                canvas_luz.create_text(w/2, h/2, text="Esperando radiación...", fill=borde_verde, font=("Arial", 9, "italic"))
        
        root.after(35, monitorear_cambios)

    monitorear_cambios()
    root.mainloop()

if __name__ == "__main__":
    iniciar_programa_completo()