import logging

from colorlog import ColoredFormatter

# Configure logging with color
formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s %(levelname)s : [%(name)s] : %(message)s",
    log_colors={
        "DEBUG": "orange",
        "INFO": "blue",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
    datefmt='%Y/%m/%d %H:%M:%S'
)
stream = logging.StreamHandler()
stream.setFormatter(formatter)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-1s : %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S'), logging.getLogger().addHandler(stream)

