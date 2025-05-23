import customtkinter as ctk
import yt_dlp
from utils.logger import log_download
import os
import json
from assets.spinner import LoadingSpinner

from utils.config import get_settings, get_cookie_path

config = get_settings()


class VideoPage:
    def __init__(self, root):
        self.root = root
        self.init_ui()

    def init_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.root, text="Download YouTube Video", font=("Arial", 18)).pack(pady=10)

        self.url_entry = ctk.CTkEntry(self.root, width=300, placeholder_text="Enter YouTube URL")
        self.url_entry.pack(pady=10)

        ctk.CTkButton(self.root, text="⬇ Download Video", command=self.download_video).pack(pady=10)

        self.result_label = ctk.CTkLabel(self.root, text="", wraplength=350)
        self.result_label.pack(pady=10)
        self.spinner = LoadingSpinner(self.root)

        ctk.CTkButton(self.root, text="⬅ Back", command=self.root.home_page).pack(pady=20)

    def download_video(self):
        url = self.url_entry.get()
        if not url:
            self.result_label.configure(text="❗ Please enter a URL.")
            return

        download_dir = config.get("download_path", "Not Found")
        os.makedirs(download_dir, exist_ok=True)
        self.spinner.start()
        self.root.update_idletasks()

        ydl_opts = {
            "cookiefile": "youtube_cookies.txt",
            "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            'ffmpeg_location': "C:\\ffmpeg\\bin",
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  
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
                if isinstance(info, dict):
                    title = info.get("title", "Unknown Title")
                    log_download("Video", title)
                    self.result_label.configure(text=f"✅ Downloaded: {title}")
                    self.show_toast(f"Downloaded: {title}")
                else:
                    self.result_label.configure(text="⚠️ Unexpected download result.")
        except Exception as e:
            if "file" in str(e).lower():
                print(f"Ignored file-related error: {e}")
            else:
                self.result_label.configure(text=f"❌ Error: {str(e)}")

        finally:
            self.spinner.stop()

    def show_toast(self, message):
        toast = ctk.CTkToplevel(self.root)
        toast.geometry("250x60+{}+{}".format(self.root.winfo_x() + 80, self.root.winfo_y() + 80))
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)
        ctk.CTkLabel(toast, text=message, font=("Arial", 12)).pack(pady=10, padx=10)
        toast.after(2500, toast.destroy)
