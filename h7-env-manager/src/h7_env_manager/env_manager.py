import os

from h7_file_finder import find_env_file

# Track whether dotenv has been loaded
_dotenv_loaded = False


class EnvManager:
    """Manages environment variables for the application."""

    @classmethod
    def _ensure_dotenv_loaded(cls):
        """Ensure .env file is loaded only once."""
        global _dotenv_loaded

        if not _dotenv_loaded:
            from dotenv.main import load_dotenv

            dotenv_path = find_env_file()
            load_dotenv(dotenv_path, override=True)
            _dotenv_loaded = True

    @classmethod
    def get_required_env_var(cls, key: str) -> str:
        """Get a required environment variable.

        Args:
            key: The name of the environment variable
        Returns:
            The value of the environment variable
        Raises:
            ValueError: If the environment variable is not found

        """
        cls._ensure_dotenv_loaded()
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Environment variable '{key}' not found")
        return value

    @classmethod
    def get_optional_env_var(cls, key: str, default: str = None) -> str:
        """Get an optional environment variable with a default value.

        Args:
            key: The name of the environment variable
            default: The default value to return if the variable is not found
        Returns:
            The value of the environment variable or the default value
        """
        cls._ensure_dotenv_loaded()
        value = os.getenv(key)  # Only the key is passed here
        if value is None:
            return default  # Default handling happens here, not in os.getenv
        return value

    @classmethod
    def get_optional_bool_env_var(cls, key: str, default: bool=False) -> bool:
        """
        Retrieves a boolean environment variable.

        Args:
            key: The name of the environment variable
            default: Default value to return if the environment variable is not set
        Returns:
            The boolean value of the environment variable or the default value
        """
        cls._ensure_dotenv_loaded()
        value = cls.get_optional_env_var(key)

        # Return default if value is None or empty string
        if not value:
            return default

        # Convert string to boolean
        return value.lower() == "true"
