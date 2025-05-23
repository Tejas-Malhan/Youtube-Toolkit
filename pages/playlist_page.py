import os
import json
from assets.spinner import LoadingSpinner
import threading
import customtkinter as ctk
import yt_dlp

from utils.config import get_settings, get_cookie_path

config = get_settings()

class PlaylistPage:
    def __init__(self, root):
        self.root = root
        self.video_checkboxes = []
        self.video_data = []
        self.spinner = None
        self.init_ui()

    def init_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.root, text="Download Playlist", font=("Arial", 18)).pack(pady=10)

        self.url_entry = ctk.CTkEntry(self.root, width=400, placeholder_text="Enter YouTube Playlist URL")
        self.url_entry.pack(pady=10)

        self.format_var = ctk.StringVar(value="mp4")
        self.format_menu = ctk.CTkOptionMenu(self.root, values=["mp4", "mp3"], variable=self.format_var)
        self.format_menu.pack(pady=10)

        ctk.CTkButton(self.root, text="Load Playlist", command=self.start_metadata_thread).pack(pady=10)

        self.spinner = ctk.CTkProgressBar(self.root, mode="indeterminate", width=200)

        self.scroll_frame = ctk.CTkScrollableFrame(self.root, width=500, height=400)
        self.scroll_frame.pack(pady=10)

        ctk.CTkButton(self.root, text="Download Selected", command=self.start_download_thread).pack(pady=10)

        self.result_label = ctk.CTkLabel(self.root, text="", wraplength=400)
        self.result_label.pack(pady=10)
        self.spinner = LoadingSpinner(self.root)

        ctk.CTkButton(self.root, text="⬅ Back", command=self.root.home_page).pack(pady=20)

    def start_metadata_thread(self):
        self.spinner.pack(pady=10)
        self.spinner.start()
        thread = threading.Thread(target=self.fetch_playlist_metadata, daemon=True)
        thread.start()

    def fetch_playlist_metadata(self):
        url = self.url_entry.get()
        if not url:
            self.result_label.configure(text="Please enter a playlist URL.")
            return
        self.spinner.start()
        self.root.update_idletasks()

        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'skip_download': True,
            'force_generic_extractor': False
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                entries = info.get('entries', [])
                self.video_data = [{'id': e['id'], 'url': e['url'], 'title': e.get('title', 'No Title')} for e in entries]
        except Exception as e:
            self.spinner.stop()
            self.spinner.pack_forget()
            self.result_label.configure(text=f"Error fetching metadata: {e}")
            return
        finally:
            self.spinner.stop()
        self.root.after(0, self.populate_checkboxes)
        

    def populate_checkboxes(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.video_checkboxes.clear()

        for video in self.video_data:
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(self.scroll_frame, text=video["title"], variable=var)
            chk.pack(anchor='w', padx=10, pady=5)
            self.video_checkboxes.append((chk, var, video))

        self.spinner.stop()
        self.spinner.pack_forget()

    def start_download_thread(self):
        thread = threading.Thread(target=self.download_selected_videos, daemon=True)
        thread.start()

    def download_selected_videos(self):
        selected_videos = [video for chk, var, video in self.video_checkboxes if var.get()]
        if not selected_videos:
            self.result_label.configure(text="No videos selected.")
            return

        self.spinner.pack(pady=10)
        self.spinner.start()
        format_choice = self.format_var.get()
        download_dir = config.get("download_path", os.getcwd())

        app_dir = os.path.join(os.getenv("APPDATA"), "YouTubeToolkit")
        settings_path = os.path.join(app_dir, "settings.json")
        cookie_path = os.path.join(app_dir, "youtube_cookies.txt")

        for video in selected_videos:
            ydl_opts = {
                "ffmpeg_location": "ffmpeg/bin",  # adjust if needed
                "outtmpl": os.path.join(download_dir, f"%(title)s.%(ext)s"),
                "format": "bestaudio/best" if format_choice == "mp3" else "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                "quiet": True
            }

            # Optional: add mp3 postprocessor
            if format_choice == "mp3":
                ydl_opts["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }]

            # ✅ Inject cookie if enabled and exists
            try:
                if os.path.exists(settings_path):
                    with open(settings_path, "r") as f:
                        settings = json.load(f)
                        if settings.get("use_cookies") and os.path.exists(cookie_path):
                            ydl_opts["cookiefile"] = cookie_path
            except Exception as e:
                print(f"[WARN] Failed to apply cookie: {e}")

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video['url']])
            except Exception as e:
                self.result_label.configure(text=f"Error downloading {video['title']}: {e}")
                continue
            
        self.spinner.stop()
        self.spinner.pack_forget()
        self.result_label.configure(text=f"Download complete: {len(selected_videos)} video(s).")
