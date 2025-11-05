from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from utils.asciiart import print_art, get_art
from utils.utils import center_panel, clean_emoji
from game.quests import quests
from items.shop import Shop
import random
import time

console = Console()


class NPC:
    def __init__(self, name, art_key, greetings):
        self.name = name
        self.art = get_art(art_key) or get_art("npc_villageois") or ""
        self.greetings = greetings
        self.art_key = art_key


VILLAGE_NPCS = [
    NPC("Vieux Villageois", "npc_villageois", [
        "Bonjour jeune aventurier !",
        "Le village a besoin de héros comme vous !",
        "Faites attention aux monstres qui rôdent..."
    ]),
    NPC("Marchand Itinérant", "npc_marchand", [
        "Salut l'ami ! J'ai les meilleures affaires !",
        "Mes prix sont imbattables !",
        "Venez voir ma marchandise !"
    ]),
    NPC("Alchimiste Mystérieux", "npc_alchimiste", [
        "Hmm... Des ingrédients rares vous intéressent ?",
        "J'ai besoin de matériaux pour mes potions...",
        "Les zombies et squelettes ont ce qu'il me faut !"
    ]),
    NPC("Forgeron Burin", "npc_forgeron", [
        "Hé ! Vous cherchez des armes ?",
        "J'ai besoin d'os pour renforcer mes créations !",
        "Les squelettes ont de bons os pour forger..."
    ]),
    NPC("Capitaine des Gardes", "npc_garde", [
        "Salut soldat ! Le village est en danger !",
        "Nous avons besoin d'aide pour éliminer les menaces !",
        "Votre aide serait la bienvenue !"
    ]),
    NPC("Vieille Sage", "npc_villageois", [
        "Bienvenue, jeune héros...",
        "Les temps sont sombres, mais vous pouvez changer cela.",
        "Accomplissez des quêtes et gagnez en puissance !"
    ]),
]


def get_random_npc():
    return random.choice(VILLAGE_NPCS)


def get_random_quest():
    incomplete_quests = [q for q in quests if not q.completed]
    if incomplete_quests:
        return random.choice(incomplete_quests)
    return None


def encounter_npc(player):
    npc = get_random_npc()
    quest = get_random_quest()
    
    village_arts = ["villagetwo", "villagethree", "villagefour", "villagefive"]
    random_village_art = random.choice(village_arts)
    
    console.print("\n")
    print_art(random_village_art, title="🏘️ Vous vous promenez dans le village...", border_style="blue")
    time.sleep(0.5)
    
    npc_text = Text()
    npc_text.append("\n", style="cyan")
    npc_text.append(npc.art, style="cyan")
    npc_text.append("\n\n", style="cyan")
    npc_text.append(f"{npc.name}", style="bold yellow")
    npc_text.append("\n\n")
    npc_text.append(f"{random.choice(npc.greetings)}", style="cyan")
    
    console.print(Panel(
        npc_text,
        title="[bold cyan]👤 Rencontre[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2)
    ))
    
    time.sleep(1)
    
    if quest:
        quest_text = Text()
        quest_text.append(f"\n📜 {npc.name} vous confie une quête !\n\n", style="bold yellow")
        quest_text.append(f"{quest.name}\n", style="bold cyan")
        quest_text.append(f"{quest.description}\n\n", style="white")
        quest_text.append(f"Objectif : {quest.objective}", style="dim")
        
        console.print(Panel(
            Align.center(quest_text),
            title="[bold yellow]📜 Nouvelle Quête ![/bold yellow]",
            border_style="yellow",
            box=box.DOUBLE,
            padding=(1, 2)
        ))
        
        console.print("\n")
    else:
        console.print(center_panel(
            "✨ Vous avez déjà toutes les quêtes disponibles !",
            "bold green"
        ))
        console.print("\n")

def show_village_menu(player):
    console.print("\n")
    
    menu_options = [
        ("1", "Se promener dans le village", "purple4"),
        ("2", "Aller au magasin", "gold1"),
        ("3", "Partir à l'aventure", "dark_red")
    ]
    
    console.print("\n")
    for key, text, color in menu_options:
        console.print(Align.center(Text(f"{key}. {text}", style=f"bold {color}")))
    console.print("\n")


def village_menu(player, state):
    while True:
        show_village_menu(player)
        choice = input("🎯 Votre choix : ").strip()
        
        if choice == "1":
            encounter_npc(player)
        elif choice == "2":
            console.print("\n")
            shop = Shop()
            shop.display_shop(player)
            input("\n👆 Appuyez sur Entrée pour continuer...")
        elif choice == "3":
            console.print(center_panel(
                "[bold green]⚔️ Vous partez à l'aventure ![/bold green]",
                border_style="green"
            ))
            console.print("\n")
            return "adventure"
        elif choice == "4":
            return "menu"
        else:
            console.print(center_panel(
                "[red]❌ Choix invalide. Entrez 1, 2, 3 ou 4.[/red]",
                border_style="red"
            ))
            time.sleep(1)


__all__ = ["village_menu", "encounter_npc"]
