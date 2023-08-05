""" algmon brain
"""
import os
from .core import Brain

print("Welcome to USE the Algmon Brain")
with open(os.path.join(os.path.dirname(__file__), "version.txt")) as f:
    version = f.read().strip()

__all__ = [
	"Brain",
]

__version__ = version

