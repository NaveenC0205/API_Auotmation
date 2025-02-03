import logging
import os


log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
logger = logging.getLogger('ClientURLLogger')
logger.setLevel(logging.INFO)
log_file = os.path.join(log_directory, 'pytestinglog.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)8s] %(message)s ( %(filename)s:%(lineno)s)')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
