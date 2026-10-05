import tkinter as tk
from tkinter import ttk, messagebox

class FingerTapCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("Finger Tap Counter")
        self.root.geometry("480x620")
        self.root.configure(bg="#181818") 


        self.duration_seconds = 30
        self.time_left = self.duration_seconds
        self.count = 0
        self.is_running = False
        self.timer_id = None
        self.current_key = "<space>"


        self.root.bind("<Button-1>", self.on_root_click)


        setting_card = tk.LabelFrame(
            root, text=" Settings ", fg="#888888", bg="#252526",
            bd=1, relief="solid", font=("Helvetica", 9, "bold")
        )
        setting_card.pack(fill="x", padx=15, pady=(15, 8))


        setting_inner = tk.Frame(setting_card, bg="#252526", padx=10, pady=10)
        setting_inner.pack(fill="x")


        tk.Label(setting_inner, text="Duration:", fg="#cccccc", bg="#252526", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", padx=2)
        self.duration_entry = tk.Entry(setting_inner, width=5, font=("Helvetica", 10), justify="center", bg="#333333", fg="#ffffff", insertbackground="#ffffff")
        self.duration_entry.insert(0, "30")
        self.duration_entry.grid(row=0, column=1, padx=4)

        self.unit_combobox = ttk.Combobox(setting_inner, values=["sec (s)", "min (m)"], width=7, state="readonly")
        self.unit_combobox.current(0)
        self.unit_combobox.grid(row=0, column=2, padx=4)

        tk.Label(setting_inner, text="Key:", fg="#cccccc", bg="#252526", font=("Helvetica", 10)).grid(row=0, column=3, sticky="w", padx=(10, 2))
        self.key_entry = tk.Entry(setting_inner, width=6, font=("Helvetica", 10), justify="center", bg="#333333", fg="#ffffff", insertbackground="#ffffff")
        self.key_entry.insert(0, "space")
        self.key_entry.grid(row=0, column=4, padx=4)


        self.duration_entry.bind("<FocusIn>", self.unbind_key_temporarily)
        self.key_entry.bind("<FocusIn>", self.unbind_key_temporarily)


        self.apply_btn = tk.Button(
            setting_inner, text="Apply", command=self.apply_settings,
            font=("Helvetica", 9, "bold"), bg="#383838", fg="#64b5f6",
            activebackground="#4f4f4f", activeforeground="#90caf9",
            bd=0, padx=8, pady=2, cursor="hand2"
        )
        self.apply_btn.grid(row=0, column=5, padx=(6, 0))


        timer_card = tk.Frame(root, bg="#2d2d30", bd=1, relief="solid")
        timer_card.pack(fill="x", padx=15, pady=8)

        self.timer_label = tk.Label(
            timer_card, text=f"Timer: {self.time_left}s",
            font=("Helvetica", 20, "bold"), fg="#ffb74d", bg="#2d2d30", pady=10
        )
        self.timer_label.pack()

        self.tap_card = tk.Frame(root, bg="#212121", bd=2, relief="groove")
        self.tap_card.pack(fill="both", expand=True, padx=15, pady=8)

        self.tap_area = tk.Label(
            self.tap_card, text="Click here or press set key\nto start counting",
            font=("Helvetica", 15, "bold"), fg="#9e9e9e", bg="#212121",
            cursor="hand2"
        )
        self.tap_area.pack(fill="both", expand=True, padx=10, pady=10)


        self.tap_area.bind("<Button-1>", self.on_tap)
        self.tap_card.bind("<Button-1>", self.on_tap)
        self.bind_custom_key(self.current_key)

        count_card = tk.Frame(root, bg="#1e282d", bd=1, relief="solid")
        count_card.pack(fill="x", padx=15, pady=8)

        self.count_label = tk.Label(
            count_card, text="0",
            font=("Helvetica", 56, "bold"), fg="#81c784", bg="#1e282d", pady=5
        )
        self.count_label.pack()

        self.reset_btn = tk.Button(
            root, text="RESET", command=self.reset,
            font=("Helvetica", 12, "bold"), bg="#37474f", fg="#ffffff",
            activebackground="#455a64", activeforeground="#ffffff",
            bd=0, pady=10, cursor="hand2"
        )
        self.reset_btn.pack(fill="x", padx=15, pady=(8, 15))

    def unbind_key_temporarily(self, event=None):
        if self.current_key:
            self.root.unbind(self.current_key)

    def on_root_click(self, event):
        widget = event.widget
        if widget not in [self.duration_entry, self.key_entry]:
            self.root.focus_set()
            self.bind_custom_key(self.key_entry.get())

    def bind_custom_key(self, key_name):
        if self.current_key:
            self.root.unbind(self.current_key)

        key_str = key_name.strip().lower()
        if key_str in ["space", "spacebar"]:
            self.current_key = "<space>"
        elif len(key_str) == 1:
            self.current_key = key_str
        else:
            self.current_key = f"<{key_str}>"

        try:
            self.root.bind(self.current_key, self.on_tap)
        except Exception:
            messagebox.showerror("Key Error", f"Invalid key format: {key_name}")
            self.current_key = "<space>"
            self.root.bind(self.current_key, self.on_tap)

    def apply_settings(self):
        if self.is_running:
            messagebox.showwarning("Warning", "Test is running! Please reset before changing settings.")
            return

        try:
            val = float(self.duration_entry.get())
            if val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number for duration!")
            return

        unit = self.unit_combobox.get()
        if "min" in unit:
            self.duration_seconds = int(val * 60)
        else:
            self.duration_seconds = int(val)

        new_key = self.key_entry.get()
        if new_key:
            self.bind_custom_key(new_key)

        self.root.focus_set()
        self.reset()
        messagebox.showinfo("Success", f"Settings Applied!\nDuration: {self.duration_seconds}s\nKey: {new_key}")

    def on_tap(self, event=None):
        if self.time_left <= 0:
            return

        if not self.is_running:
            self.is_running = True
            key_display = self.key_entry.get()
            self.tap_area.config(text=f"Counting...\n(Current Key: {key_display})", fg="#e0e0e0")
            self.tap_card.config(bg="#1b3a4b")
            self.tap_area.config(bg="#1b3a4b")
            self.update_timer()

        self.count += 1
        self.count_label.config(text=str(self.count))

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Timer: {self.time_left}s", fg="#ffb74d")
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.is_running = False
            self.timer_label.config(text="Time's up!", fg="#e57373")
            self.tap_area.config(text="Measurement Locked", fg="#757575")
            self.tap_card.config(bg="#212121")
            self.tap_area.config(bg="#212121")

    def reset(self, event=None):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.time_left = self.duration_seconds
        self.count = 0
        self.is_running = False

        self.timer_label.config(text=f"Timer: {self.time_left}s", fg="#ffb74d")
        self.count_label.config(text="0")
        key_display = self.key_entry.get()
        self.tap_area.config(text=f"Click here or press [{key_display}]\nto start counting", fg="#9e9e9e")
        self.tap_card.config(bg="#212121")
        self.tap_area.config(bg="#212121")

if __name__ == "__main__":
    root = tk.Tk()
    app = FingerTapCounter(root)
    root.mainloop()
