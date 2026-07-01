import tkinter as tk
from tkinter import messagebox
import math
import pygame
import sys

def user_input():
    config = {}

    root = tk.Tk()
    root.title("Pendulum Configurations")
    root.geometry("340x380")
    root.resizable(False, False)
    
    # List of tuples: (Label text, variable key, default value string)
    fields = [
        ("Mass 1 (bob size, try 10):", "mass_1", "10"),
        ("Mass 2 (bob size, try 10):", "mass_2", "10"),
        ("Length 1 (pixels, try 150):", "length_1", "150"),
        ("Length 2 (pixels, try 150):", "length_2", "150"),
        ("Angle 1 (degrees, try 90):", "theta_1", "90"),
        ("Angle 2 (degrees, try 90):", "theta_2", "90"),
        ("Gravity (speed, try 0.6):", "g", "0.6")
    ]
    
    entries = {}
    for label_text, key, default in fields:
        frame = tk.Frame(root, pady=4) 
        frame.pack(fill="x", padx=15) 
        lbl = tk.Label(frame, text=label_text, width=22, anchor="w") 
        lbl.pack(side="left") 
        ent = tk.Entry(frame) 
        ent.insert(0, default) 
        ent.pack(side="right", expand=True, fill="x") 
        entries[key] = ent 

    def submit():
        try:
            config["mass_1"] = float(entries["mass_1"].get())
            config["mass_2"] = float(entries["mass_2"].get())
            config["length_1"] = float(entries["length_1"].get())
            config["length_2"] = float(entries["length_2"].get())
            config["theta_1"] = math.radians(float(entries["theta_1"].get()))
            config["theta_2"] = math.radians(float(entries["theta_2"].get()))
            config["g"] = float(entries["g"].get())
            
            root.destroy()  
        except ValueError:
            messagebox.showerror("Invalid Input", "Please make sure all inputs are valid numbers.")

    btn = tk.Button(root, text="Launch Simulation", command=submit, bg="#0DFF00", fg="black", font=("Arial", 10, "bold"), pady=6)
    btn.pack(pady=20)

    root.mainloop()
    return config

user_settings = user_input()


if not user_settings:
    sys.exit()

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chaotic Double Pendulum Simulation")
clock = pygame.time.Clock()

# Color Palette
background = (248, 249, 250)
line_color = (33, 37, 41)
bob_color_1 = (230, 57, 70)
bob_color_2 = (29, 53, 87)
trace_color = (168, 218, 220)

# The static anchor point for the first pendulum rod
pivot_x = width // 2
pivot_y = 200

# Velocities always start at zero for a pendulum system
omega_1 = 0.0
omega_2 = 0.0

# Map user settings into active state variables
length_1 = user_settings["length_1"]
length_2 = user_settings["length_2"]
mass_1 = user_settings["mass_1"]
mass_2 = user_settings["mass_2"]
theta_1 = user_settings["theta_1"]
theta_2 = user_settings["theta_2"]
g = user_settings["g"]

# Trace line memory bank
path = []
max_path_length = 1500  # determines how long the trace line can be before it starts erasing old points

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    delta = theta_1 - theta_2
    
    # Solve for Angular Acceleration 1
    num1 = -g * (2 * mass_1 + mass_2) * math.sin(theta_1) - mass_2 * g * math.sin(theta_1 - 2 * theta_2)
    num2 = -2 * math.sin(delta) * mass_2 * (omega_2**2 * length_2 + omega_1**2 * length_1 * math.cos(delta))
    den1 = length_1 * (2 * mass_1 + mass_2 - mass_2 * math.cos(2 * theta_1 - 2 * theta_2))
    alpha_1 = (num1 + num2) / den1

    # Solve for Angular Acceleration 2
    num3 = 2 * math.sin(delta) * (omega_1**2 * length_1 * (mass_1 + mass_2) + g * (mass_1 + mass_2) * math.cos(theta_1) + omega_2**2 * length_2 * mass_2 * math.cos(delta))
    den2 = length_2 * (2 * mass_1 + mass_2 - mass_2 * math.cos(2 * theta_1 - 2 * theta_2))
    alpha_2 = num3 / den2

    # Numerical Integration step updates
    omega_1 += alpha_1
    omega_2 += alpha_2
    theta_1 += omega_1
    theta_2 += omega_2

    # Angles to Screen Coordinates
    x1 = pivot_x + length_1 * math.sin(theta_1)
    y1 = pivot_y + length_1 * math.cos(theta_1)

    x2 = x1 + length_2 * math.sin(theta_2)
    y2 = y1 + length_2 * math.cos(theta_2)

    # Update the trace path
    path.append((int(x2), int(y2)))
    if len(path) > max_path_length:
        path.pop(0)

    screen.fill(background)

    if len(path) > 1:
        pygame.draw.lines(screen, trace_color, False, path, 2)

    pygame.draw.line(screen, line_color, (pivot_x, pivot_y), (int(x1), int(y1)), 4)
    pygame.draw.line(screen, line_color, (int(x1), int(y1)), (int(x2), int(y2)), 4)

    pygame.draw.circle(screen, bob_color_1, (int(x1), int(y1)), int(max(5, mass_1 + 5)))
    pygame.draw.circle(screen, bob_color_2, (int(x2), int(y2)), int(max(5, mass_2 + 5)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()