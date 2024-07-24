import os
import tkinter as tk
from tkinter import messagebox
from measurement import setup_measurement, perform_measurement, interface_with_ppms
from data_analysis import calculate_resistivity, calculate_hall_coefficient


if not os.path.exists('data'):
    os.makedirs('data')

def run_gui():
    root = tk.Tk()
    root.title("Resistivity and Hall Effect Measurements")

    # Sample dimensions input
    tk.Label(root, text="Sample Length (cm):").grid(row=0, column=0)
    length_entry = tk.Entry(root)
    length_entry.grid(row=0, column=1)

    tk.Label(root, text="Sample Cross-Sectional Area (cm^2):").grid(row=1, column=0)
    area_entry = tk.Entry(root)
    area_entry.grid(row=1, column=1)

    # Channel input
    channels = []

    def add_channel():
        try:
            current = float(current_entry.get())
            name = channel_name_entry.get()
            if not name:
                messagebox.showerror("Invalid Input", "Please enter a name for the channel.")
                return
            channels.append({"name": name, "current": current})
            channel_list.insert(tk.END, f"Channel {name}: {current} A")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numerical values for current.")

    def remove_channel():
        try:
            selected_index = channel_list.curselection()[0]
            channel_list.delete(selected_index)
            del channels[selected_index]
        except IndexError:
            messagebox.showerror("Invalid Selection", "Please select a channel to remove.")

    tk.Label(root, text="Channel Name:").grid(row=2, column=0)
    channel_name_entry = tk.Entry(root)
    channel_name_entry.grid(row=2, column=1)

    tk.Label(root, text="Current (A):").grid(row=3, column=0)
    current_entry = tk.Entry(root)
    current_entry.grid(row=3, column=1)

    add_channel_button = tk.Button(root, text="Add Channel", command=add_channel)
    add_channel_button.grid(row=4, column=0, columnspan=2)

    remove_channel_button = tk.Button(root, text="Remove Channel", command=remove_channel)
    remove_channel_button.grid(row=5, column=0, columnspan=2)

    channel_list = tk.Listbox(root)
    channel_list.grid(row=6, column=0, columnspan=2)

    def start_measurement():
        try:
            length = float(length_entry.get())
            area = float(area_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numerical values for length and area.")
            return
        
        setup_measurement(length, area)
        results = perform_measurement(channels)
        
        for channel in results:
            resistivity = calculate_resistivity({"voltage": results[channel]}, length, area)
            hall_coefficient = calculate_hall_coefficient({"voltage": results[channel]})
            # Display results
            tk.Label(root, text=f"{channel} - Resistivity: {resistivity} Ohm.cm").grid(row=7, column=0, columnspan=2)
            tk.Label(root, text=f"{channel} - Hall Coefficient: {hall_coefficient} cm^3/C").grid(row=8, column=0, columnspan=2)
            # Save results
            with open(f'data/results_{channel}.txt', 'w') as f:
                f.write(f"Resistivity: {resistivity} Ohm.cm\nHall Coefficient: {hall_coefficient} cm^3/C\n")

        # Example usage of interface_with_ppms
        ppms_response = interface_with_ppms('TCPIP::192.168.1.100::INSTR', '*IDN?')
        print(f"PPMS Response: {ppms_response}")

    start_button = tk.Button(root, text="Start Measurement", command=start_measurement)
    start_button.grid(row=9, column=0, columnspan=2)

    root.mainloop()