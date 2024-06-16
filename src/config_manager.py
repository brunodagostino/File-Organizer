import logging
from tkinter import messagebox

from hydra import compose, initialize
from hydra.utils import to_absolute_path
from omegaconf import OmegaConf


# Load updated config
def load_config():
    config_path = to_absolute_path("config/tags/default_tags.yaml")
    try:
        existing_config = OmegaConf.load(config_path)
        if "tags" not in existing_config:
            existing_config.tags = {}
        return existing_config.tags
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        messagebox.showerror("Configuration Error", f"Error loading configuration: {e}")
        return {}


# Save updated config to the file
def save_config(tags):
    try:
        config_path = to_absolute_path("config/tags/default_tags.yaml")
        existing_config = OmegaConf.load(config_path)
        if "tags" not in existing_config:
            existing_config.tags = {}

        existing_tags = existing_config.tags

        # Merge existing tags with new tags
        for tag, exts in tags.items():
            if exts is None:
                continue  # Skip tags with None as their extensions
            if tag in existing_tags:
                existing_tags[tag] = list(set(existing_tags[tag] + exts))
            else:
                existing_tags[tag] = exts

        # Save the updated configuration
        with open(config_path, "w") as f:
            OmegaConf.save(config=existing_config, f=f)
    except Exception as e:
        logging.error(f"Error saving configuration: {e}")
        messagebox.showerror("Configuration Error", f"Error saving configuration: {e}")


def initialize_config():
    # Initialize Hydra
    try:
        initialize(config_path="../config", job_name="file_organizer")
        cfg = compose(config_name="config")
        return cfg
    except Exception as e:
        logging.error(f"Error initializing Hydra configuration: {e}")
        messagebox.showerror(
            "Configuration Error", f"Error initializing configuration: {e}"
        )
        raise
