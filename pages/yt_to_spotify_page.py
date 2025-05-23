import customtkinter as ctk
from utils.spotify_utils import convert_yt_playlist_to_spotify

class YTtoSpotifyPage:
    def __init__(self, root):
        self.root = root
        self.init_ui()

    def init_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.root, text="🎵 YouTube → Spotify Playlist", font=("Arial", 18)).pack(pady=10)

        self.url_entry = ctk.CTkEntry(self.root, width=300, placeholder_text="Enter YouTube Playlist URL")
        self.url_entry.pack(pady=8)

        self.client_id_entry = ctk.CTkEntry(self.root, width=300, placeholder_text="Spotify Client ID")
        self.client_id_entry.pack(pady=8)

        self.client_secret_entry = ctk.CTkEntry(self.root, width=300, placeholder_text="Spotify Client Secret", show="*")
        self.client_secret_entry.pack(pady=8)

        ctk.CTkButton(self.root, text="Convert to Spotify", command=self.convert).pack(pady=12)

        self.result_label = ctk.CTkLabel(self.root, text="", wraplength=350)
        self.result_label.pack(pady=10)

        ctk.CTkButton(self.root, text="⬅ Back", command=self.root.home_page).pack(pady=20)

    def convert(self):
        yt_url = self.url_entry.get()
        client_id = self.client_id_entry.get()
        client_secret = self.client_secret_entry.get()

        self.result_label.configure(text="⏳ Converting playlist...")

        try:
            result_url = convert_yt_playlist_to_spotify(yt_url, client_id, client_secret)
            self.result_label.configure(text=f"✅ Success!\nSpotify Playlist: {result_url}")
        except Exception as e:
            self.result_label.configure(text=f"❌ Error: {e}")
