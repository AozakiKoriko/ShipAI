import logging
import os

log_file_path = f'/Users/zipengzhu/Desktop/Ship/port_log.txt'

# Define a custom logging format
log_format = "%(asctime)s: %(message)s"
# Configure logging to write to port_log.txt on Desktop, set log level, format, and date format
logging.basicConfig(filename=log_file_path, level=logging.INFO, format=log_format, datefmt='%b %d %Y: %H:%M')

def log_message(message):
    """
    Logs a message to the port_log.txt file on Desktop.
    """
    logging.info(message)

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

os.chmod(log_file_path, 0o444)
# Example usage
log_login("Wayne Rooney")
log_user_message("Wayne Rooney", "Hello World!!!")
log_system_info("start executing the manifest")