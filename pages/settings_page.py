import customtkinter as ctk
from tkinter import filedialog
import os
import json
import webbrowser

APP_DIR = os.path.join(os.getenv("APPDATA"), "YouTubeToolkit")
SETTINGS_FILE = os.path.join(APP_DIR, "settings.json")
COOKIES_PATH = os.path.join(APP_DIR, "youtube_cookies.txt")

class SettingsPage:
    def __init__(self, root):
        self.root = root
        self.init_ui()

    def init_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.root, text="⚙️ Settings", font=("Arial", 18)).pack(pady=10)

        self.path_entry = ctk.CTkEntry(self.root, width=300, placeholder_text="Download folder")
        self.path_entry.pack(pady=8)

        self.appearance_option = ctk.CTkOptionMenu(self.root, values=["System", "Light", "Dark"])
        self.appearance_option.pack(pady=8)

        self.cookie_check = ctk.CTkCheckBox(self.root, text="Use cookies.txt for YouTube")
        self.cookie_check.pack(pady=5)

        ctk.CTkButton(self.root, text="📄 How to Get Cookies File", command=self.show_cookie_help).pack(pady=5)
        ctk.CTkButton(self.root, text="📁 Upload cookies.txt", command=self.select_cookie_file).pack(pady=5)

        ctk.CTkButton(self.root, text="Save Settings", command=self.save_settings).pack(pady=10)

        self.result_label = ctk.CTkLabel(self.root, text="", wraplength=350)
        self.result_label.pack(pady=10)

        ctk.CTkButton(self.root, text="⬅ Back", command=self.root.home_page).pack(pady=20)

        os.makedirs(APP_DIR, exist_ok=True)
        self.load_settings()

    def save_settings(self):
        settings = {
            "download_path": self.path_entry.get(),
            "theme": self.appearance_option.get(),
            "use_cookies": self.cookie_check.get()
        }
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)
        ctk.set_appearance_mode(settings["theme"])
        self.result_label.configure(text="✅ Settings saved.")

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
                self.path_entry.insert(0, settings.get("download_path", ""))
                self.appearance_option.set(settings.get("theme", "System"))
                if settings.get("use_cookies"):
                    self.cookie_check.select()

    def show_cookie_help(self):
        help_text = (
            "🔐 To get your YouTube cookies:\n\n"
            "1. Open Google Chrome.\n"
            "2. Install: Get cookies.txt extension → https://bit.ly/get-cookies-txt\n"
            "3. Login to YouTube. Click the extension.\n"
            "4. Save as cookies.txt and upload it here.\n"
            "App will use it to access restricted videos."
        )
        help_window = ctk.CTkToplevel(self.root)
        help_window.title("How to Get YouTube Cookies")
        help_window.geometry("450x320")
        ctk.CTkLabel(help_window, text=help_text, wraplength=420, justify="left").pack(padx=10, pady=10)

    def select_cookie_file(self):
        file_path = filedialog.askopenfilename(title="Select cookies.txt file", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "rb") as src, open(COOKIES_PATH, "wb") as dst:
                    dst.write(src.read())
                self.result_label.configure(text="✅ Cookie file saved securely.")
            except Exception as e:
                self.result_label.configure(text=f"❌ Failed: {e}")
