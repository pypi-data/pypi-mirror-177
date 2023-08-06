"""
Palign provides functions for aligning text to be rendered via Pillow.
"""

from importlib.resources import files

with files(__package__).joinpath("VERSION").open("r") as t:
    version = t.readline().strip()

__all__ = [
    "version",
]
