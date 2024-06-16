import glob
import logging
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from config_manager import load_config, save_config
from file_operations import organize_files_by_tags

# Dictionary to map file extensions to folder names
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Video": [".mp4", ".mkv", ".flv", ".avi", ".mov"],
    "Scripts": [".py", ".js", ".html", ".css"],
    "Others": [],  # For all other file types
}

# Combine all default extensions into a set
default_extensions = {ext for exts in file_types.values() for ext in exts}


def browse_directory(entry):
    directory = filedialog.askdirectory()
    if directory:
        entry.delete(0, tk.END)
        entry.insert(0, directory)
    else:
        logging.warning("No directory selected.")
        messagebox.showwarning("Directory Selection", "No directory selected.")


def start_organization(entry, tags, progress_bar):
    directory = entry.get()
    if os.path.isdir(directory):
        clean_tags(tags)  # Clean the tags before using them
        organize_files_by_tags(directory, tags, progress_bar)
        save_config(tags)  # Save updated config after organization
    else:
        logging.error("The provided directory does not exist.")
        messagebox.showerror("Error", "The provided directory does not exist.")


def edit_tags(tags):
    editor = tk.Toplevel()
    editor.title("Edit Tags")

    rows = len(tags)
    for i, (tag, extensions) in enumerate(tags.items()):
        ttk.Label(editor, text=tag).grid(row=i, column=0, padx=5, pady=5)
        ext_entry = ttk.Entry(editor)
        ext_entry.grid(row=i, column=1, padx=5, pady=5)

        if extensions is None:
            extensions = []
        ext_entry.insert(
            0, ",".join(extensions if isinstance(extensions, (list, tuple)) else [])
        )
        ext_entry.bind(
            "<FocusOut>", lambda e, t=tag, entry=ext_entry: update_tags(t, entry, tags)
        )

    ttk.Button(editor, text="Add Tag", command=lambda: add_tag(tags, editor)).grid(
        row=rows + 1, column=0, padx=5, pady=5, columnspan=2
    )

    editor.mainloop()


def preview_files(directory, tags):
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "The provided directory does not exist.")
        return

    preview_window = tk.Toplevel()
    preview_window.title("File Preview")

    text_widget = tk.Text(preview_window, wrap="word", width=80, height=20)
    text_widget.grid(row=0, column=0, padx=10, pady=10)

    for tag, extensions in tags.items():
        if not extensions:  # Skip tags with None or empty extensions
            continue
        text_widget.insert(tk.END, f"{tag}:\n")
        for extension in extensions:
            for file_path in glob.iglob(os.path.join(directory, "*" + extension)):
                if tag in os.path.basename(file_path):
                    text_widget.insert(tk.END, f"  {os.path.basename(file_path)}\n")
        text_widget.insert(tk.END, "\n")

    preview_window.mainloop()


def create_main_window():
    root = tk.Tk()
    root.title("File Organizer by Tags")
    root.geometry("600x300")

    # Style Configuration
    style = ttk.Style()
    style.configure("TLabel", padding=6, font=("Helvetica", 12))
    style.configure("TButton", padding=6, font=("Helvetica", 12))
    style.configure("TEntry", padding=6, font=("Helvetica", 12))
    style.configure("TProgressbar", thickness=20)

    tags = load_config()
    tags = clean_tags(tags)  # Clean the tags after loading

    # Configure grid layout
    root.columnconfigure(1, weight=1)
    root.rowconfigure(1, weight=1)

    ttk.Label(root, text="Select Directory:").grid(
        row=0, column=0, padx=5, pady=5, sticky=tk.W
    )
    directory_entry = ttk.Entry(root, width=50)
    directory_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
    ttk.Button(
        root, text="Browse", command=lambda: browse_directory(directory_entry)
    ).grid(row=0, column=2, padx=5, pady=5)

    progress_bar = ttk.Progressbar(
        root, orient="horizontal", length=400, mode="determinate"
    )
    progress_bar.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky=tk.EW)

    ttk.Button(
        root,
        text="Start",
        command=lambda: start_organization(directory_entry, tags, progress_bar),
    ).grid(row=2, column=1, padx=5, pady=5)
    ttk.Button(root, text="Edit Tags", command=lambda: edit_tags(tags)).grid(
        row=2, column=2, padx=5, pady=5
    )

    ttk.Button(
        root,
        text="Preview Files",
        command=lambda: preview_files(directory_entry.get(), tags),
    ).grid(row=3, column=1, padx=5, pady=5)

    root.mainloop()


def update_tags(tag, entry, tags):
    extensions = set([ext.strip() for ext in entry.get().split(",") if ext.strip()])
    tags[tag] = list(extensions)


def add_tag(tags, editor):
    def save_tag():
        tag_name = tag_entry.get()
        if not tag_name.strip():
            messagebox.showerror("Input Error", "Tag Name is required.")
            return
        extensions = set(
            [ext.strip() for ext in ext_entry.get().split(",") if ext.strip()]
        )
        extensions.update(default_extensions)
        tags[tag_name] = list(extensions)
        editor.destroy()
        edit_tags(tags)

    add_window = tk.Toplevel(editor)
    add_window.title("Add New Tag")

    ttk.Label(add_window, text="Tag Name").grid(row=0, column=0, padx=5, pady=5)
    tag_entry = ttk.Entry(add_window)
    tag_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(add_window, text="Extensions (comma separated)").grid(
        row=1, column=0, padx=5, pady=5
    )
    ext_entry = ttk.Entry(add_window)
    ext_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(add_window, text="Save", command=save_tag).grid(
        row=2, column=0, padx=5, pady=5, columnspan=2
    )


def clean_tags(tags):
    return {tag: exts for tag, exts in tags.items() if exts is not None}


if __name__ == "__main__":
    create_main_window()
