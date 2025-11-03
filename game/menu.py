
from game import character
from game.game import GameState
from utils.utils import center_panel
from shop.objects import ITEM_REGISTRY
from shop.shop import Shop
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
import sys
import json
import os
import random
import keyboard

console = Console()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_name_lists():
    try:
        with open("json/banned_names.json", "r") as f:
            data = json.load(f)
            return data["banned"], data["ramdom"]
    except FileNotFoundError:
        console.print(Panel("⚠️ Fichier banned_names.json non trouvé", border_style="red"))
        return [], []
    except json.JSONDecodeError:
        console.print(Panel("⚠️ Erreur de lecture du fichier JSON", border_style="red"))
        return [], []


def check_name(name):
    banned_names, random_names = load_name_lists()

    if name.lower() in [banned.lower() for banned in banned_names]:
        random_name = random.choice(random_names)
        return random_name
    return name


def display_title(title, color="magenta"):
    console.print("\n")
    console.print(center_panel(f"[bold {color}]{title}[/bold {color}]", border_style=color))
    console.print("\n")


def show_welcome_screen():
    title_art = """
    ██╗     ███████╗ ██████╗ ███████╗███╗   ██╗██████╗ ███████╗ █████╗ 
    ██║     ██╔════╝██╔════╝ ██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗
    ██║     █████╗  ██║  ███╗█████╗  ██╔██╗ ██║██║  ██║█████╗  ███████║
    ██║     ██╔══╝  ██║   ██║██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██║
    ███████╗███████╗╚██████╔╝███████╗██║ ╚████║██████╔╝███████╗██║  ██║
    ╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
    """
    console.print(center_panel(title_art, border_style="purple4"))
    console.print(center_panel(Text("Bienvenue dans le monde des héros et des monstres !", style="bold gold1"), border_style="gold1"))
    print("🌟 Appuyez sur une touche pour commencer... ")

    event = keyboard.read_event(suppress=True)
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == 'esc':
            console.print(center_panel("👋 Au revoir, aventurier !", "red"))
            sys.exit()
        else:
            console.print(center_panel("🌟 Bienvenue jeune Aventurier !", "yellow"))


def save_game(player, state: GameState):
    save_data = {
        "player": {
            "name": player.name,
            "hp": player.hp,
            "hp_max": player.hp_max,
            "attack_value": player.attack_value,
            "defense_value": player.defense_value,
            "exp": player.exp,
            "level": player.level,
            "coins": player.coins,
            "inventory": [item.name for item in player.inventory],
        },
        "state": {
            "current_dungeon_index": state.current_dungeon_index,
            "current_floor_index": state.current_floor_index,
        },
    }

    with open("save_game.json", "w") as save_file:
        json.dump(save_data, save_file)

    console.print(center_panel("💾 Partie sauvegardée avec succès !", "green"))


def load_game():
    if not os.path.exists("save_game.json"):
        console.print(center_panel("❌ Aucune sauvegarde trouvée.", "red"))
        return None, None, None

    with open("save_game.json", "r") as save_file:
        save_data = json.load(save_file)

    player_data = save_data["player"]
    player = character.Character(
        player_data["name"],
        player_data["hp_max"],
        player_data["attack_value"],
        player_data["defense_value"],
        exp_reward=1,
        coins_reward=1,
    )

    player.hp = player_data["hp"]
    player.exp = player_data["exp"]
    player.level = player_data["level"]
    player.coins = player_data["coins"]
    player.inventory = [ITEM_REGISTRY[name]() for name in player_data["inventory"] if name in ITEM_REGISTRY]

    console.print(center_panel("⚔️ Partie chargée avec succès !", "green"))

    state_data = save_data.get("state", {"current_dungeon_index": 0, "current_floor_index": 0})
    return player, GameState(state_data["current_dungeon_index"], state_data["current_floor_index"])


def choose_character_class():
    display_title("Choisissez votre classe", "blue")

    classes = ["Archer", "Voleur", "Guerrier", "Mage"]
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("N°", justify="center", style="dim")
    table.add_column("Classe", style="bold green")

    for i, c in enumerate(classes, 1):
        table.add_row(str(i), c)
    console.print(Align.center(table))

    while True:
        choice = input("🎯 Entrez le numéro de votre classe : ")
        if choice in ["1", "2", "3", "4"]:
            return ["Archer", "Voleur", "Guerrier", "Mage"][int(choice) - 1]
        console.print(center_panel("Classe invalide. Réessayez.", "red", box.ROUNDED))


def create_main_character(name, char_class):
    classes = {
        "Archer": character.Archer(name, 30, 10, 5, 1, 1),
        "Voleur": character.Thief(name, 32, 10, 4, 1, 1),
        "Guerrier": character.Warrior(name, 35, 12, 8, 1, 1),
        "Mage": character.Mage(name, 30, 12, 3, 1, 1),
    }
    return classes[char_class]


def show_main_menu():
    display_title("🌟 Les Légendes d'Etheria 🌟")
    menu = [
        ("1", "Nouvelle partie", "green"),
        ("2", "Charger une partie", "yellow"),
        ("3", "Quitter", "red"),
    ]
    for key, text, color in menu:
        console.print(Align.center(Text(f"{key}. {text}", style=f"bold {color}")))
    console.print("\n")


def select_character():
    while True:
        show_main_menu()
        choice = input("🎮 Entrez votre choix : ")

        if choice == "1":
            name = input("🧙 Nom de votre héros : ")
            name = check_name(name)
            char_class = choose_character_class()
            player = create_main_character(name, char_class)
            text = Text.assemble(
                "Bienvenue chère ",
                (f"{name}", "bold yellow"),
                " ! OH ! Mais vous êtes un ",
                (f"{char_class}", "bold cyan"),
                " !",
                style="green"
            )
            console.print(center_panel(text))
            return player, GameState(0, 0)

        elif choice == "2":
            player, state = load_game()
            if player:
                return player, state

        elif choice == "3":
            console.print(center_panel("👋 Au revoir, aventurier !", "red"))
            sys.exit()

        else:
            console.print(center_panel("Choix invalide. Entrez 1, 2 ou 3.", "red"))


def show_game_menu():
    display_title("🎮 Menu Principal", "magenta")
    options = [
        ("1", "Accéder au Donjon", "green"),
        ("2", "Magasin (Shop)", "yellow"),
        ("3", "Sauvegarder la partie", "cyan"),
        ("4", "Quitter", "red"),
    ]
    for key, text, color in options:
        console.print(Align.center(Text(f"{key}. {text}", style=f"bold {color}")))
    console.print("\n")


def select_option(player, state: GameState):
    while True:
        show_game_menu()
        choice = input("🗝️ Entrez votre choix : ")

        if choice == "1":
            clear_terminal()
            console.print(center_panel("⚔️ Vous entrez dans le donjon...", "green"))
            break

        elif choice == "2":
            console.print(center_panel("🏪 Bienvenue au magasin !", "yellow"))
            shop = Shop()
            shop.display_shop(player)

        elif choice == "3":
            save_game(player, state)

        elif choice == "4":
            console.print(center_panel("👋 Au revoir, aventurier !", "red"))
            sys.exit()

        else:
            console.print(center_panel("❌ Choix invalide. Entrez 1, 2, 3 ou 4.", "red"))


def show_death_menu():
    clear_terminal()
    display_title("💀 Vous êtes mort ! 💀", "red")
    console.print(Align.center(Text("1. Recommencer", style="bold green")))
    console.print(Align.center(Text("2. Quitter", style="bold red")))

    while True:
        choice = input("☠️ Entrez votre choix : ")
        if choice == "1":
            return "restart"
        elif choice == "2":
            console.print(center_panel("Fermeture du jeu...", "red"))
            sys.exit()
        console.print(center_panel("Choix invalide. Entrez 1 ou 2.", "red"))
