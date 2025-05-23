import json
import customtkinter as ctk
from PIL import Image
import urllib.request
import yt_dlp
from assets.spinner import LoadingSpinner
import io
import os
from tkinter import filedialog

class InfoPage:
    def __init__(self, root):
        self.root = root
        self.init_ui()

    def init_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.root, text="📍 YouTube Data Extractor", font=("Arial", 22, "bold")).pack(pady=(20, 10))

        self.url_entry = ctk.CTkEntry(self.root, width=500, placeholder_text="Paste YouTube Video URL here")
        self.url_entry.pack(pady=10)

        ctk.CTkButton(self.root, text="🔍 Extract Video Info", command=self.extract_data).pack(pady=10)

        self.result_text = ctk.CTkTextbox(self.root, width=550, height=280, wrap="word")
        self.result_text.pack(pady=(10, 5))

        self.thumbnail_label = ctk.CTkLabel(self.root, text="", width=320, height=180)
        self.thumbnail_label.pack(pady=5)

        self.download_thumb_button = ctk.CTkButton(self.root, text="🔽 Download Thumbnail", command=self.download_thumbnail)
        self.download_thumb_button.pack(pady=5)
        self.download_thumb_button.configure(state="disabled")
        self.spinner = LoadingSpinner(self.root)
        ctk.CTkButton(self.root, text="⬅ Back", command=self.root.home_page).pack(pady=15)

    def extract_data(self):
        url = self.url_entry.get()
        if not url:
            self.result_text.delete("1.0", "end")
            self.result_text.insert("end", "❌ Please enter a YouTube URL.\n")
            return
        self.spinner.start()
        self.root.update_idletasks()
        ydl_opts = {
            'ffmpeg_location': 'C:\\ffmpeg\\bin',
            'cookiefile': 'youtube_cookies.txt',
            'quiet': True,
            'skip_download': True,
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
                info = ydl.extract_info(url, download=False)

            data_lines = [
                f"\ud83d\udcdd Title: {info.get('title', 'N/A')}",
                f"\ud83d\udc64 Channel: {info.get('uploader', 'N/A')}",
                f"\ud83d\udcc5 Upload Date: {info.get('upload_date', 'N/A')}",
                f"⏱ Duration: {info.get('duration_string', str(info.get('duration', 'N/A')) + 's')}",
                f"📈 Views: {info.get('view_count', 'N/A')}",
                f"👍 Likes: {info.get('like_count', 'N/A')}",
                f"❌ Dislikes: {info.get('dislike_count', 'N/A')}",
                f"⭐ Rating: {info.get('average_rating', 'N/A')}",
                f"Tags: {', '.join(info.get('tags', [])) or 'N/A'}",
                f"Webpage: {info.get('webpage_url', 'N/A')}",
                f"Categories: {', '.join(info.get('categories', [])) or 'N/A'}",
                f"Live Broadcast: {info.get('is_live', 'N/A')}",
                f"Age Limit: {info.get('age_limit', 'N/A')}",
                f"\nDescription:\n{info.get('description', 'N/A')[:400]}...",
            ]

            self.result_text.delete("1.0", "end")
            self.result_text.insert("end", "\n".join(data_lines))

            # Load and display thumbnail
            self.thumbnail_url = info.get('thumbnail', '')
            if self.thumbnail_url:
                with urllib.request.urlopen(self.thumbnail_url) as u:
                    raw_data = u.read()
                image = Image.open(io.BytesIO(raw_data)).resize((320, 180))
                self.thumb_img = ctk.CTkImage(light_image=image, dark_image=image, size=(320, 180))
                self.thumbnail_label.configure(image=self.thumb_img, text="")
                self.download_thumb_button.configure(state="normal")
            else:
                self.thumbnail_label.configure(image=None, text="No Thumbnail Available")
                self.download_thumb_button.configure(state="disabled")

        except Exception as e:
            self.result_text.delete("1.0", "end")
            self.result_text.insert("end", f"\n❌ Error: {e}\n")

    def download_thumbnail(self):
        if hasattr(self, 'thumbnail_url') and self.thumbnail_url:
            try:
                file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")], title="Save Thumbnail As")
                if file_path:
                    urllib.request.urlretrieve(self.thumbnail_url, file_path)
                    self.result_text.insert("end", f"\n🔹 Thumbnail downloaded as '{file_path}'\n")
            except Exception as e:
                self.result_text.insert("end", f"\n🛑 Failed to download thumbnail: {e}\n")
            
            finally:
                self.spinner.stop() 