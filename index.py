import tkinter as tk
from tkinter import messagebox
import time

class RSVPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rapid Serial Visual Presentation")
        self.root.geometry("800x600")

        self.root.bind("<Configure>", self.resize_widgets)
        
        self.text_label = tk.Label(root, text="Enter your text:", font=("Arial", 16))
        self.text_label.pack(pady=10)

        self.text_input = tk.Text(root, height=10, font=("Arial", 14), wrap=tk.WORD)
        self.text_input.pack(padx=20, pady=10)

        self.start_button = tk.Button(root, text="Start", font=("Arial", 14), command=self.start_rsvp)
        self.start_button.pack(pady=20)

        self.speed_frame = tk.Frame(root)
        self.speed_frame.pack(pady=10)

        self.speed_label = tk.Label(self.speed_frame, text="Words per minute (WPM):", font=("Arial", 14))
        self.speed_label.grid(row=0, column=0, padx=5)

        self.speed_scale = tk.Scale(self.speed_frame, from_=300, to=700, orient='horizontal', length=300, command=self.update_wpm_from_scale)
        self.speed_scale.set(300)
        self.speed_scale.grid(row=0, column=1, padx=5)

        self.speed_entry = tk.Entry(self.speed_frame, font=("Arial", 14), width=5)
        self.speed_entry.insert(0, "300")
        self.speed_entry.grid(row=0, column=2, padx=5)
        self.speed_entry.bind("<Return>", self.update_wpm_from_entry)

    def resize_widgets(self, event):
        self.text_input.config(width=int(self.root.winfo_width() / 10))
        self.start_button.config(width=int(self.root.winfo_width() / 25))

    def update_wpm_from_scale(self, value):
        self.speed_entry.delete(0, tk.END)
        self.speed_entry.insert(0, value)

    def update_wpm_from_entry(self, event):
        try:
            wpm = int(self.speed_entry.get())
            if 100 <= wpm <= 1000:
                self.speed_scale.set(wpm)
            else:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid WPM between 100 and 1000.")

    def start_rsvp(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text!")
            return

        try:
            wpm = int(self.speed_entry.get())
            if wpm <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid WPM!")
            return

        words = text.split()
        delay = 60 / wpm
        
        self.fullscreen_window = tk.Toplevel(self.root)
        self.fullscreen_window.attributes("-fullscreen", True)
        self.fullscreen_window.configure(bg='black')

        self.word_label = tk.Label(self.fullscreen_window, text="", font=("Arial", 50), fg='white', bg='black')
        self.word_label.pack(expand=True)

        self.fullscreen_window.bind("<Escape>", lambda e: self.fullscreen_window.destroy())
        self.fullscreen_window.bind("<space>", lambda e: self.fullscreen_window.destroy())

        self.show_words(words, delay)

    def show_words(self, words, delay):
        for word in words:
            self.word_label.config(text=word)
            self.root.update()
            time.sleep(delay)
        
        self.word_label.config(text="")
        self.fullscreen_window.focus_set()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = RSVPApp(root)
    root.mainloop()
