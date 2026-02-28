# ShapeUI.py
import tkinter as tk
from tkinter import ttk, simpledialog
from splitter import ShapeDataStructure
import Surrounding_Materials
import Sink_Materials

class ShapeUI:
    def __init__(self):
        # ---------------- ROOT & USER INPUT ----------------
        self.root = tk.Tk()
        self.root.withdraw()  # hide until dialogs

        # Ask for grid size
        self.width = simpledialog.askinteger("Grid Width", "Enter X size:", minvalue=5, maxvalue=100)
        self.height = simpledialog.askinteger("Grid Height", "Enter Y size:", minvalue=5, maxvalue=100)
        self.resolution = 1
        self.cell_size = 25  # initial cell size

        # ---------------- SCALE TO SCREEN ----------------
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        max_width = int(screen_width * 0.7)
        max_height = int(screen_height * 0.8)

        scale_x = max_width / (self.width * self.cell_size)
        scale_y = max_height / (self.height * self.cell_size)
        self.scale = min(scale_x, scale_y, 1)
        self.cell_size = max(int(self.cell_size * self.scale), 1)

        canvas_width = self.width * self.cell_size
        canvas_height = self.height * self.cell_size

        # ---------------- INITIALIZE SHAPE ----------------
        self.shape = ShapeDataStructure(self.width, self.height, self.resolution)

        # ---------------- MAIN WINDOW ----------------
        self.root.deiconify()
        self.root.title("Heat Source Integration Tool")
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # ---------------- LEFT HEAT SOURCE SIDEBAR ----------------
        self.left_frame = tk.Frame(self.main_frame, width=50, bg="white")
        self.left_frame.pack(side="left", fill="y")
        self.heat_canvas = tk.Canvas(self.left_frame, width=50, height=canvas_height, bg="white")
        self.heat_canvas.pack(fill="y", expand=True)

        # ---------------- CANVAS ----------------
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side="left", fill="both", expand=True)
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

    # ---------------- CONTROL PANEL ----------------
    def _build_controls(self):
        # ---------------- CUSTOM MATERIAL ENTRIES ----------------
        tk.Label(self.control_frame, text="Custom k (Sink)", font=("Arial", 10)).pack(anchor="w")
        self.sink_custom_entry = tk.Entry(self.control_frame)
        self.sink_custom_entry.pack(fill="x", pady=(0,5))
        tk.Label(self.control_frame, text="Custom h (Surround)", font=("Arial", 10)).pack(anchor="w")
        self.surround_custom_entry = tk.Entry(self.control_frame)
        self.surround_custom_entry.pack(fill="x", pady=(0,5))

        # ---------------- MATERIAL DROPDOWNS ----------------
        tk.Label(self.control_frame, text="Sink Material", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10,0))
        self.sink_material_var = tk.StringVar(value="Steel")
        self.sink_material_dropdown = ttk.Combobox(
            self.control_frame,
            textvariable=self.sink_material_var,
            values=list(Sink_Materials.keys()) + ["Custom"]
        )
        self.sink_material_dropdown.pack(fill="x", pady=5)

        tk.Label(self.control_frame, text="Surrounding Material", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10,0))
        self.surround_material_var = tk.StringVar(value="Air")
        self.surround_material_dropdown = ttk.Combobox(
            self.control_frame,
            textvariable=self.surround_material_var,
            values=list(Surrounding_Materials.keys()) + ["Custom"]
        )
        self.surround_material_dropdown.pack(fill="x", pady=5)

        # ---------------- TEMPERATURES ----------------
        tk.Label(self.control_frame, text="Heat Source Temp (°C)", font=("Arial", 12, "bold")).pack(anchor="w", pady=(15,0))
        self.heat_temp_var = tk.StringVar(value="100")
        self.heat_temp_entry = tk.Entry(self.control_frame, textvariable=self.heat_temp_var)
        self.heat_temp_entry.pack(fill="x", pady=5)

        tk.Label(self.control_frame, text="Ambient Temp (°C)", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10,0))
        self.ambient_temp_var = tk.StringVar(value="25")
        self.ambient_temp_entry = tk.Entry(self.control_frame, textvariable=self.ambient_temp_var)
        self.ambient_temp_entry.pack(fill="x", pady=5)

        # ---------------- BUTTONS ----------------
        tk.Button(self.control_frame, text="Clear", command=self.clear).pack(fill="x", pady=(15, 5))
        tk.Button(self.control_frame, text="Run Physics", command=self.run_physics).pack(fill="x", pady=(5, 15))

        # Heatmap legend
        self.legend_canvas = tk.Canvas(self.control_frame, width=50, height=200)
        self.legend_canvas.pack()
        self.status_label = tk.Label(self.control_frame, text="", fg="gray")
        self.status_label.pack(pady=10)

    # ---------------- EVENTS ----------------
    def _bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_motion)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    # ---------------- DRAWING ----------------
    def start_draw(self, event):
        x = event.x // self.cell_size
        y = self.height - 1 - event.y // self.cell_size

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
        self._draw_heat_source_line()

    def add_point_from_event(self, event):
        canvas_x = event.x // self.cell_size
        canvas_y = event.y // self.cell_size
        x = canvas_x
        y = self.height - 1 - canvas_y

        if (x, y) not in self.drawn_coordinates:
            self.drawn_coordinates.append((x, y))
            self._draw_cell(x, y, "black")

    # ---------------- INTEGRATION ----------------
    def integrate_shape(self):
        if not self.drawn_coordinates:
            return

        try:
            heat_temp = float(self.heat_temp_var.get())
            ambient_temp = float(self.ambient_temp_var.get())
        except ValueError:
            self.status_label.config(text="Invalid temperature", fg="red")
            return

        # Determine material k/h
        sink_k = Sink_MaterialsS.get(self.sink_material_var.get())
        if self.sink_material_var.get() == "Custom":
            try:
                sink_k = float(self.sink_custom_entry.get())
            except ValueError:
                self.status_label.config(text="Invalid k value", fg="red")
                return

        surround_h = Surrounding_Materials.get(self.surround_material_var.get())
        if self.surround_material_var.get() == "Custom":
            try:
                surround_h = float(self.surround_custom_entry.get())
            except ValueError:
                self.status_label.config(text="Invalid h value", fg="red")
                return

        # Call existing integration
        self.shape.integrate_under_line(
            self.drawn_coordinates,
            material=self.sink_material_var.get(),
            temperature=heat_temp
        )

        self._render_uniform()
        self.status_label.config(text=f"{len(self.shape.drawn_points)} points integrated", fg="black")

    # ---------------- HEAT SOURCE LINE ----------------
    def _draw_heat_source_line(self):
        if not self.shape.drawn_points:
            return
        min_y = min(p.y for p in self.shape.drawn_points)
        max_y = max(p.y for p in self.shape.drawn_points)

        for y in range(min_y, max_y + 1):
            self._draw_heat_cell(0, y, "red")

    def _draw_heat_cell(self, x, y, color):
        canvas_y = self.height - 1 - y
        x1 = 0
        y1 = canvas_y * self.cell_size
        x2 = self.cell_size
        y2 = y1 + self.cell_size
        self.heat_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    # ---------------- PHYSICS ----------------
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

    # ---------------- RENDERING ----------------
    def _draw_cell(self, x, y, color):
        canvas_y = self.height - 1 - y
        x1 = x * self.cell_size
        y1 = canvas_y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def _draw_grid(self):
        for x in range(self.width):
            for y in range(self.height):
                self._draw_cell(x, y, "white")

    def _highlight_start_cell(self):
        self._draw_cell(0, 0, "#90ee90")

    def _flash_cell(self, x, y, color):
        self._draw_cell(x, y, color)
        self.root.after(300, lambda: self._draw_cell(x, y, "#90ee90"))

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
        ratio = (temp - t_min) / (t_max - t_min) if t_max != t_min else 0
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
            self.legend_canvas.create_rectangle(0, height-i, 50, height-i-1, fill=color, outline="")

        temps = [p.attributes['temperature'] for p in self.shape.drawn_points]
        t_min = min(temps)
        t_max = max(temps)
        self.legend_canvas.create_text(25, 10, text=f"{t_max:.1f}", fill="black")
        self.legend_canvas.create_text(25, 190, text=f"{t_min:.1f}", fill="black")

    # ---------------- CLEAR ----------------
    def clear(self):
        self.shape.clear_shape()
        self.drawn_coordinates = []
        self.canvas.delete("all")
        self.heat_canvas.delete("all")
        self.legend_canvas.delete("all")
        self.must_start = True
        self._draw_grid()
        self._highlight_start_cell()
        self.status_label.config(text="Start drawing at (0,0)", fg="blue")