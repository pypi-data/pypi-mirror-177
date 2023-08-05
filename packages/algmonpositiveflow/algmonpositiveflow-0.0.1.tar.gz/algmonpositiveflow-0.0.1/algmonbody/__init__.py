""" algmon body
"""
import os
from .core import Body

print("Welcome to USE the Algmon Body")
with open(os.path.join(os.path.dirname(__file__), "version.txt")) as f:
    version = f.read().strip()

__all__ = [
	"Body",
]

__version__ = version
