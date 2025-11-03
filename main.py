import time
import shutil
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.rule import Rule
from rich import box

from game import menu, game, character

console = Console()


def display_banner(title: str, subtitle: str = "") -> None:
    width = shutil.get_terminal_size().columns
    
    title_text = Text.assemble(
        ("✨ ", "gold1"),
        (title, "bold magenta"),
        (" ✨", "gold1")
    )

    if subtitle:
        subtitle_text = Text(subtitle, style="gold1")
        content = Align.center(Text.assemble(title_text, "\n", subtitle_text), vertical="middle", width=width)
    else:
        content = Align.center(title_text, vertical="middle", width=width)

    panel = Panel(
        content,
        box=box.DOUBLE,
        border_style="purple4",
        padding=(1, 8),
        width=min(width - 4, 100),
    )
    
    console.print("\n")
    console.print(Align.center(panel, vertical="middle"))
    console.print("\n")


def display_centered_panel(message: str, style: str = "gold1", border_style: str = "purple4") -> None:
    width = shutil.get_terminal_size().columns
    
    panel = Panel(
        Align.center(Text(message, style=style), vertical="middle"),
        border_style=border_style,
        box=box.ROUNDED,
        width=min(width - 6, 100),
        padding=(1, 4)
    )
    
    console.print("\n")
    console.print(Align.center(panel, vertical="middle"))
    console.print("\n")


def display_main_menu() -> None:
    console.print("\n")
    console.print(Align.center(Rule(style="gold1"), vertical="middle"))
    console.print(Align.center(Text("⚔️ Choisis ta voie ⚔️", style="bold magenta"), vertical="middle"))
    console.print(Align.center(Rule(style="gold1"), vertical="middle"))
    time.sleep(0.3)

def handle_game_loop(player, state) -> None:
    while True:
        display_main_menu()
        menu.select_option(player, state)
        game.start_game(player, state)


def main() -> None:
    """Point d'entrée principal du jeu."""
    with console.screen():
        menu.clear_terminal()
        
        display_banner("Chroniques du Donjon", "Un court voyage épique t'attend...")
        time.sleep(0.8)

        menu.show_welcome_screen()
        
        player, state = menu.select_character()

        if player is None:
            display_centered_panel(
                "Aucun personnage n'a été sélectionné.", 
                style="bold red", 
                border_style="red"
            )
            return

        try:
            handle_game_loop(player, state)
        except KeyboardInterrupt:
            display_centered_panel(
                "Au revoir, aventurier. Que tes quêtes continuent !", 
                style="gold1", 
                border_style="purple4"
            )
        except Exception as e:
            display_centered_panel(
                f"Une erreur inattendue s'est produite : {e}", 
                style="bold red", 
                border_style="red"
            )


if __name__ == "__main__":
    main()