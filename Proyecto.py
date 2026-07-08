import tkinter as tk
from tkinter import ttk

class FrontendSimacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación: Interacción Luz-Materia")
        self.root.geometry("1100x600")
        self.root.configure(bg="#1e1e1e") # Fondo oscuro elegante
        
        # --- VARIABLES DE ESTADO (Para conectar con el backend) ---
        self.laser_encendido = False
        self.wavelength = 520.0       # λ inicial (nm) 
        self.intensidad = 50.0        # % 
        self.tiempo_vida = 5.0        # ns 
        self.ancho_espectral = 10.0   # nm 
        self.rendimiento_cuantico = 0.5 # Entre 0 y 1 
        
        # Estilo para los componentes de Tkinter
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")
        self.estilo.configure(".", background="#1e1e1e", foreground="white")
        self.estilo.configure("TLabel", background="#1e1e1e", foreground="white", font=("Arial", 10))
        
        # --- CONSTRUCCIÓN DE LA INTERFAZ ---
        self.crear_titulo()
        self.crear_tres_paneles()
        self.crear_panel_controles()

    def crear_titulo(self):
        titulo = tk.Label(
            self.root, 
            text="INTERACCIÓN LUZ-MATERIA", # 
            font=("Arial", 16, "bold"), 
            bg="#1e1e1e", 
            fg="#00ffcc", 
            pady=10
        )
        titulo.pack(side=tk.TOP, fill=tk.X)

    def crear_tres_paneles(self):
        # Contenedor principal para los paneles
        contenedor_paneles = tk.Frame(self.root, bg="#1e1e1e")
        contenedor_paneles.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 1. Panel Izquierdo: Onda Incidente [cite: 7]
        frame_izq = tk.LabelFrame(contenedor_paneles, text=" Luz Incidente ", bg="#1e1e1e", fg="white", font=("Arial", 10, "bold"))
        frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_izq = tk.Canvas(frame_izq, bg="black", highlightthickness=0)
        self.canvas_izq.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 2. Panel Central: Átomo [cite: 8]
        frame_cen = tk.LabelFrame(contenedor_paneles, text=" Átomo (Niveles) ", bg="#1e1e1e", fg="white", font=("Arial", 10, "bold"))
        frame_cen.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_cen = tk.Canvas(frame_cen, bg="#0a0a0a", highlightthickness=0)
        self.canvas_cen.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 3. Panel Derecho: Gráficas de Absorbancia y Fluorescencia [cite: 5]
        frame_der = tk.LabelFrame(contenedor_paneles, text=" Gráficas ", bg="#1e1e1e", fg="white", font=("Arial", 10, "bold"))
        frame_der.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_der = tk.Canvas(frame_der, bg="black", highlightthickness=0)
        self.canvas_der.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def crear_panel_controles(self):
        # Contenedor inferior para los controles 
        frame_controles = tk.LabelFrame(self.root, text=" Panel de Controles ", bg="#252526", fg="#00ffcc", font=("Arial", 10, "bold"))
        frame_controles.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)
        
        # --- COLUMNA 1: BOTÓN DE ENCENDIDO ---
        frame_col1 = tk.Frame(frame_controles, bg="#252526")
        frame_col1.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.btn_laser = tk.Button(
            frame_col1, 
            text="Encender Láser", # 
            font=("Arial", 11, "bold"),
            bg="#cc0000", 
            fg="white", 
            activebackground="#ff3333",
            command=self.conmutar_laser,
            width=15,
            height=2
        )
        self.btn_laser.pack()

        # --- COLUMNA 2: DESLIZADORES DE ONDA E INTENSIDAD ---
        frame_col2 = tk.Frame(frame_controles, bg="#252526")
        frame_col2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Longitud de onda (400 - 700 nm) 
        self.lbl_wave = ttk.Label(frame_col2, text=f"Longitud de onda (λ): {self.wavelength:.0f} nm")
        self.lbl_wave.pack(anchor="w")
        self.sl_wavelen = ttk.Scale(frame_col2, from_=400, to=700, command=self.act_wavelength)
        self.sl_wavelen.set(self.wavelength)
        self.sl_wavelen.pack(fill=tk.X, pady=(0, 10))
        
        # Intensidad (0 - 100 %) 
        self.lbl_int = ttk.Label(frame_col2, text=f"Intensidad: {self.intensidad:.0f} %")
        self.lbl_int.pack(anchor="w")
        self.sl_intensidad = ttk.Scale(frame_col2, from_=0, to=100, command=self.act_intensidad)
        self.sl_intensidad.set(self.intensidad)
        self.sl_intensidad.pack(fill=tk.X)

        # --- COLUMNA 3: DESLIZADORES AVANZADOS ---
        frame_col3 = tk.Frame(frame_controles, bg="#252526")
        frame_col3.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20)
        

    # --- MÉTODOS DE ACTUALIZACIÓN EN TIEMPO REAL ---
    def conmutar_laser(self):
        self.laser_encendido = not self.laser_encendido
        if self.laser_encendido:
            self.btn_laser.config(text="Apagar Láser", bg="#00aa00", activebackground="#33cc33")
        else:
            self.btn_laser.config(text="Encender Láser", bg="#cc0000", activebackground="#ff3333")
            
    def act_wavelength(self, val):
        self.wavelength = float(val)
        self.lbl_wave.config(text=f"Longitud de onda (λ): {self.wavelength:.0f} nm")
        
    def act_intensidad(self, val):
        self.intensidad = float(val)
        self.lbl_int.config(text=f"Intensidad: {self.intensidad:.0f} %")
        
    def act_tiempo_vida(self, val):
        self.tiempo_vida = float(val)
        self.lbl_vida.config(text=f"Tiempo de vida: {self.tiempo_vida:.1f} ns")
        
    def act_rendimiento(self, val):
        self.rendimiento_cuantico = float(val)
        self.lbl_rendimiento.config(text=f"Rendimiento Cuántico: {self.rendimiento_cuantico:.2f}")

# Inicialización de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = FrontendSimacion(root)
    root.mainloop()