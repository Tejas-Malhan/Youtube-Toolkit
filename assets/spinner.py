import customtkinter as ctk
import threading
import itertools
import time

class LoadingSpinner:
    def __init__(self, parent):
        self.label = ctk.CTkLabel(parent, text="⏳", font=("Arial", 24))
        self.running = False

    def start(self):
        self.running = True
        self.label.pack(pady=10)
        threading.Thread(target=self.animate, daemon=True).start()

    def animate(self):
        for frame in itertools.cycle(["⏳", "⌛", "🕐", "🕘"]):
            if not self.running:
                break
            self.label.configure(text=frame)
            time.sleep(0.2)

    def stop(self):
        self.running = False
        self.label.pack_forget()
