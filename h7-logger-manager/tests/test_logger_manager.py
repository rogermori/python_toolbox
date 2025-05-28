import unittest
import os
import sys
from unittest.mock import patch, MagicMock
import logging

# Add the src directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from h7_logger_manager import LoggerManager

class TestLoggerManager(unittest.TestCase):
    
    @patch('h7_logger_manager.logger_manager.EnvManager')
    @patch('h7_logger_manager.logger_manager.find_logs_folder')
    @patch('h7_logger_manager.logger_manager.os.path.exists')
    @patch('h7_logger_manager.logger_manager.os.makedirs')
    def test_setup_logger(self, mock_makedirs, mock_exists, mock_find_logs, mock_env_manager):
        """Test that setup_logger creates and returns a logger"""
        # Setup mocks
        mock_exists.return_value = True
        mock_find_logs.return_value = "/fake/logs/dir"
        mock_env_manager.get_required_env_var.return_value = "test_logger"
        mock_env_manager.get_optional_env_var.return_value = "false"
        
        # Clear any existing loggers
        LoggerManager._loggers = {}
        
        # Test logger creation
        logger = LoggerManager.setup_logger()
        
        # Verify logger was created correctly
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "test_logger")
        self.assertEqual(len(logger.handlers), 2)  # Should have console and file handlers
        
        # Test that calling again returns the same logger
        logger2 = LoggerManager.setup_logger()
        self.assertIs(logger2, logger)
    
    @patch('h7_logger_manager.logger_manager.EnvManager')
    @patch('h7_logger_manager.logger_manager.find_logs_folder')
    @patch('h7_logger_manager.logger_manager.os.path.exists')
    @patch('h7_logger_manager.logger_manager.os.makedirs')
    def test_setup_logger_with_custom_name(self, mock_makedirs, mock_exists, mock_find_logs, mock_env_manager):
        """Test that setup_logger works with a custom logger name"""
        # Setup mocks
        mock_exists.return_value = False  # Test directory creation path
        mock_find_logs.return_value = "/fake/logs/dir"
        mock_env_manager.get_optional_env_var.return_value = "true"  # Debug mode on
        
        # Clear any existing loggers
        LoggerManager._loggers = {}
        
        # Test logger creation with custom name
        logger = LoggerManager.setup_logger("custom_logger", "custom_prefix")
        
        # Verify logger was created correctly
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "custom_logger")
        mock_makedirs.assert_called_once_with("/fake/logs/dir")

if __name__ == '__main__':
    unittest.main()
