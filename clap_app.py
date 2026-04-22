import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import numpy as np
import threading
import webbrowser
import time

# Global variables
listening = False
threshold = 68.0  # New default on a 0-100 scale
last_clap_time = 15
cooldown = 10.0 

# Modern Color Palette
BG_COLOR = "#0A0F1E"      # Darker Navy
CARD_COLOR = "#161E2E"    # Deep Slate
ACCENT_COLOR = "#0EA5E9"  # Vibrant Sky Blue
SUCCESS_COLOR = "#10B981" # Emerald
ERROR_COLOR = "#F43F5E"   # Rose
TEXT_COLOR = "#F1F5F9"    # Slate 100

def detect_clap(indata, frames, time_info, status):
    global last_clap_time, threshold
    if not listening:
        return

    # Use Peak Amplitude for more precise 'spike' detection
    # This is more resilient than linalg.norm for claps
    peak = np.max(np.abs(indata)) * 100
    
    # Update volume meter
    try:
        root.after(0, lambda: update_volume_meter(peak))
    except:
        pass

    if peak > threshold:
        current_time = time.time()
        if current_time - last_clap_time > cooldown:
            last_clap_time = current_time
            try:
                root.after(0, trigger_action)
            except:
                pass

def trigger_action():
    status_label.config(text="👏 Clap Recognized!", fg=SUCCESS_COLOR)
    # Visual feedback on the volume bar
    volume_canvas.itemconfig(volume_bar, fill=SUCCESS_COLOR)
    open_youtube()
    root.after(2000, lambda: status_label.config(text="Listening...", fg=ACCENT_COLOR))

def update_volume_meter(val):
    # Map 0-100 value to 0-300 pixel width
    width = min(300, val * 3)
    volume_canvas.coords(volume_bar, 0, 0, width, 40)
    
    # Dynamic coloring
    if val > threshold:
        volume_canvas.itemconfig(volume_bar, fill=ERROR_COLOR)
    else:
        volume_canvas.itemconfig(volume_bar, fill=ACCENT_COLOR)

def open_youtube():
    try:
        brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        webbrowser.get(f'"{brave_path}" %s').open("https://www.youtube.com")
    except:
        webbrowser.open("https://www.youtube.com")

def toggle_listening():
    global listening
    if not listening:
        start_listening()
    else:
        stop_listening()

def start_listening():
    global listening
    listening = True
    status_label.config(text="Listening...", fg=ACCENT_COLOR)
    toggle_btn.config(text="Stop System", bg=ERROR_COLOR)
    
    def listen():
        try:
            # increased blocksize for stability
            with sd.InputStream(callback=detect_clap, blocksize=1024):
                while listening:
                    time.sleep(0.1)
        except Exception as e:
            root.after(0, lambda: status_label.config(text="Mic Error", fg=ERROR_COLOR))

    threading.Thread(target=listen, daemon=True).start()

def stop_listening():
    global listening
    listening = False
    status_label.config(text="System Inactive", fg="#475569")
    toggle_btn.config(text="Start System", bg=SUCCESS_COLOR)
    update_volume_meter(0)

def update_threshold(val):
    global threshold
    threshold = float(val)
    threshold_label.config(text=f"Trigger Sensitivity: {threshold:.0f}%")

# UI setup
root = tk.Tk()
root.title("Aura Clap v2")
root.geometry("400x520")
root.configure(bg=BG_COLOR)

# Header
tk.Label(root, text="AURA", font=("Arial", 28, "bold"), bg=BG_COLOR, fg=ACCENT_COLOR).pack(pady=(40, 0))
tk.Label(root, text="CLAP CONTROL", font=("Arial", 10, "bold"), bg=BG_COLOR, fg="#475569").pack(pady=(0, 20))

# Status Display
status_label = tk.Label(root, text="System Inactive", font=("Arial", 14), bg=BG_COLOR, fg="#475569")
status_label.pack(pady=10)

# Main Interaction Area
container = tk.Frame(root, bg=CARD_COLOR, padx=30, pady=30, highlightthickness=1, highlightbackground="#1E293B")
container.pack(fill="x", padx=40)

# Volume Visualization
tk.Label(container, text="INPUT LEVEL", font=("Arial", 8, "bold"), bg=CARD_COLOR, fg="#64748B").pack(anchor="w")
volume_bg = tk.Frame(container, height=40, bg=BG_COLOR)
volume_bg.pack(fill="x", pady=(5, 20))
volume_canvas = tk.Canvas(volume_bg, height=40, bg=BG_COLOR, highlightthickness=0)
volume_canvas.pack(fill="x")
volume_bar = volume_canvas.create_rectangle(0, 0, 0, 40, fill=ACCENT_COLOR, outline="")

# Toggle Button
toggle_btn = tk.Button(container, text="Start System", font=("Arial", 11, "bold"),
                       command=toggle_listening, bg=SUCCESS_COLOR, fg="white",
                       relief="flat", pady=12, cursor="hand2", activebackground="#059669")
toggle_btn.pack(fill="x")

# Threshold Slider
slider_label_frame = tk.Frame(root, bg=BG_COLOR)
slider_label_frame.pack(fill="x", padx=40, pady=(30, 0))

threshold_label = tk.Label(slider_label_frame, text=f"Trigger Sensitivity: {threshold:.0f}%", 
                           font=("Arial", 10), bg=BG_COLOR, fg=TEXT_COLOR)
threshold_label.pack(side="left")

threshold_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", 
                            command=update_threshold, bg=BG_COLOR, fg=TEXT_COLOR,
                            highlightthickness=0, troughcolor=CARD_COLOR, 
                            activebackground=ACCENT_COLOR, length=320, showvalue=False)
threshold_slider.set(threshold)
threshold_slider.pack(pady=10)

tk.Label(root, text="Brave Browser Integration Active", font=("Arial", 8),
         bg=BG_COLOR, fg="#334155").pack(side="bottom", pady=20)

root.mainloop()
