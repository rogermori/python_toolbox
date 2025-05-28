import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from h7_file_finder import find_logs_folder
from h7_env_manager import EnvManager

class LoggerManager:
    """
    Centralized logging manager for the application.
    Provides methods to set up and retrieve loggers with consistent configuration.
    """

    # Dictionary to store loggers by name to avoid recreating them
    _loggers = {}

    @classmethod
    def setup_logger(cls, logger_name=None, log_file_prefix=None):
        """
        Set up and return a logger with the specified name.
        If a logger with this name already exists, return the existing logger.

        Args:
            logger_name (str): Name of the logger to create or retrieve
            log_file_prefix (str, optional): Prefix for the log file name.
                                           If None, uses logger_name

        Returns:
            logging.Logger: Configured logger object
        """
        debug_mode = EnvManager.get_optional_env_var("DEBUG_MODE", "false").lower() == "true"
        if not debug_mode or logger_name is None:
            logger_name = EnvManager.get_required_env_var('LOGGER_NAME')

        # If logger already exists, return it
        if logger_name in cls._loggers:
            return cls._loggers[logger_name]

        # Create logs directory if it doesn't exist
        logs_dir = find_logs_folder()
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # Create logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # Only add handlers if the logger doesn't have any
        if not logger.handlers:
            # Create formatter with timestamp
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # Create console handler with a higher log level
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)

            # Create file handler which logs even debug messages
            timestamp = datetime.now().strftime('%Y%m%d')
            file_prefix = log_file_prefix if log_file_prefix else logger_name
            log_file = os.path.join(logs_dir, f'{file_prefix}_{timestamp}.log')
            file_handler = RotatingFileHandler(
                log_file, maxBytes=5 * 1024 * 1024, backupCount=10, encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            # Add the handlers to the logger
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)

        # Store logger for future use
        cls._loggers[logger_name] = logger

        return logger
