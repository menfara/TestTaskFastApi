# Standard Library
import logging
import pathlib

# Third Party Library
from loguru import logger

# Application Library
from .conf import settings

__all__ = [
	'get_logger',
]

path = pathlib.Path(settings.log_dir).resolve()
path.mkdir(parents=True, exist_ok=True)

logger.add(
	path / settings.log_filename,
	rotation=f'{settings.log_rotation} MB',
	retention=f'{settings.log_retention} days',
	level=logging.getLevelName(settings.log_level),
)


def get_logger():
	return logger
