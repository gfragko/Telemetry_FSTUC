import tkinter as tk
from tkinter import filedialog

# Create a hidden root window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Open file explorer and select a file
file_path = filedialog.askopenfilename(title="Select a file")

# Print the selected file path
if file_path:
    print(f"Selected file: {file_path}")
else:
    print("No file selected.")