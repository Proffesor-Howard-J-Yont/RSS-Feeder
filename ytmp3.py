import os
import re
import subprocess
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk

# Function to sanitize filenames
def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '', title).replace(' ', '_')

# Function to download and convert to MP3
def download_and_convert():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    try:
        # Download audio using yt-dlp
        safe_title = sanitize_filename("youtube_audio")
        mp3_filename = f"{safe_title}.mp3"
        subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", "-o", mp3_filename, url])

        messagebox.showinfo("Success", f"MP3 saved as: {mp3_filename}")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# GUI setup
root = ttk.Window(themename="darkly")
root.title("YouTube to MP3 Converter")
root.geometry("400x200")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Enter YouTube URL:", font=("Arial", 12)).pack(pady=5)
url_entry = ttk.Entry(frame, width=40)
url_entry.pack(pady=5)

download_btn = ttk.Button(frame, text="Download & Convert", command=download_and_convert, bootstyle="success")
download_btn.pack(pady=10)

root.mainloop()