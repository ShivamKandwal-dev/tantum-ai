import tkinter as tk
from tkinter import ttk

class ProgressWindow:
    def __init__(self, title="Processing...", initial_text="Starting..."):
        self.root = tk.Toplevel()
        self.root.title(title)
        self.root.geometry("400x150")
        self.root.resizable(False, False)

        self.label = tk.Label(self.root, text=initial_text, font=("Arial", 12))
        self.label.pack(pady=10)

        self.progress = ttk.Progressbar(self.root, orient="horizontal",
                                        length=350, mode="determinate")
        self.progress.pack(pady=10)

        self.root.update()

    def update_progress(self, done, total=None, message=""):
        # done = percent or step number, depending on caller
        if total:
            try:
                percent = (done / total) * 100
            except Exception:
                percent = 0
        else:
            percent = float(done)

        if percent < 0: percent = 0
        if percent > 100: percent = 100

        self.progress["value"] = percent
        if message:
            self.label.config(text=message)

        self.root.update()

    def close(self):
        self.root.destroy()
