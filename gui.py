import tkinter as tk
from tkinter import ttk
from warehouse import Warehouse
from robot import Robot
from PIL import Image, ImageTk  # For images; install pillow with `pip install pillow`

CELL_SIZE = 60
GRID_WIDTH = 5
GRID_HEIGHT = 5

class WarehouseGUI(tk.Tk):
    def __init__(self, warehouse):
        super().__init__()
        self.title("Warehouse Simulation")
        self.warehouse = warehouse

        self.speed_ms = 1000  # Update every 1000ms initially
        self.running = False

        # Canvas for drawing grid
        self.canvas = tk.Canvas(self, width=CELL_SIZE * GRID_WIDTH, height=CELL_SIZE * GRID_HEIGHT)
        self.canvas.grid(row=0, column=0, columnspan=3)

        # Start/Pause buttons
        self.start_btn = ttk.Button(self, text="Start", command=self.start_simulation)
        self.start_btn.grid(row=1, column=0, sticky="ew")

        self.pause_btn = ttk.Button(self, text="Pause", command=self.pause_simulation, state="disabled")
        self.pause_btn.grid(row=1, column=1, sticky="ew")

        # Speed control slider
        self.speed_slider = ttk.Scale(self, from_=100, to=2000, orient='horizontal', command=self.change_speed)
        self.speed_slider.set(self.speed_ms)
        self.speed_slider.grid(row=1, column=2, sticky="ew")
        self.speed_label = ttk.Label(self, text="Speed (ms)")
        self.speed_label.grid(row=2, column=2)

        # Status message box
        self.status_text = tk.Text(self, height=6, width=50, state='disabled', bg="#f0f0f0")
        self.status_text.grid(row=3, column=0, columnspan=3, pady=10)

        # Load images for robots and boxes
        # Load and resize images
        self.robot_img = ImageTk.PhotoImage(Image.open("robot.png").resize((40, 40)))
        self.box_img = ImageTk.PhotoImage(Image.open("box.png").resize((40, 40)))

        self.update_loop()

    def log_status(self, message):
        self.status_text['state'] = 'normal'
        self.status_text.insert('end', message + '\n')
        self.status_text.see('end')  # Scroll to end
        self.status_text['state'] = 'disabled'

    def start_simulation(self):
        self.running = True
        self.start_btn['state'] = 'disabled'
        self.pause_btn['state'] = 'normal'
        self.log_status("Simulation started.")

    def pause_simulation(self):
        self.running = False
        self.start_btn['state'] = 'normal'
        self.pause_btn['state'] = 'disabled'
        self.log_status("Simulation paused.")

    def change_speed(self, val):
        self.speed_ms = int(float(val))
        self.log_status(f"Speed changed to {self.speed_ms} ms per update.")

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(self.warehouse.height):
            for x in range(self.warehouse.width):
                x1, y1 = x * CELL_SIZE, y * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

                # Draw empty cell background
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

                # Draw box image if present
                if self.warehouse.grid[y][x] is not None:
                    self.canvas.create_image(x1 + CELL_SIZE//2, y1 + CELL_SIZE//2, image=self.box_img)

        # Draw robots
        for robot in self.warehouse.robots:
            # Smooth transition
            dx = robot.x - robot.visual_x
            dy = robot.y - robot.visual_y

            speed = 0.2  # lower = slower, higher = faster

            if abs(dx) > 0.01 or abs(dy) > 0.01:
                robot.visual_x += dx * speed
                robot.visual_y += dy * speed
            else:
                robot.visual_x = robot.x
                robot.visual_y = robot.y
            x1, y1 = robot.x * CELL_SIZE, robot.y * CELL_SIZE
            color = "green" if not robot.carrying else "red"  # Green normal, red if carrying
            # Instead of circles, use robot image with a color tint (for demo just place image)
            self.canvas.create_image(x1 + CELL_SIZE//2, y1 + CELL_SIZE//2, image=self.robot_img)
            # Draw a small circle colored to show carrying state
            radius = 8
            cx, cy = x1 + CELL_SIZE - 15, y1 + 15
            self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill=color, outline='black')
            self.canvas.create_text(x1 + CELL_SIZE / 2, y1 + CELL_SIZE / 2, text=robot.name[0], fill="white", font=("Arial", 20, "bold"))
            # Convert float position to pixel center
            px = robot.visual_x * CELL_SIZE + CELL_SIZE // 2
            py = robot.visual_y * CELL_SIZE + CELL_SIZE // 2

            # Draw robot image
            # Draw robot image
            self.canvas.create_image(px, py, image=self.robot_img)

            # Draw robot's initial letter on top
            self.canvas.create_text(px, py, text=robot.name[0], fill="white", font=("Arial", 20, "bold"))

            # Show 📦 emoji if robot is carrying something
            if robot.carrying:
                self.canvas.create_text(px + 18, py - 18, text="📦", font=("Arial", 14))





    def update_loop(self):
        if self.running:
            for robot in self.warehouse.robots:
                action_message = robot.ai_behavior()
                if action_message:
                    self.log_status(action_message)

            self.draw_grid()

        self.after(self.speed_ms, self.update_loop)

def main():
    w = Warehouse(GRID_WIDTH, GRID_HEIGHT)
    r1 = Robot(w, "Alpha", x=0, y=0)
    r2 = Robot(w, "Beta", x=4, y=4)

    w.place_item(2, 2, 'Box')
    w.place_item(3, 1, 'Box')

    app = WarehouseGUI(w)
    app.mainloop()

if __name__ == "__main__":
    main()
