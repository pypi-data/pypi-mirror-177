"""
nvalues is a Python package for working with n-dimensional volumes of data.
"""

from importlib.resources import files

from nvalues.values import Values

with files(__package__).joinpath("VERSION").open("r") as t:
    version = t.readline().strip()

__all__ = [
    "Values",
]
