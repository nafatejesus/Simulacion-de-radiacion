import tkinter as tk
from tkinter import ttk
import math


class ModuloLuzIncidente:
    def __init__(self, root):
        self.root = root
        self.root.title(
            "Simulación: Interacción Radiación Electromagnética con la Materia"
        )
        self.root.geometry("1200x650")
        self.root.configure(bg="#1e1e1e")

        self.laser_encendido = False
        self.wavelength = 520.0
        self.intensidad = 50.0
        self.fase_onda = 0.0

        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")
        self.estilo.configure(".", background="#1e1e1e", foreground="white")
        self.estilo.configure(
            "TLabel", background="#1e1e1e", foreground="white", font=("Arial", 10)
        )

        self.crear_titulo()
        self.crear_paneles_completos()
        self.crear_controles_linterna()
        self.bucle_animacion()

    def crear_titulo(self):
        titulo = tk.Label(
            self.root,
            text="SIMULACIÓN DE LA INTERACCIÓN DE LA RADIACIÓN ELECTROMAGNÉTICA CON LA MATERIA",
            font=("Arial", 14, "bold"),
            bg="#1e1e1e",
            fg="#00ffcc",
            pady=10,
        )
        titulo.pack(side=tk.TOP, fill=tk.X)

    def crear_paneles_completos(self):
        contenedor = tk.Frame(self.root, bg="#1e1e1e")
        contenedor.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        f_izq = tk.LabelFrame(
            contenedor,
            text=" Propagación y Frontera del Material ",
            bg="#1e1e1e",
            fg="white",
            font=("Arial", 9, "bold"),
        )
        f_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_izq = tk.Canvas(f_izq, bg="black", highlightthickness=0)
        self.canvas_izq.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        f_cen = tk.LabelFrame(
            contenedor,
            text=" Átomo (Niveles de Energía) ",
            bg="#1e1e1e",
            fg="white",
            font=("Arial", 9, "bold"),
        )
        f_cen.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_cen = tk.Canvas(f_cen, bg="#0a0a0a", highlightthickness=0)
        self.canvas_cen.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def crear_controles_linterna(self):
        f_controles = tk.LabelFrame(
            self.root,
            text=" Panel de Controles ",
            bg="#252526",
            fg="#00ffcc",
            font=("Arial", 10, "bold"),
        )
        f_controles.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)

        f_col1 = tk.Frame(f_controles, bg="#252526")
        f_col1.pack(side=tk.LEFT, padx=20, pady=10)
        self.btn_laser = tk.Button(
            f_col1,
            text="Encender Láser",
            font=("Arial", 11, "bold"),
            bg="#cc0000",
            fg="white",
            activebackground="#ff3333",
            command=self.conmutar_laser,
            width=14,
            height=2,
        )
        self.btn_laser.pack()

        f_col2 = tk.Frame(f_controles, bg="#252526")
        f_col2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        f_wave_hdr = tk.Frame(f_col2, bg="#252526")
        f_wave_hdr.pack(fill=tk.X, anchor="w", pady=(0, 5))

        self.lbl_wave = ttk.Label(
            f_wave_hdr, text=f"Longitud de onda (λ): {self.wavelength:.0f} nm"
        )
        self.lbl_wave.pack(side=tk.LEFT)

        colores_rapidos = [
            ("Rojo", 650, "#cc0000"),
            ("Verde", 520, "#00aa00"),
            ("Azul", 450, "#0044ff"),
        ]
        for color, nm, hex_c in colores_rapidos:
            b = tk.Button(
                f_wave_hdr,
                text=color,
                bg=hex_c,
                fg="white",
                font=("Arial", 8, "bold"),
                command=lambda n=nm: self.fijar_color_rapido(n),
            )
            b.pack(side=tk.RIGHT, padx=2)

        self.sl_wavelen = ttk.Scale(
            f_col2, from_=400, to=700, command=self.act_wavelength
        )
        self.sl_wavelen.set(self.wavelength)
        self.sl_wavelen.pack(fill=tk.X, pady=(0, 10))

        self.lbl_int = ttk.Label(f_col2, text=f"Intensidad: {self.intensidad:.0f} %")
        self.lbl_int.pack(anchor="w")
        self.sl_intensidad = ttk.Scale(
            f_col2, from_=0, to=100, command=self.act_intensidad
        )
        self.sl_intensidad.set(self.intensidad)
        self.sl_intensidad.pack(fill=tk.X)

    def conmutar_laser(self):
        self.laser_encendido = not self.laser_encendido
        if self.laser_encendido:
            self.btn_laser.config(
                text="Apagar Láser", bg="#00aa00", activebackground="#33cc33"
            )
        else:
            self.btn_laser.config(
                text="Encender Láser", bg="#cc0000", activebackground="#ff3333"
            )

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
            r = -(wl - 440) / (440 - 400)
            b = 1.0
        elif 440 <= wl < 490:
            g = (wl - 440) / (490 - 440)
            b = 1.0
        elif 490 <= wl < 580:
            r = 0.0
            g = 1.0
            b = -(wl - 580) / (580 - 490)
        elif 580 <= wl < 645:
            r = (wl - 580) / (645 - 580)
            g = 1.0 - (wl - 580) / (645 - 580)
        elif 645 <= wl <= 700:
            r = 1.0
            g = 0.0
            b = 0.0

        factor = 1.0
        if 400 <= wl < 420:
            factor = 0.3 + 0.7 * (wl - 400) / (420 - 400)
        elif 700 >= wl > 650:
            factor = 0.3 + 0.7 * (700 - wl) / (700 - 650)

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
            offset_y = h / 3.5  # Separación vertical para las ondas resultantes
            x_barrera = w * 0.55  # Posición de la frontera del material
            color_actual = self.wavelength_to_hex(self.wavelength)

            # --- DIBUJO DEL ENTORNO ---
            # Material absorbente / transparente (Barrera derecha)
            self.canvas_izq.create_rectangle(
                x_barrera, 0, w, h, fill="#1a202c", outline=""
            )
            self.canvas_izq.create_line(
                x_barrera, 0, x_barrera, h, fill="#4a5568", width=2, dash=(4, 4)
            )

            # Textos de los canales
            self.canvas_izq.create_text(
                x_barrera - 80,
                cy - offset_y - 25,
                text="Onda Reflejada",
                fill="#a0aec0",
                font=("Arial", 10, "bold"),
            )
            self.canvas_izq.create_text(
                x_barrera + 80,
                cy - 25,
                text="Onda Absorbida",
                fill="#a0aec0",
                font=("Arial", 10, "bold"),
            )
            self.canvas_izq.create_text(
                x_barrera + 80,
                cy + offset_y - 25,
                text="Onda Transmitida",
                fill="#a0aec0",
                font=("Arial", 10, "bold"),
            )

            # Linterna (Láser)
            self.canvas_izq.create_rectangle(
                15, cy - 20, 65, cy + 20, fill="#555555", outline="#888888", width=1.5
            )
            self.canvas_izq.create_polygon(
                65,
                cy - 20,
                105,
                cy - 35,
                105,
                cy + 35,
                65,
                cy + 20,
                fill="#333333",
                outline="#888888",
                width=1.5,
            )
            color_switch = "#00ff00" if self.laser_encendido else "#aa0000"
            self.canvas_izq.create_rectangle(
                30, cy - 25, 45, cy - 20, fill=color_switch, outline=""
            )

            if self.laser_encendido:
                self.canvas_izq.create_oval(
                    100, cy - 35, 110, cy + 35, fill=color_actual, outline=""
                )

                # --- MATEMÁTICA DE LAS ONDAS ---
                # Todas las ondas tendrán la misma amplitud por el momento según tu solicitud
                amp_universal = (self.intensidad / 100.0) * (h / 8)
                k_incidente = (2 * math.pi) / max(10, (750 - self.wavelength))

                # Fase exacta de la onda al tocar la barrera para que las divisiones nazcan sincronizadas
                fase_en_frontera = k_incidente * (x_barrera - 105) - self.fase_onda

                puntos_inc = []
                puntos_ref = []
                puntos_abs = []
                puntos_trans = []

                # 1. Calcular Onda Incidente (Centro, viaja a la derecha)
                for x in range(105, int(x_barrera), 2):
                    y = cy + amp_universal * math.sin(
                        k_incidente * (x - 105) - self.fase_onda
                    )
                    puntos_inc.append((x, y))

                # 2. Calcular Onda Reflejada (Canal Superior, viaja a la izquierda hacia el láser)
                cy_ref = cy - offset_y
                for x in range(105, int(x_barrera), 2):
                    # Se suma pi para simular el rebote en un medio más denso y se invierte el viaje
                    y = cy_ref + amp_universal * math.sin(
                        k_incidente * (x_barrera - x) + fase_en_frontera + math.pi
                    )
                    puntos_ref.append((x, y))

                # 3. Calcular Onda Absorbida (Canal Central, viaja a la derecha dentro del material)
                cy_abs = cy
                for x in range(int(x_barrera), w, 2):
                    y = cy_abs + amp_universal * math.sin(
                        k_incidente * (x - x_barrera) + fase_en_frontera
                    )
                    puntos_abs.append((x, y))

                # 4. Calcular Onda Transmitida (Canal Inferior, viaja a la derecha dentro del material)
                cy_trans = cy + offset_y
                for x in range(int(x_barrera), w, 2):
                    y = cy_trans + amp_universal * math.sin(
                        k_incidente * (x - x_barrera) + fase_en_frontera
                    )
                    puntos_trans.append((x, y))

                # --- RENDERIZADO VISUAL ---
                # Dibujar líneas guía verticales en la frontera para conectar las 3 divisiones
                self.canvas_izq.create_line(
                    x_barrera,
                    cy_ref,
                    x_barrera,
                    cy_trans,
                    fill=color_actual,
                    dash=(2, 2),
                )
                self.canvas_izq.create_oval(
                    x_barrera - 4,
                    cy_ref - 4,
                    x_barrera + 4,
                    cy_ref + 4,
                    fill=color_actual,
                )
                self.canvas_izq.create_oval(
                    x_barrera - 4,
                    cy_abs - 4,
                    x_barrera + 4,
                    cy_abs + 4,
                    fill=color_actual,
                )
                self.canvas_izq.create_oval(
                    x_barrera - 4,
                    cy_trans - 4,
                    x_barrera + 4,
                    cy_trans + 4,
                    fill=color_actual,
                )

                # Dibujar los caminos de onda
                if len(puntos_inc) > 1:
                    self.canvas_izq.create_line(
                        puntos_inc, fill=color_actual, width=3
                    )  # Principal gruesa
                if len(puntos_ref) > 1:
                    self.canvas_izq.create_line(
                        puntos_ref, fill=color_actual, width=2
                    )  # Reflexión
                if len(puntos_abs) > 1:
                    self.canvas_izq.create_line(
                        puntos_abs, fill=color_actual, width=2
                    )  # Absorción
                if len(puntos_trans) > 1:
                    self.canvas_izq.create_line(
                        puntos_trans, fill=color_actual, width=2
                    )  # Transmisión

                # Avanzar el tiempo (fase)
                self.fase_onda += 0.35

        # Bucle 60 FPS aprox.
        self.root.after(16, self.bucle_animacion)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModuloLuzIncidente(root)
    root.mainloop()
