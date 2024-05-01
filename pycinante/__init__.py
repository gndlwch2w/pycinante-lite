from __future__ import annotations

import os
import re
import json
from typing import Iterable, Any

__version__ = "0.0.1"

def listify(obj: Any) -> list:
    """Convert an object of any type into a list.

    Note that If the object is iterable and not a string, all elements within the iterable
    will be appended to a list, otherwise the object will be directly appended to a list.

    Examples:
        >>> # Convert an iterable object into a list
        >>> listify(range(10))
        >>> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> # Convert a non-iterable object into a list
        >>> listify("https://www.google.com")
        >>> ["https://www.google.com"]
    """
    if isinstance(obj, list):
        return obj
    if not isinstance(obj, str) and isinstance(obj, Iterable):
        return list(obj)
    return [obj]

def save_json(data: Any, pathname: str, encoding: str = "utf-8", **kwargs: Any) -> None:
    """Save a serializable python object to a json file.

    Examples:
        >>> orders = [{"name": "Harry Potter", "price": 19.3, "unit": "dollars"}]
        >>> save_json(orders, "orders.json", indent=2)
    """
    with open(pathname, "w", encoding=encoding) as fp:
        json.dump(data, fp, **kwargs)

def load_json(pathname: str, encoding: str = "utf-8", **kwargs: Any) -> object:
    """Load a json file to a python object.

    Examples:
        >>> orders = load_json("orders.json")
        >>> orders
        [{"name": "Harry Potter", "price": 19.3, "unit": "dollars"}]
    """
    with open(pathname, "r", encoding=encoding) as fp:
        return json.load(fp, **kwargs)

def get_filename(pathname: str) -> str:
    """Return the filename of a pathname without the extension.

    Examples:
        >>> get_filename("/workspace/pycinante-lite/__init__.py")
        '__init__'
    """
    return os.path.basename(os.path.splitext(pathname)[0])

def get_ext(pathname: str) -> str:
    """Return the extension of a pathname without the filename.

    Examples:
        >>> get_filename("/workspace/pycinante-lite/__init__.py")
        '.py'
    """
    return os.path.splitext(pathname)[1]

def normalize_path(pathname: str, rep: str = "") -> str:
    """Replace all the invalid characters from a pathname with the char `rep`.

    Examples:
        >>> normalize_path('A survey: Code is cheap, show me the code.pdf')
        'A survey Code is cheap, show me the code.pdf'
    """
    return re.sub(re.compile(r'[<>:"/\\|?*\x00-\x1F\x7F]'), rep, pathname)

class PathBuilder(object):
    """A pathname builder for easily constructing a pathname by the operation `/` and `+`.

    Examples:
        >>> p = PathBuilder("/", "tmp", "pycinante-lite")
        >>> p / "pycinante" + "__init__.py"
        '/tmp/pycinante-lite/pycinante/__init__.py'
    """

    def __init__(self, *names: str) -> None:
        self.path = str(os.path.join(*(names or ('.',))))
        os.makedirs(self.path, exist_ok=True)

    def __truediv__(self, pathname: str) -> 'PathBuilder':
        """Append a sub-pathname to the original pathname and return a new pathname instance
        with the added sub-pathname.
        """
        return PathBuilder(os.path.join(self.path, pathname))

    def __add__(self, basename: str) -> str:
        """Append a basename to the original pathname and return the full pathname string
        after adding the basename.
        """
        return os.path.join(self.path, basename)
