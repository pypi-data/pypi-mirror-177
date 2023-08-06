import re
from typing import Iterable


def normalize_path(path: str) -> str:
    """Normalize a given path by ensuring it starts with a slash and does not end with a slash.

    Args:
        path: Path string

    Returns:
        Path string
    """
    path = path.strip("/")
    path = "/" + path
    return re.sub("//+", "/", path)


def join_paths(paths: Iterable[str]) -> str:
    """Normalize and joins path fragments.

    Args:
        paths: An iterable of path fragments.

    Returns:
        A normalized joined path string.
    """
    return normalize_path("/".join(paths))
