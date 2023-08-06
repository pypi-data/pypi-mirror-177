from __future__ import annotations

import inspect
import io
from os import PathLike
from pathlib import Path
import textwrap
from types import TracebackType
from typing import Any, Optional, TextIO

from . import utils

class Markdown:
    """
    Class that holds all Markdown content. All ``add_*``
    methods return the object itself so these methods can
    be chained. For example::
        
        md = Markdown()
        (md
            .add_heading("Hello")
            .add_paragraph("Lorem ipsum dolor sit amet.")
            .add_horizontal_rule()
            .add_codeblock("import mkmd", language = "python")
            .save("lorem-ipsum.md")
        )
    
    Attributes
    ----------
    lines
        Lines of the Markdown document.
    """
    def __init__(
        self,
        path: Optional[str | PathLike[str] | TextIO] = None,
        width: Optional[int] = None,
    ):
        """
        Parameters
        ----------
        path
            This should only be set when using as a context
            manager. Otherwise use the :meth:`save` method
            and provide the path there.
        
        width
            The maximum amount of characters a line can contain.
        """
        self.lines: list[str] = []
        self._path = path
        self._width = width
    
    @classmethod
    def from_string(
        cls,
        text: str,
        *args: Any,
        **kwargs: Any,
    ) -> Markdown:
        """
        Loads document from a string.
        
        Parameters
        ----------
        text
            Markdown document as a string.
        
        args
            Positional arguments passed to constructor.
        
        kwargs
            Keyword arguments passed to constructor.
        """
        md = cls(*args, **kwargs)
        md.lines.extend(text.splitlines())
        
        return md
    
    @classmethod
    def from_file(
        cls,
        path: str | PathLike[str] | TextIO,
        *args: Any,
        **kwargs: Any,
    ) -> Markdown:
        """
        Loads document from a file.
        
        Parameters
        ----------
        path
            Markdown document as path or file object.
        
        args
            Positional arguments passed to constructor.
        
        kwargs
            Keyword arguments passed to constructor.
        """
        if isinstance(path, io.TextIOBase):
            return cls.from_string(path.read())
        return cls.from_string(
            Path(path).read_text(),
            path = path,
            *args,
            **kwargs,
        )
    
    def __str__(self) -> str:
        return "\n".join(self.lines)
    
    def __enter__(self) -> Markdown:
        if self._path is None:
            raise ValueError("no path specified")
        return self
    
    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> None:
        self.save(self._path)
    
    def save(self, path: str | PathLike[str] | TextIO) -> None:
        """
        Writes the Markdown document to a file. Alternatively
        a context manager may be used.
        
        Parameters
        ----------
        path
            A file-like object or path to save contents
            to.
            
        Example
        -------
        .. code-block:: python
           
           # these are all equivalent:
           
           with open("document.md", "w") as f:
               md.save(f)
           
           md.save("document.md")
           
           md.save(Path("document.md"))
        """
        if isinstance(path, io.TextIOBase):
            path = path.write(str(self))
            return
        
        path = Path(path)
        path.write_text(str(self))
    
    def _wrap(
        self,
        text: str,
    ) -> str:
        """
        Wraps the lines so they do not go across the
        specified maximum width.
        
        Parameters
        ----------
        text
            Text to wrap.
        """
        return text if self._width is None else textwrap.fill(
            text,
            drop_whitespace = False,
            break_on_hyphens = False,
            width = self._width
        )
    
    def add_lines(
        self,
        *lines: Optional[str],
    ) -> Markdown:
        """
        Adds lines.
        
        .. attention::
           This method should only used by subclasses. Usually
           the wrapper method :meth:`add_paragraph` does the
           job.
        
        Parameters
        ----------
        lines
            Lines to add. ``None`` will be skipped.
        """
        self.lines.extend(self._wrap(l) for l in lines if l is not None)
        return self
    
    def add_heading(
        self,
        text: str,
        level: int = 1,
        alternate: bool = True,
    ) -> Markdown:
        """
        Parameters
        ----------
        text
            The content of the heading.
        
        level
            A heading level between 1 and 7 inclusive.
        
        alternate
            Uses hyphens and equal signs respectively instead
            of number signs for heading level 1 and 2.
        """
        if level not in range(1, 7):
            raise ValueError("level must be in range 1..=6")
        
        if alternate and level in [1, 2]:
            lines = [
                text.strip(),
                ("=" if level == 1 else "-") * len(text)
            ]
        
        else:
            lines = [f"{'#' * level} {text}"]
        
        self.add_paragraph(*lines)
        return self
    
    def add_paragraph(
        self,
        *lines: Optional[str],
        wrapped: bool = False,
    ) -> Markdown:
        """
        Adds a paragraph.
        
        Parameters
        ----------
        lines
            Lines to add. ``None`` will be skipped.
        
        wrapped
            Removes indention of each line.
        """
        result_lines = []
        for line in lines:
            if line is None:
                continue
            
            if wrapped:
                text = inspect.cleandoc(line)
                result_lines.extend(text.splitlines())
                continue
            
            result_lines.append(line)
        
        self.add_lines(
            "" if self.lines and not utils._blank(self.lines[-1]) else None,
            *result_lines,
            ""
        )
        
        return self
    
    def add_codeblock(
        self,
        text: str,
        language: Optional[str] = None,
        wrapped: bool = True,
    ) -> Markdown:
        """
        Adds a code block.
        
        Parameters
        ----------
        text
            The content of the code block.
        
        language
            The programming language of the content.
        
        wrapped
            Interprets ``text`` in a docstring-like
            syntax. This calls ``inspect.cleandoc`` on
            ``text``.
        """
        # TODO: escape ```
        # TODO: ignore width
        
        self.add_paragraph(
            "```" + ("" if language is None else language),
            inspect.cleandoc(text) if wrapped else text,
            "```",
        )
        
        return self
    
    def add_horizontal_rule(
        self,
        style: str = "-",
        width: Optional[int] = None,
    ) -> Markdown:
        """
        Adds a horizontal rule
        
        Parameters
        ----------
        style
            What characters to use for the horizontal rule.
            One of ``*``, ``-`` or ``_``.
        
        width
            The width of the horizontal rule. Defaults to
            :attr:`width` if provided otherwise `20`.
        """
        if style not in "*-_":
            raise ValueError("style must be '*', '-' or '_'")
        
        if width is None:
            if self._width is None:
                width = 20
            
            else:
                width = self._width
        
        self.add_paragraph(style * width)
        return self
    
    def add_reference(
        self,
        label: str,
        url: str,
        title: Optional[str] = None,
    ) -> Markdown:
        """
        Adds a reference.
        
        Parameters
        ----------
        label
            The unique lable of the reference.
        
        url
            The url to link to.
        
        title
            An optional title to use.
        """
        self.add_lines(
            "",
            f"[{label}]: <{utils._url_escape(url)}>" + ("" if title is None else f' "{title}"')
        )
        return self
    
    def add_image(
        self,
        alt_text: str,
        path_or_url: str | Path,
        title: Optional[str] = None,
        link: Optional[str] = None,
    ) -> Markdown:
        """
        Adds an image.
        
        Parameters
        ----------
        alt_text
            The alternative text to display.
        
        path_or_url
            Path or url of image to display.
            
            .. attention::
               Paths are relative from the markdown document,
               not from the python file.
        
        title
            An optional title to use.
        
        link
            Optional url to link to.
        """
        text = f"![{alt_text}][{path_or_url}" + ("" if title is None else f' "{title}"') + "]"
        
        if link is not None:
            text = utils.link(text, link)
        
        self.add_paragraph(text)
        return self
    
    def add_unordered_list(
        self,
        *items: str,
        style: str = "-",
    ) -> Markdown:
        """
        Adds an unordered list.
        
        Parameters
        ----------
        items
            All list items.
        
        style
            What characters to use list.
            One of ``-``, ``*`` or ``+``.
        """
        # TODO: initial indent when width is reached
        if style not in "-*+":
            raise ValueError("style must be '-', '*' or '+'")
        
        self.add_paragraph(*(f"{style} {item}" for item in items))
        return self
    
    def add_ordered_list(
        self,
        *items: str,
    ) -> Markdown:
        """
        Adds an ordered list.
        
        Parameters
        ----------
        items
            All list items.
        """
        self.add_paragraph(*(
            f"{number}. {item}" for number, item in enumerate(items, start = 1)
        ))
        return self
    