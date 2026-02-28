import tkinter as tk
from tkinter import ttk
from splitter import ShapeDataStructure

class ShapeUI:
    def __init__(self, width=20, height=20, resolution=1, cell_size=25):
        self.width = width
        self.height = height
        self.resolution = resolution
        self.cell_size = cell_size

        self.shape = ShapeDataStructure(width, height, resolution)

        self.root = tk.Tk()
        self.root.title("Integration + Physics Tool")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # ---------------- CANVAS ----------------
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side="left", fill="both", expand=True)

        canvas_width = width * cell_size
        canvas_height = height * cell_size

        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg="white"
        )
        self.canvas.pack()

        # ---------------- CONTROL PANEL ----------------
        self.control_frame = tk.Frame(self.main_frame, padx=15, pady=15)
        self.control_frame.pack(side="right", fill="y")

        self._build_controls()

        # ---------------- DRAW STATE ----------------
        self.drawing = False
        self.drawn_coordinates = []
        self.must_start = True  # enforce start at (0,0)

        self._bind_events()
        self._draw_grid()
        self._highlight_start_cell()

        self.status_label.config(text="Start drawing at (0,0)", fg="blue")

    # ---------------------------------------------------
    # CONTROL PANEL
    # ---------------------------------------------------

    def _build_controls(self):
        tk.Label(self.control_frame, text="Material", font=("Arial", 12, "bold")).pack(anchor="w")

        self.material_var = tk.StringVar(value="Steel")
        self.material_dropdown = ttk.Combobox(
            self.control_frame,
            textvariable=self.material_var,
            values=["Steel", "Aluminum", "Copper", "Custom"]
        )
        self.material_dropdown.pack(fill="x", pady=5)

        tk.Label(self.control_frame, text="Temperature (°C)", font=("Arial", 12, "bold")).pack(anchor="w", pady=(15, 0))

        self.temp_var = tk.StringVar(value="20.0")
        self.temp_entry = tk.Entry(self.control_frame, textvariable=self.temp_var)
        self.temp_entry.pack(fill="x", pady=5)

        tk.Button(self.control_frame, text="Clear", command=self.clear).pack(fill="x", pady=(15, 5))
        tk.Button(self.control_frame, text="Run Physics", command=self.run_physics).pack(fill="x", pady=(5, 15))

        # Heatmap legend
        self.legend_canvas = tk.Canvas(self.control_frame, width=50, height=200)
        self.legend_canvas.pack()

        self.status_label = tk.Label(self.control_frame, text="", fg="gray")
        self.status_label.pack(pady=10)

    # ---------------------------------------------------
    # EVENTS
    # ---------------------------------------------------

    def _bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_motion)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    def start_draw(self, event):
        canvas_x = event.x // self.cell_size
        canvas_y = event.y // self.cell_size

        x = canvas_x
        y = self.height - 1 - canvas_y

        if self.must_start:
            if (x, y) != (0, 0):
                self.status_label.config(text="Must start at (0,0)", fg="red")
                self._flash_cell(0, 0, "red")
                return
            else:
                self.must_start = False
                self.status_label.config(text="Drawing...", fg="green")

        self.drawing = True
        self.drawn_coordinates = []
        self.add_point_from_event(event)

    def draw_motion(self, event):
        if self.drawing:
            self.add_point_from_event(event)

    def end_draw(self, event):
        self.drawing = False
        self.integrate_shape()

    # ---------------------------------------------------
    # DRAWING
    # ---------------------------------------------------

    def add_point_from_event(self, event):
        canvas_x = event.x // self.cell_size
        canvas_y = event.y // self.cell_size

        # Convert to mathematical coordinates
        x = canvas_x
        y = self.height - 1 - canvas_y

        if (x, y) not in self.drawn_coordinates:
            self.drawn_coordinates.append((x, y))
            self._draw_cell(x, y, "black")

    def _highlight_start_cell(self):
        self._draw_cell(0, 0, "#90ee90")  # light green

    def _flash_cell(self, x, y, color):
        self._draw_cell(x, y, color)
        self.root.after(300, lambda: self._draw_cell(x, y, "#90ee90"))

    # ---------------------------------------------------
    # INTEGRATION
    # ---------------------------------------------------

    def integrate_shape(self):
        if not self.drawn_coordinates:
            return

        material = self.material_var.get()

        try:
            temperature = float(self.temp_var.get())
        except ValueError:
            self.status_label.config(text="Invalid temperature", fg="red")
            return

        self.shape.integrate_under_line(
            self.drawn_coordinates,
            material=material,
            temperature=temperature
        )

        self._render_uniform()
        self.status_label.config(text=f"{len(self.shape.drawn_points)} points integrated", fg="black")

    # ---------------------------------------------------
    # PHYSICS PLACEHOLDER
    # ---------------------------------------------------

    def run_physics(self):
        if not self.shape.drawn_points:
            return

        max_y = max(p.y for p in self.shape.drawn_points)

        for point in self.shape.drawn_points:
            base_temp = point.attributes['temperature']
            gradient = (point.y / max_y) * 50 if max_y > 0 else 0
            point.attributes['temperature'] = base_temp + gradient

        self._render_heatmap()
        self._draw_heatmap_legend()

        self.status_label.config(text="Physics simulation complete", fg="green")

    # ---------------------------------------------------
    # RENDERING
    # ---------------------------------------------------

    def _render_uniform(self):
        for point in self.shape.drawn_points:
            self._draw_cell(int(point.x), int(point.y), "skyblue")

    def _render_heatmap(self):
        temps = [p.attributes['temperature'] for p in self.shape.drawn_points]
        t_min = min(temps)
        t_max = max(temps)

        for point in self.shape.drawn_points:
            t = point.attributes['temperature']
            color = self._temperature_to_color(t, t_min, t_max)
            self._draw_cell(int(point.x), int(point.y), color)

    def _temperature_to_color(self, temp, t_min, t_max):
        if t_max == t_min:
            ratio = 0
        else:
            ratio = (temp - t_min) / (t_max - t_min)

        r = int(255 * ratio)
        b = int(255 * (1 - ratio))
        g = 50

        return f"#{r:02x}{g:02x}{b:02x}"

    def _draw_heatmap_legend(self):
        self.legend_canvas.delete("all")

        height = 200
        for i in range(height):
            ratio = i / height
            r = int(255 * ratio)
            b = int(255 * (1 - ratio))
            g = 50
            color = f"#{r:02x}{g:02x}{b:02x}"

            self.legend_canvas.create_rectangle(
                0, height - i,
                50, height - i - 1,
                fill=color,
                outline=""
            )

        temps = [p.attributes['temperature'] for p in self.shape.drawn_points]
        t_min = min(temps)
        t_max = max(temps)

        self.legend_canvas.create_text(25, 10, text=f"{t_max:.1f}", fill="black")
        self.legend_canvas.create_text(25, 190, text=f"{t_min:.1f}", fill="black")

    def _draw_cell(self, x, y, color):
        # Convert math y to canvas y
        canvas_y = self.height - 1 - y

        x1 = x * self.cell_size
        y1 = canvas_y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            outline="gray"
        )

    def _draw_grid(self):
        for x in range(self.width):
            for y in range(self.height):
                self._draw_cell(x, y, "white")

    # ---------------------------------------------------
    # CLEAR
    # ---------------------------------------------------

    def clear(self):
        self.shape.clear_shape()
        self.drawn_coordinates = []
        self.canvas.delete("all")
        self.legend_canvas.delete("all")
        self.must_start = True
        self._draw_grid()
        self._highlight_start_cell()
        self.status_label.config(text="Start drawing at (0,0)", fg="blue")

    # ---------------------------------------------------
    # RUN
    # ---------------------------------------------------

    def run(self):
        self.root.mainloop()
