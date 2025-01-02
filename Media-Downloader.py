import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os

def download_content():
    url = url_entry.get().strip()
    download_type = download_type_var.get()
    playlist_handling = playlist_handling_var.get()
    output_folder = output_folder_entry.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    if not (url.startswith("http://") or url.startswith("https://")):
        messagebox.showerror("Error", "Invalid URL. Please enter a valid URL starting with http:// or https://.")
        return

    if not output_folder:
        output_folder = os.getcwd()

    progress_bar["value"] = 0  # Reset progress bar

    # Define yt-dlp options
    ydl_opts = {
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'noplaylist': (playlist_handling == "noplaylist"),
        'progress_hooks': [progress_hook],  # Add the progress hook
    }

    if download_type == "Audio":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    elif download_type == "Video":
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", f"Download completed for: {url}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download: {str(e)}")


def progress_hook(d):
    """Update the progress bar based on download status."""
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 1)  # Avoid division by zero
        percent = (downloaded / total) * 100
        progress_bar["value"] = percent
        app.update_idletasks()  # Refresh the GUI


def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, folder_selected)

# Create the main application window
app = tk.Tk()
app.title("Multi-Platform Downloader")

# URL Input
tk.Label(app, text="Enter URL:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
url_entry = tk.Entry(app, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Output Folder
tk.Label(app, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
output_folder_entry = tk.Entry(app, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=10)
browse_button = tk.Button(app, text="Browse", command=browse_folder)
browse_button.grid(row=1, column=2, padx=10, pady=10)

# Download Type
tk.Label(app, text="Download Type:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
download_type_var = tk.StringVar(value="Default")
tk.Radiobutton(app, text="Default", variable=download_type_var, value="Default").grid(row=2, column=1, sticky=tk.W)
tk.Radiobutton(app, text="Video", variable=download_type_var, value="Video").grid(row=2, column=1, padx=90, sticky=tk.W)
tk.Radiobutton(app, text="Audio", variable=download_type_var, value="Audio").grid(row=2, column=1, padx=180, sticky=tk.W)

# Playlist Handling
tk.Label(app, text="Playlist Handling:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
playlist_handling_var = tk.StringVar(value="noplaylist")
tk.Radiobutton(app, text="Single Video", variable=playlist_handling_var, value="noplaylist").grid(row=3, column=1, sticky=tk.W)
tk.Radiobutton(app, text="Entire Playlist", variable=playlist_handling_var, value="playlist").grid(row=3, column=1, padx=150, sticky=tk.W)

# Progress Bar
progress_bar = ttk.Progressbar(app, orient="horizontal", mode="determinate", length=300)
progress_bar.grid(row=4, column=0, columnspan=3, pady=20)

# Download Button
download_button = tk.Button(app, text="Download", command=download_content)
download_button.grid(row=5, column=0, columnspan=3, pady=20)

# Run the application
app.mainloop()
