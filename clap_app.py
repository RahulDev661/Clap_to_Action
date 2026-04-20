import tkinter as tk
import sounddevice as sd
import numpy as np
import threading
import webbrowser

# Global variables
listening = False
threshold = 0.6

# Clap detection
def detect_clap(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10

    if volume_norm > threshold:
        status_label.config(text="👏 Clap Detected!", fg="green")
        open_youtube()

# Open YouTube in Brave
def open_youtube():
    try:
        webbrowser.get(
            '"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe" %s'
        ).open("https://www.youtube.com")
    except:
        status_label.config(text="❌ Brave path error", fg="red")

# Start listening
def start_listening():
    global listening
    listening = True
    status_label.config(text="Listening...", fg="blue")

    def listen():
        with sd.InputStream(callback=detect_clap):
            while listening:
                pass

    threading.Thread(target=listen, daemon=True).start()

# Stop listening
def stop_listening():
    global listening
    listening = False
    status_label.config(text="Stopped", fg="red")

# Update sensitivity
def update_threshold(val):
    global threshold
    threshold = float(val)
    threshold_label.config(text=f"Sensitivity: {threshold:.2f}")

# UI setup
root = tk.Tk()
root.title("Clap to Open YouTube (Brave)")
root.geometry("400x300")
root.configure(bg="#1e1e1e")

title = tk.Label(root, text="🎤 Clap Controller", font=("Arial", 16, "bold"),
                 bg="#1e1e1e", fg="white")
title.pack(pady=10)

status_label = tk.Label(root, text="Idle", font=("Arial", 12),
                        bg="#1e1e1e", fg="yellow")
status_label.pack(pady=5)

start_btn = tk.Button(root, text="Start Listening",
                      command=start_listening, bg="green",
                      fg="white", width=15)
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="Stop",
                     command=stop_listening, bg="red",
                     fg="white", width=15)
stop_btn.pack(pady=5)

threshold_slider = tk.Scale(root, from_=0.1, to=2.0, resolution=0.1,
                            orient="horizontal", command=update_threshold,
                            bg="#1e1e1e", fg="white", length=250)
threshold_slider.set(0.6)
threshold_slider.pack(pady=10)

threshold_label = tk.Label(root, text="Sensitivity: 0.6",
                           bg="#1e1e1e", fg="white")
threshold_label.pack()

root.mainloop()