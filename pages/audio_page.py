import os
import customtkinter as ctk
import yt_dlp
from assets.spinner import LoadingSpinner
import json

from utils.config import get_settings, get_cookie_path

config = get_settings()


class AudioPage:
    def __init__(self, root):
        self.root = root
        self.init_ui()

    def init_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.root, text="Download Audio (MP3)", font=("Arial", 18)).pack(pady=10)

        self.url_entry = ctk.CTkEntry(self.root, width=300, placeholder_text="Enter YouTube URL")
        self.url_entry.pack(pady=10)

        ctk.CTkButton(self.root, text="Download MP3", command=self.download_audio).pack(pady=10)

        self.result_label = ctk.CTkLabel(self.root, text="", wraplength=350)
        self.result_label.pack(pady=10)
        self.spinner = LoadingSpinner(self.root)

        ctk.CTkButton(self.root, text="⬅ Back", command=self.root.home_page).pack(pady=20)

    def download_audio(self):
        url = self.url_entry.get()
        if not url:
            self.result_label.configure(text="Please enter a URL.")
            return
        path = config.get("download_path", "Not Found")
        self.spinner.start()
        self.root.update_idletasks()
        ydl_opts = {
            "cookiefile": "youtube_cookies.txt",
            'ffmpeg_location': 'C:\\ffmpeg\\bin',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),  
            
        }
        try:
            app_dir = os.path.join(os.getenv("APPDATA"), "YouTubeToolkit")
            settings_path = os.path.join(app_dir, "settings.json")
            cookie_path = os.path.join(app_dir, "youtube_cookies.txt")

            if os.path.exists(settings_path):
                with open(settings_path, "r") as f:
                    settings = json.load(f)
                    if settings.get("use_cookies") and os.path.exists(cookie_path):
                        ydl_opts["cookiefile"] = cookie_path
        except Exception as e:
                 print(f"[WARN] Could not apply cookies: {e}")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                self.result_label.configure(text=f"Downloaded: {info['title']}.mp3")
        except yt_dlp.utils.DownloadError as e:
            if "ffmpeg" in str(e).lower():
                pass
            else:
                self.result_label.configure(text=f"Download error: {e}")
        except Exception as e:
            self.result_label.configure(text=f"Unexpected error: {e}")

        finally:
            self.spinner.stop()
