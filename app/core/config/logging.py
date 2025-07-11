import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # Or DEBUG for more detail
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),  # Log to console
            logging.FileHandler("app.log"),  # Log to file
        ]
    )

setup_logging()