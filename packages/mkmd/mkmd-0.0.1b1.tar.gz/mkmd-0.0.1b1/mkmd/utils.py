from __future__ import annotations
from typing import Optional

def _blank(text: str) -> bool:
    """
    Returns whether a line is empty or only
    consists of whitespace.
    """
    return not text or text.isspace()

def _url_escape(url: str) -> str:
    """
    Replace spaces from url with ``%20``.
    """
    return url.replace(" ", "%20")

#def escape(text: str) -> str:
#    # https://www.markdownguide.org/basic-syntax/#characters-you-can-escape

def italic(text: str) -> str:
    """Makes text italic."""
    return f"*{text}*"

def bold(text: str) -> str:
    """Makes text bold."""
    return f"**{text}**"

def bold_and_italic(text: str) -> str:
    """Makes text bold and italic."""
    return f"***{text}***"

def link(url: str, title: Optional[str] = None) -> str:
    """
    Adds a link.
    
    Parameters
    ----------
    url
        The url to redirect to.
    
    title
        Text to display instead of the url.
    """
    url = _url_escape(url)
    
    if title is None:
        return f"<{url}>"
    
    else:
        return f"[{title}]({url})"

def email(adress: str) -> str:
    """Adds an email."""
    return f"<{adress}>"

def refer(text: str, label: str) -> str:
    return f"[{text}][{label}]"
