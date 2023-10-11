import logging

def configure_logger(file_name, level=logging.INFO):
    # Set the desired log level
    logging.basicConfig(level=level)

    # Create a logger with the file name
    logger = logging.getLogger(file_name)

    # Create a handler to save logs to a file
    file_handler = logging.FileHandler(file_name + '.log')

    # Define the log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)

    return logger

# Example usage of the function

my_logger = configure_logger('my_log_file', level=logging.INFO)

my_logger.debug('This is a debug message')
my_logger.info('This is an information message')
my_logger.warning('This is a warning message')
my_logger.error('This is an error message')
my_logger.critical('This is a critical message')
