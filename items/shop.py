from items.objects import (
    WoodenShield, BoneShield, IronShield, CopperShield,
    WoodenSword, IronSword, DiamondSword, Excalibur,
    LeatherArmor, IronArmor, Chainmail, EndiumArmor,
    FireStick, IceStick, WindStick, UltimateStick,
    WoodenDagger, SilverDagger, CopperDagger, GoldDagger,
    ClassicBow, LongBow, Crossbow, TripleBow,
    ManaCape, HealCape, DefenseCape, UltimateCape,
    Potion, SuperPotion, HyperPotion, MaxPotion
)
from utils.utils import center_panel, clean_emoji
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

console = Console()


def display_category(title: str, items: list):
    console.print("\n")
    console.print(Align.center(
        Panel(f"[bold magenta]{title}[/bold magenta]", border_style="purple4", box=box.DOUBLE)
    ))

    table = Table(
        show_header=True,
        header_style="bold gold1",
        box=box.ROUNDED,
        title=f"[bold cyan]{title} disponibles[/bold cyan]"
    )
    table.add_column("N°", style="dim", justify="center", width=6)
    table.add_column("Nom", style="bold yellow")
    table.add_column("Prix (🪙)", justify="center", style="bold green")

    for i, item in enumerate(items, start=1):
        table.add_row(str(i), item.name, str(item.price))

    table.add_row("0", "🔙 Retour", "")

    console.print(Align.center(table))
    console.print("\n")


CATEGORIES = {
    clean_emoji("🛡️ Boucliers"): [WoodenShield, BoneShield, IronShield, CopperShield],
    clean_emoji("⚔️ Épées"): [WoodenSword, IronSword, DiamondSword, Excalibur],
    "🦾 Armures": [LeatherArmor, IronArmor, Chainmail, EndiumArmor],
    "✨ Bâtons magiques": [FireStick, IceStick, WindStick, UltimateStick],
    "🔪 Dagues": [WoodenDagger, SilverDagger, CopperDagger, GoldDagger],
    "🏹 Arcs": [ClassicBow, LongBow, Crossbow, TripleBow],
    "🧥 Capes": [ManaCape, HealCape, DefenseCape, UltimateCape],
    "🧪 Potions": [Potion, SuperPotion, HyperPotion, MaxPotion],
}


class Shop:
    def __init__(self):
        self.items = [cls() for cat in CATEGORIES.values() for cls in cat]

    def display_shop(self, player):
        console.print("\n")

        while True:
            if player.coins <= 0:
                console.print(center_panel("💸 Vous n'avez plus de pièces. Le magasin se ferme...", "red"))
                break

            coins_panel = Panel(
                Align.center(Text(f"💰 Votre solde : {player.coins} 🪙", style="gold1")),
                border_style="gold1"
            )
            console.print(Align.center(coins_panel))
            console.print(Align.center(
                Panel("🏪 [bold magenta]Bienvenue dans le magasin ![/bold magenta]",
                      border_style="gold1", box=box.DOUBLE)
            ))

            if not self.select_category(player):
                break

    def select_category(self, player):
        console.print("\n")
        console.print(center_panel(clean_emoji("🗂️ [bold cyan]Choisissez une catégorie[/bold cyan]"), "purple4"))

        table = Table(show_header=True, header_style="bold gold1", box=box.ROUNDED,
                      title="[bold magenta]Catégories disponibles[/bold magenta]")
        table.add_column("N°", style="dim", justify="center", width=6)
        table.add_column("Catégorie", style="bold green")

        for i, name in enumerate(CATEGORIES.keys(), start=1):
            table.add_row(str(i), name)

        table.add_row("0", "🔙 Quitter le magasin")

        console.print(Align.center(table))
        console.print("\n")

        try:
            category_choice = int(input("👉 Entrez le numéro de la catégorie : "))
            if category_choice == 0:
                return False

            category_names = list(CATEGORIES.keys())
            category_title = category_names[category_choice - 1]
        except (ValueError, IndexError):
            console.print(center_panel("❌ Choix invalide. Veuillez entrer un nombre valide.", "red"))
            return True

        category_classes = CATEGORIES[category_title]
        items = [cls() for cls in category_classes]

        while True:
            display_category(category_title, items)

            try:
                item_choice = int(input("🎯 Entrez le numéro de l'article que vous voulez acheter : "))
                if item_choice == 0:
                    return True 

                item = items[item_choice - 1]
                self.buy_item(player, item)
            except (ValueError, IndexError):
                console.print(center_panel("❌ Choix d'article invalide.", "red"))
                continue

            if player.coins <= 0:
                console.print(center_panel("💸 Vous n'avez plus de pièces. Le magasin se ferme...", "red"))
                return False

            again = input("🔁 Voulez-vous acheter un autre objet dans cette catégorie ? (o/n) : ").lower()
            if again != "o":
                return True

    def buy_item(self, player, item):
        if player.coins < item.price:
            console.print(center_panel("❌ Vous n'avez pas assez de pièces pour cet objet.", "red"))
            return

        player.coins -= item.price
        player.inventory.append(item)
        text = Text.assemble(
            "✅ Vous avez acheté ",
            (f"{item.name}", "bold yellow"),
            " pour ",
            (f"{item.price}🪙", "bold green"),
            style="gold1"
        )
        console.print(center_panel(text, "blue"))

        allowed = getattr(item, 'allowed_classes', None)
        player_class = type(player).__name__
        if hasattr(player, "auto_equip"):
            if allowed is None or player_class in allowed:
                player.auto_equip(item)
            else:
                console.print(center_panel(
                    f"ℹ️ Vous avez acheté {item.name} mais votre classe ({player_class}) n'en tirera pas les bonus.",
                    "yellow"))
