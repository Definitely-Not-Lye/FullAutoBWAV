import os
import subprocess
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, ttk
import ctypes
import sys
def get_folder_or_file():
    root = ctk.CTk()
    ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode("Dark")
    root.withdraw()
    dialog = ctk.CTkToplevel(root)
    dialog.title("Lye's TOTK Batch WAV to BWAV Converter")
    label = ctk.CTkLabel(dialog, text="Select the folder of .wav files or individual .wav file(s) to be converted to .bwav")
    label.pack(padx=10, pady=10)
    selection_paths = []
    selection_path = tk.StringVar()
    entry = ctk.CTkEntry(dialog, textvariable=selection_path)
    entry.pack(padx=10, pady=5, fill=tk.X)
    def browse_folder():
        try:
            folder = filedialog.askdirectory()
            if folder:
                selection_paths.clear()
                selection_paths.append(folder)
                selection_path.set(folder)
        except Exception as e:
            print("Error selecting folder:", e)
    def browse_file():
        try:
            files = filedialog.askopenfilenames(filetypes=[("WAV files", "*.wav")])
            if files:
                selection_paths.clear()
                selection_paths.extend(files)
                selection_path.set(", ".join(files))
        except Exception as e:
            print("Error selecting file:", e)
    browse_button_folder = ctk.CTkButton(dialog, text="Select Folder", command=browse_folder)
    browse_button_folder.pack(padx=10, pady=5)

    browse_button_file = ctk.CTkButton(dialog, text="Select File(s)", command=browse_file)
    browse_button_file.pack(padx=10, pady=5)
    def run_conversion():
        selected_paths = selection_paths
        if selected_paths:
            dialog.destroy()
            for path in selected_paths:
                if os.path.isdir(path):
                    process_folder(path)
                elif os.path.isfile(path):
                    process_file(path)
            sys.exit()
        else:
            print("No folder or file selected.")
    run_button = ctk.CTkButton(dialog, text="Convert", command=run_conversion)
    run_button.pack(padx=10, pady=10)
    dialog.protocol("WM_DELETE_WINDOW", lambda: cleanup(dialog))
    dialog.grab_set()
    dialog.mainloop()
def cleanup(dialog):
    dialog.destroy()
    sys.exit()
def hide_console():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
def show_console():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
def process_folder(selected_folder):
    if not selected_folder:
        print("No folder selected. Exiting...")
        return
    show_console()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.environ['__COMPAT_LAYER'] = 'WIN8RTM'
    output_dir = os.path.join(selected_folder, 'Output')
    os.makedirs(output_dir, exist_ok=True)
    try:
        for file in os.listdir(selected_folder):
            if file.endswith('.wav'):
                input_file = os.path.join(selected_folder, file)
                output_file = os.path.join(output_dir, os.path.splitext(file)[0] + '.bwav')
                try:
                    result = subprocess.run(['brstm_converter-clang-amd64.exe', input_file, '-o', output_file],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            text=True,
                                            check=True)
                    print("Conversion output:", result.stdout)
                except subprocess.CalledProcessError as e:
                    print("Error during conversion:", e)
                    print("Error output:", e.stderr)
        open_output_folder(output_dir)
    except Exception as e:
        print("Error processing folder:", e)
        show_console()
        cleanup(dialog)
def process_file(selected_file):
    if not selected_file:
        print("No file selected. Exiting...")
        return
    show_console()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.environ['__COMPAT_LAYER'] = 'WIN8RTM'
    output_dir = os.path.join(os.path.dirname(selected_file), 'Output')
    os.makedirs(output_dir, exist_ok=True)
    try:
        input_file = selected_file
        output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + '.bwav')
        result = subprocess.run(['brstm_converter-clang-amd64.exe', input_file, '-o', output_file],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                check=True)
        print("Conversion output:", result.stdout)
        open_output_folder(output_dir)
    except subprocess.CalledProcessError as e:
        print("Error during conversion:", e)
        print("Error output:", e.stderr)
    except Exception as e:
        print("Error processing file:", e)
        show_console()
        cleanup(dialog)
def open_output_folder(folder_path):
    os.startfile(folder_path)
hide_console()
get_folder_or_file()
