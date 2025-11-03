from rich.align import Align
from rich import box
from rich.panel import Panel
from rich.text import Text

def strip_rich_markup(text: str) -> str:
    return Text.from_markup(text).plain

def center_panel(text, border_style="purple4", box_style=box.DOUBLE):
    return Align.center(Panel(text, border_style=border_style, box=box_style))