import importlib.metadata
from tesseract.server import serve

__version__ = importlib.metadata.version("tesseract-sdk")
__all__ = ['serve']
