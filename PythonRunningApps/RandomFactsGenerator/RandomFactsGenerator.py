from tkinter import *
from tkinter import ttk
import ctypes
from ctypes import wintypes
import requests
import webbrowser
import os

# Define the path where you want to save fact.txt
FACT_FILE_PATH = r"C:\Users\gaura\Desktop\PythonRunningApps\RandomFactsGenerator\fact.txt"

def apply_rounded_corners(root, radius):
    HRGN = ctypes.c_void_p
    hWnd = ctypes.wintypes.HWND(int(root.frame(), 16))
    hRgn = ctypes.windll.gdi32.CreateRoundRectRgn(0, 0, root.winfo_width(), root.winfo_height(), radius, radius)
    ctypes.windll.user32.SetWindowRgn(hWnd, hRgn, True)

def count_saved_facts():
    try:
        with open(FACT_FILE_PATH, "r") as file:
            return len(file.readlines())
    except FileNotFoundError:
        return 0  # Return 0 if the file doesn't exist yet

def update_ui_elements():
    update_coordinates()
    update_fact_count()

def update_fact_count():
    num_facts = count_saved_facts()
    fact_count_label.config(text=f"Number of Saved Facts: {num_facts}")

def open_github(event=None):
    webbrowser.open('https://github.com/LordGauravB')

def on_press(event):
    global x_window, y_window
    x_window = event.x
    y_window = event.y

def update_coordinates():
    x, y = root.winfo_x(), root.winfo_y()
    coordinate_label.config(text=f"Coordinates: {x}, {y}")

def on_drag(event):
    x = event.x_root - x_window
    y = event.y_root - y_window
    root.geometry(f"+{x}+{y}")
    update_coordinates()

def set_static_position(event=None):
    x, y = -407, 7
    root.geometry(f"+{x}+{y}")
    update_coordinates()

def open_fact_file(event=None):
    if os.path.exists(FACT_FILE_PATH):
        webbrowser.open(FACT_FILE_PATH)
    else:
        save_status_label.config(text="Fact file not found.", fg="#ff0000")

def fetch_random_fact():
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en", timeout=10)
        if response.status_code == 200:
            fact = response.json()['text']
            if len(fact.split()) <= 15:
                return fact
            else:
                return None
        else:
            return "Failed to fetch a random fact"
    except requests.RequestException as e:
        return f"Error: {str(e)}"

def adjust_font_size(text):
    words_count = len(text.split())
    return 13

def generate_new_fact():
    global fact_saved
    fact_saved = False  # Reset the fact_saved flag
    new_fact_text = None
    save_button.config(bg='#808080', state='disabled')  # Disable save button at the start

    while new_fact_text is None:
        new_fact_text = fetch_random_fact()
        if new_fact_text is None or isinstance(new_fact_text, Exception):
            save_status_label.config(text="Failed to fetch a new fact", fg="#ff0000")
            return  # Maintain the button disabled if no new fact is fetched

    if new_fact_text:
        fact_label.config(text=new_fact_text)
        fact_font_size = adjust_font_size(new_fact_text)
        fact_label.config(font=("Trebuchet MS", fact_font_size))
        fade_out_saved_message()  # Clear the saved status message
        save_button.config(bg='#007bff', state='normal')  # Re-enable the save button

    update_save_button()

def fade_out_saved_message():
    save_status_label.config(text="", fg="#1e1e1e")  # Clear any previous save status messages

def save_fact_to_file():
    global fact_saved
    if not fact_saved:
        fact_text = fact_label.cget("text")
        try:
            with open(FACT_FILE_PATH, "r") as file:
                existing_facts = file.readlines()
            # Check if the current fact is in the list of existing facts
            if any(fact_text.strip() + '\n' == existing_fact for existing_fact in existing_facts):
                save_status_label.config(text="Fact already saved.", fg="#ff0000")
                return
        except FileNotFoundError:
            # If the file doesn't exist, continue to create it below
            pass

        with open(FACT_FILE_PATH, "a") as file:
            file.write(fact_text + '\n')
        save_status_label.config(text="Fact Saved!", fg="#b66d20")
        fact_saved = True
        update_save_button()
        update_fact_count()  # Update the fact count after saving
    else:
        save_status_label.config(text="Fact already saved.", fg="#ff0000")

def update_save_button():
    if fact_saved or fact_label.cget("text") == "Welcome to Fact Generator!":
        save_button.config(bg='#808080', state='disabled')
    else:
        save_button.config(bg='#007bff', state='normal')

root = Tk()
root.geometry("400x250")
root.overrideredirect(True)
root.configure(bg='#1e1e1e')

fact_saved = False

title_bar = Frame(root, bg='#000000', height=30, relief='raised')
title_bar.pack(side="top", fill="x")
title_bar.bind("<Button-1>", on_press)
title_bar.bind("<B1-Motion>", on_drag)

title_label = Label(title_bar, text="Facts", fg="white", bg='#030303', font=("Trebuchet MS", 12, 'bold'))
title_label.pack(side="top", fill="x", pady=5)

fact_frame = Frame(root, bg="#1e1e1e")
fact_frame.pack(side="top", fill="both", expand=True)

fact_text = fetch_random_fact() or "Welcome to Fact Generator!"
fact_font_size = adjust_font_size(fact_text)
fact_label = Label(fact_frame, text=fact_text, fg="white", bg="#1e1e1e", font=("Trebuchet MS", fact_font_size), wraplength=350)
fact_label.pack(side="top", fill="both", expand=True)

root.update_idletasks()
apply_rounded_corners(root, 15)
root.attributes('-alpha', 0.65)

bottom_frame = Frame(root, bg="#1e1e1e")
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=5)

credit_label = Label(bottom_frame, text="       Created by - Gaurav Bhandari", fg="white", bg="#1e1e1e", cursor="hand2", font=("Trebuchet MS", 7))
credit_label.pack(side="right")
credit_label.bind("<Button-1>", open_github)

coordinate_label = Label(bottom_frame, text="Coordinates: ", fg="white", bg="#1e1e1e", font=("Trebuchet MS", 7))
coordinate_label.pack(side="right")

fact_count_label = Label(bottom_frame, text="Number of Saved Facts: 0", fg="white", bg="#1e1e1e", cursor="hand2", font=("Trebuchet MS", 7))
fact_count_label.pack(side="left")
fact_count_label.bind("<Button-1>", open_fact_file)

root.update_idletasks()
update_ui_elements()

control_frame = Frame(root, bg="#1e1e1e")
control_frame.pack(side="bottom", fill="x")

set_static_position()
root.bind("<s>", set_static_position)

generate_button = Button(control_frame, text="Generate Fact", bg='#b66d20', fg="white", command=generate_new_fact, cursor="hand2", borderwidth=0, highlightthickness=0, padx=10, pady=5)
generate_button.pack(side="left", padx=10, pady=0.5)

save_button = Button(control_frame, text="Save Fact", bg='#007bff', fg="white", command=save_fact_to_file, cursor="hand2", borderwidth=0, highlightthickness=0, padx=10, pady=5)
save_button.pack(side="right", padx=10, pady=0.5)

save_status_label = Label(control_frame, text="", fg="#b66d20", bg="#1e1e1e", font=("Trebuchet MS", 10))
save_status_label.pack(side="bottom", fill="x")

root.mainloop()
