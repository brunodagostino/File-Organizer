import glob
import logging
import os
import shutil
from tkinter import messagebox

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


# Function to get the folder name for a file type based on its extension
def get_file_type_folder(extension):
    for folder, extensions in file_types.items():
        if extension in extensions:
            return folder
    return "Others"


# Organize files by tags
def organize_files_by_tags(directory, tags, progress_bar):
    try:
        total_files = sum(
            len(glob.glob(os.path.join(directory, "*" + ext)))
            for exts in tags.values()
            for ext in exts
        )
        if total_files == 0:
            messagebox.showinfo("Info", "No files found to organize")
            return

        processed_files = 0

        # Create tag-based folders if they don't exist
        for tag, extensions in tags.items():
            tag_path = os.path.join(directory, tag)
            if not os.path.exists(tag_path):
                try:
                    os.makedirs(tag_path)
                    logging.info(f"Created directory: {tag_path}")
                except OSError as e:
                    logging.error(f"Error creating directory {tag_path}: {e}")
                    messagebox.showerror(
                        "Directory Error", f"Error creating directory {tag_path}: {e}"
                    )
                    continue

            # Create subfolders for each file extension category
            for category in file_types.keys():
                ext_folder = os.path.join(tag_path, category)
                if not os.path.exists(ext_folder):
                    try:
                        os.makedirs(ext_folder)
                        logging.info(f"Created subdirectory: {ext_folder}")
                    except OSError as e:
                        logging.error(f"Error creating subdirectory {ext_folder}: {e}")
                        messagebox.showerror(
                            "Directory Error",
                            f"Error creating subdirectory {ext_folder}: {e}",
                        )
                        continue

        # Move files into their respective folders
        for tag, extensions in tags.items():
            for extension in extensions:
                for file_path in glob.iglob(os.path.join(directory, "*" + extension)):
                    if tag in os.path.basename(file_path):
                        dest_folder = os.path.join(
                            directory, tag, get_file_type_folder(extension)
                        )
                        try:
                            shutil.move(file_path, dest_folder)
                            logging.info(f"Moved {file_path} to {dest_folder}")
                            processed_files += 1
                            progress_bar["value"] = (
                                processed_files / total_files
                            ) * 100
                            progress_bar.update()
                        except (shutil.Error, OSError) as e:
                            logging.error(
                                f"Error moving file {file_path} to {dest_folder}: {e}"
                            )
                            messagebox.showerror(
                                "File Error",
                                f"Error moving file {file_path} to {dest_folder}: {e}",
                            )

        messagebox.showinfo(
            "Success", f"Organized {processed_files} files into categories."
        )
        logging.info(f"Organized {processed_files} files")
    except Exception as e:
        logging.error(f"Error organizing files in directory {directory}: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
