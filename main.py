import tkinter as tk
import matplotlib
import sys
import os
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from matplotlib.figure import Figure
import numpy as np
import random

_x = []
_y = []


points = [[0, 0], [0, 0], [0, 0]]

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Logo = "favicon.ico"
Logo = resource_path(Logo)

def clicked_generate_button():
    for artist in a.lines + a.collections:
        artist.remove()
    x_coords = []
    x_coord = int(random.random()*18-9)
    for i in range(3):
        while x_coord in x_coords:
            x_coord = int(random.random() * 36 - 18)/2
        x_coords.append(x_coord)
        y = random.random()*18-9
        a.plot(x_coords[i], y, 'ro')
        points[i] = [x_coords[i], y]
    canvas.draw()

def calculate_score():
    score_value = 0
    x_values = np.linspace(-10,10,1000)

    a = float(entry_squared.get())
    b = float(entry_linear.get())
    c = float(entry_constant.get())

    for point in points:
        distance = 10000
        for x in x_values:
            now_distance = np.sqrt((a*x**2+b*x+c - point[1])**2 + (x-point[0])**2)
            if distance > now_distance:
                distance = now_distance
        score_value += distance
    score_value = int(score_value*100)/100
    return score_value

def calculate_ground_truth():
    left_side_equation = np.array([[points[0][0]**2, points[0][0], 1], [points[1][0]**2, points[1][0], 1], [points[2][0]**2, points[2][0], 1]])
    right_side_equation = np.array([points[0][1], points[1][1], points[2][1]])
    x = np.linalg.solve(left_side_equation, right_side_equation)
    return x

def destroy_final_score_window(new_window):
    new_window.destroy()

def play_again(new_window):
    destroy_final_score_window(new_window)
    score.set(0)
    round_counter.set(1)
    clicked_generate_button()

def end_game(new_window):
    destroy_final_score_window(new_window)
    window.destroy()

def create_final_score_window():
    new_window = tk.Toplevel(window)
    # new_window.iconbitmap(Logo)
    new_window.title("Final Score")
    score_supporting_label_final = tk.Label(new_window, text= "Final Score: ")
    score_label_final = tk.Label(new_window, textvariable=score)
    score_supporting_label_final.grid(row=0, column=0, sticky='E')
    score_label_final.grid(row=0, column=1, sticky='W', pady=10, padx=20)

    button_play_again = tk.Button(new_window, text= "Play again", width=10, command=lambda: play_again(new_window))
    button_play_again.grid(row = 1, column=0, padx=5)
    button_quit = tk.Button(new_window, text = "Quit", width=10, command=lambda: end_game(new_window))
    button_quit.grid(row = 1, column=1, pady=10, padx=5)


def destroy_score_window(new_window):
    new_window.destroy()
    if round_counter.get() < 5:
        round_counter.set(round_counter.get() + 1)
        clicked_generate_button()
    else:
        create_final_score_window()


def create_score_window(score_value, parameters):
    new_window = tk.Toplevel(window)
    # new_window.iconbitmap(Logo)
    new_window.title("Score")
    score_supporting_label_new = tk.Label(new_window, text="You scored: " + str(score_value))
    score_supporting_label_new.pack()
    ground_truth_label = tk.Label(new_window, text="Correct parameters: ")
    ground_truth_label.pack()
    parameters_label = tk.Label(new_window, text= "a = " + str(parameters[0]) + ", b = " + str(parameters[1]) + ", c = " + str(parameters[2]))
    parameters_label.pack()
    button_ok = tk.Button(new_window, text = "Ok", command=lambda: destroy_score_window(new_window))
    button_ok.pack()

def animate_cool_line(i):
    x_aktuell = -10+i*20/50
    _x.append(x_aktuell)
    if i>2:
        _x.pop(0)
    y = float(entry_squared.get()) * x_aktuell**2 + float(entry_linear.get()) * x_aktuell + float(entry_constant.get())
    _y.append(y)
    if i > 2:
        _y.pop(0)
    a.plot(_x, _y, 'b')

def draw_ground_truth(parameters):
    x = np.linspace(-10, 10, 1000)
    y = parameters[0] * x**2 + parameters[1] * x +parameters[2]
    a.plot(x, y, 'r')

def clicked_guess_button():
    global _x, _y
    _x = []
    _y = []

    ani = animation.FuncAnimation(fig=canvas.figure, func=animate_cool_line, interval=1, frames=50, repeat=False)
    canvas.draw()

    score_value = calculate_score()
    parameters = calculate_ground_truth()

    draw_ground_truth(parameters)
    create_score_window(score_value, parameters)

    score_value += int(float(score.get()) * 100)/100
    score.set(score_value)


# TODO: implement multi-round with quit, interesting statistics? Ground-truth-solution?

window = tk.Tk()
# window.iconbitmap(Logo)

score = tk.DoubleVar(value = 0.00)
round_counter = tk.IntVar(window, 1)

window.title("ParabolaGuesser")

fig = Figure(figsize=(5, 5))
a = fig.add_subplot(111)
major_ticks = np.arange(-10, 10.1, 1)
# minor_ticks = np.arange(-10, 10.1, 0.1)
a.set_xticks(major_ticks)
a.set_yticks(major_ticks)
a.set_xlim([-10, 10])
a.set_ylim([-10, 10])
a.grid(which='major', alpha = 1, color='black', linestyle='--', linewidth=0.3)

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(row=0, sticky='N', columnspan=10)
canvas.draw()

clicked_generate_button()

# button_generate = tk.Button(window, text = "Generate new random set of points", width=40, height=2, command=clicked_generate_button)
# button_generate.grid(sticky='W', row=1, column=0, columnspan=4)

round_supporting_label = tk.Label(window, text="Round: ")
round_label = tk.Label(window, textvariable=round_counter)
round_supporting_label_2 = tk.Label(window, text="/ 5")
round_supporting_label.grid(row=1, column=2, sticky='E')
round_label.grid(row=1, column=3, sticky='E')
round_supporting_label_2.grid(row=1, column=4, sticky='W')

score_supporting_label = tk.Label(window, text="Score: ")
score_label = tk.Label(window, textvariable=score)
score_supporting_label.grid(row=1, column=5, sticky='E')
score_label.grid(row=1, column=6, sticky='W', pady=5)

entry_squared = tk.Entry(window)
entry_squared.insert(0, "0")
entry_linear = tk.Entry(window)
entry_linear.insert(0, "0")
entry_constant = tk.Entry(window)
entry_constant.insert(0, "0")

formula_label = tk.Label(window, text = "f(x) = a * x^2 + b * x + c")
formula_label.grid(row=2, columnspan=10, pady = 5)

squared_label = tk.Label(window, text = "a: ")
squared_label.grid(row=3, column = 0, pady = 5)
entry_squared.grid(row=3, column = 1)

linear_label = tk.Label(window, text = "b: ")
linear_label.grid(row=3, column = 2)
entry_linear.grid(row=3, column = 3, columnspan=2)

constant_label = tk.Label(window, text = "c: ")
constant_label.grid(row=3, column = 5)
entry_constant.grid(row=3, column = 6, columnspan=2)

button_guess = tk.Button(window, text="Guess using these parameters", command=clicked_guess_button)
button_guess.grid(row=4, columnspan = 10, pady = 5)

# ani = animation.FuncAnimation(fig=fig, func=animate_cool_line, interval=10, frames=1000)

window.mainloop()