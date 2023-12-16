import logging
import os

log_file_path = f'/Users/zipengzhu/Desktop/CS179M/port_log.txt'

log_format = "%(asctime)s: %(message)s"
logger = logging.getLogger('my_app_logger')  # Create a new logger
logger.setLevel(logging.INFO)
handler = logging.FileHandler('port_log.txt')
handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(handler)

def log_message(message):
    logger.info(message)  # Use the custom logger, not the root logger


def log_login(user_name):
    """
    Logs a user login event.
    """
    log_message(f"{user_name} has logged in")

def log_system_info(info):
    """
    Logs system information.
    """
    log_message(f"System {info}")

def log_user_message(user_name, message):
    """
    Logs a message sent by a user.
    """
    log_message(f'{user_name} sent "{message}"')

#os.chmod(log_file_path, 0o666)


