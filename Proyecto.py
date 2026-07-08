import tkinter as tk
from tkinter import ttk
import math

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
        
        f_izq = tk.LabelFrame(contenedor, text=" Luz Incidente ", bg="#1e1e1e", fg="white", font=("Arial", 9, "bold"))
        f_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_izq = tk.Canvas(f_izq, bg="black", highlightthickness=0)
        self.canvas_izq.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        f_cen = tk.LabelFrame(contenedor, text=" Átomo (Niveles de Energía) ", bg="#1e1e1e", fg="white", font=("Arial", 9, "bold"))
        f_cen.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_cen = tk.Canvas(f_cen, bg="#0a0a0a", highlightthickness=0)
        self.canvas_cen.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        f_der = tk.LabelFrame(contenedor, text=" Espectros de Absorción y Fluorescencia ", bg="#1e1e1e", fg="white", font=("Arial", 9, "bold"))
        f_der.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_der = tk.Canvas(f_der, bg="black", highlightthickness=0)
        self.canvas_der.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

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
        
        colores_rapidos = [("Rojo", 650, "#cc0000"), ("Verde", 530, "#00aa00"), ("Azul", 450, "#0044ff")]
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
            color_actual = self.wavelength_to_hex(self.wavelength)
            
            self.canvas_izq.create_rectangle(15, cy - 20, 65, cy + 20, fill="#555555", outline="#888888", width=1.5)
            self.canvas_izq.create_polygon(65, cy - 20, 105, cy - 35, 105, cy + 35, 65, cy + 20, fill="#333333", outline="#888888", width=1.5)
            color_switch = "#00ff00" if self.laser_encendido else "#aa0000"
            self.canvas_izq.create_rectangle(30, cy - 25, 45, cy - 20, fill=color_switch, outline="")
            
            if self.laser_encendido:
                self.canvas_izq.create_oval(100, cy - 35, 110, cy + 35, fill=color_actual, outline="")
                
                puntos = []
                amp = (self.intensidad / 100.0) * (h / 4)
                frec_angular = (2 * math.pi) / max(10, (750 - self.wavelength))
                
                for x in range(105, w, 2):
                    y = cy + amp * math.sin(frec_angular * (x - 105) - self.fase_onda)
                    puntos.append((x, y))
                    
                if len(puntos) > 1:
                    self.canvas_izq.create_line(puntos, fill=color_actual, width=3)
                
                self.fase_onda += 0.35 
        
        self.root.after(22, self.bucle_animacion)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModuloLuzIncidente(root)
    root.mainloop()
