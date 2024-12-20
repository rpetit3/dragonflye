import logging

import rich
import rich.console
import rich_click as click
from rich import print
from rich.logging import RichHandler


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Logger object.
    """
    return logging.getLogger(name)


class Logger(logging.Logger):

    def __init__(
        self,
        name: str,
        silent: bool,
        verbose: bool,
        show_time: bool = False,
        show_level: bool = False,
    ):
        """
        Initialize the logger.

        Args:
            name (str): Name of the logger.
            silent (bool): Suppress all output.
            verbose (bool): Enable debug output.
            show_time (bool, optional): Show the time in the log. Defaults to False, unless verbose is enabled.
            show_level (bool, optional): Show the log level in the log. Defaults to False, unless verbose is enabled.

        Returns:
            None
        """
        super().__init__(
            name,
            logging.ERROR if silent else logging.DEBUG if verbose else logging.INFO,
        )
        self.addHandler(
            RichHandler(
                rich_tracebacks=True,
                console=rich.console.Console(stderr=True),
                show_time=True if verbose else show_time,
                show_level=True if verbose else show_level,
                show_path=False,
            )
        )

    def info(self, msg, *args, **kwargs):
        super().info(f"[{self.name}] {msg}")

    def debug(self, msg, *args, **kwargs):
        super().debug(f"[{self.name}] {msg}")

    def error(self, msg, *args, **kwargs):
        super().error(f"[{self.name}] {msg}")

    def warning(self, msg, *args, **kwargs):
        super().warning(f"[{self.name}] {msg}")

    def critical(self, msg, *args, **kwargs):
        super().critical(f"[{self.name}] {msg}")
