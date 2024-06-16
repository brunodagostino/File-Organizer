import logging
import os

from hydra.utils import to_absolute_path

LOG_DIR = to_absolute_path("logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "file_organizer.log"),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)
