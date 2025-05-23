import customtkinter as ctk
from pages.video_pages import VideoPage
from pages.audio_page import AudioPage
from pages.playlist_page import PlaylistPage
from pages.info_page import InfoPage
from pages.yt_to_spotify_page import YTtoSpotifyPage
from pages.settings_page import SettingsPage

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def vp(self):
    video_window = ctk.CTkToplevel(widget=self)
    VideoPage(video_window)

class YouTubeToolkitApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Toolkit")
        self.geometry("500x300")
        self.minsize(500, 300)
        self.maxsize(1600, 800)
        self.resizable(True, True)
        self.home_page()

    def home_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text="🎬 YouTube Toolkit", font=("Arial", 22)).pack(pady=20)

        grid_frame = ctk.CTkFrame(self)
        grid_frame.pack(pady=10)

        buttons = [
            ("📥 Download Video", VideoPage),
            ("🎵 Download Audio", AudioPage),
            ("🔍 Download Playlist", PlaylistPage),
            ("🖼️ Extract Info", InfoPage)
        ]

        for i, (text, PageClass) in enumerate(buttons):
            btn = ctk.CTkButton(grid_frame, text=text, width=180, height=40,
                                command=lambda p=PageClass: p(self))
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)

        ctk.CTkButton(self, text="⚙️ Settings", width=200, command=lambda: SettingsPage(self)).pack(pady=20)

if __name__ == "__main__":
    app = YouTubeToolkitApp()
    app.mainloop()
