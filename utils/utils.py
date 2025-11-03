from rich.align import Align
from rich import box
from rich.panel import Panel
from rich.text import Text

def strip_rich_markup(text: str) -> str:
    return Text.from_markup(text).plain

def center_panel(text, border_style, box_style=box.DOUBLE):
    return Align.center(Panel(text, border_style=border_style, box=box_style))

def clean_emoji(s: str):
    return s.replace("\ufe0f", "")


def box_combat(text, border_style, title=None, padding=None, box_style=box.SQUARE):
    kwargs = {}
    if title is not None:
        kwargs["title"] = title
    if padding is not None:
        kwargs["padding"] = padding
    return Align.left(Panel(text, border_style=border_style, box=box_style, **kwargs))

def box_damages(text, border_style, title=None, padding=None, box_style=box.SQUARE):
    kwargs = {"title": title} if title else {}
    return Align.center(Panel(text, border_style=border_style, padding=padding, box=box_style, **kwargs))
