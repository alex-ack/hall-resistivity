import tkinter as tk
from tkinter import messagebox

class ResistivityMeasurementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resistivity and Hall Effect Measurements")

        self.channels = []

        # Create and place widgets
        tk.Label(root, text="Sample Length (cm):").grid(row=0, column=0)
        self.length_entry = tk.Entry(root)
        self.length_entry.grid(row=0, column=1)

        tk.Label(root, text="Sample Cross-Sectional Area (cm^2):").grid(row=1, column=0)
        self.area_entry = tk.Entry(root)
        self.area_entry.grid(row=1, column=1)

        tk.Label(root, text="Channel Name:").grid(row=2, column=0)
        self.channel_name_entry = tk.Entry(root)
        self.channel_name_entry.grid(row=2, column=1)

        tk.Label(root, text="Current (A):").grid(row=3, column=0)
        self.current_entry = tk.Entry(root)
        self.current_entry.grid(row=3, column=1)

        self.add_button = tk.Button(root, text="Add Channel", command=self.add_channel)
        self.add_button.grid(row=4, column=0)

        self.remove_button = tk.Button(root, text="Remove Channel", command=self.remove_channel)
        self.remove_button.grid(row=4, column=1)

        self.channel_listbox = tk.Listbox(root)
        self.channel_listbox.grid(row=5, column=0, columnspan=2)

        self.start_button = tk.Button(root, text="Start Measurement", command=self.start_measurement)
        self.start_button.grid(row=6, column=0, columnspan=2)

    def add_channel(self):
        channel_name = self.channel_name_entry.get()
        current = self.current_entry.get()

        if not channel_name or not current:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            current = float(current)
        except ValueError:
            messagebox.showerror("Error", "Current must be a number")
            return

        if channel_name in self.channels:
            messagebox.showerror("Error", f"Channel '{channel_name}' already exists")
            return

        self.channels.append(channel_name)
        self.channel_listbox.insert(tk.END, f"Channel {channel_name}: {current:.1f} A")
        self.channel_name_entry.delete(0, tk.END)
        self.current_entry.delete(0, tk.END)

    def remove_channel(self):
        selected = self.channel_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No channel selected")
            return

        selected_channel = self.channel_listbox.get(selected)
        channel_name = selected_channel.split(':')[0].replace("Channel ", "").strip()

        try:
            self.channels.remove(channel_name)
            self.channel_listbox.delete(selected)
        except ValueError:
            messagebox.showerror("Error", f"Channel '{channel_name}' not found in list")

    def start_measurement(self):
        length = self.length_entry.get()
        area = self.area_entry.get()

        if not length or not area:
            messagebox.showerror("Error", "Please fill in sample dimensions")
            return

        try:
            length = float(length)
            area = float(area)
        except ValueError:
            messagebox.showerror("Error", "Sample dimensions must be numbers")
            return

        if not self.channels:
            messagebox.showerror("Error", "No channels added")
            return

        # Here you would start the actual measurement process
        # This is just a placeholder for demonstration
        messagebox.showinfo("Info", "Measurement started")

def run_gui():
    root = tk.Tk()
    app = ResistivityMeasurementApp(root)
    root.mainloop()