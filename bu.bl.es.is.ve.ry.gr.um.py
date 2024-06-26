import os
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk
import ctypes
import sys

def get_folder():
    root = tk.Tk()
    root.withdraw()

    dialog = tk.Toplevel(root)
    dialog.title("TOTK Batch WAV to BWAV Converter")

    label = ttk.Label(dialog, text="Select the folder containing the .wav files to be converted to .bwav")
    label.pack(padx=10, pady=10)

    folder_selected = tk.StringVar()
    folder_entry = ttk.Entry(dialog, textvariable=folder_selected, width=50)
    folder_entry.pack(padx=10, pady=5)

    def browse_folder():
        try:
            folder = filedialog.askdirectory()
            if folder:
                folder_selected.set(folder)
        except Exception as e:
            print("Error selecting folder:", e)

    browse_button = ttk.Button(dialog, text="Select Folder", command=browse_folder)
    browse_button.pack(padx=10, pady=10)

    def run_conversion():
        try:
            selected_folder = folder_selected.get()
            if selected_folder:
                dialog.destroy()
                process_folder(selected_folder)
                sys.exit()
        except Exception as e:
            print("Error running conversion:", e)
            cleanup(dialog)

    run_button = ttk.Button(dialog, text="Convert", command=run_conversion)
    run_button.pack(padx=10, pady=10)

    dialog.protocol("WM_DELETE_WINDOW", lambda: cleanup(dialog))

    dialog.grab_set()
    dialog.mainloop()

    return folder_selected.get()

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

def open_output_folder(folder_path):
    os.startfile(folder_path)

hide_console()

selected_folder = get_folder()

if selected_folder:
    process_folder(selected_folder)
