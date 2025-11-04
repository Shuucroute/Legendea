from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.text import Text as _Text
from rich.align import Align
from rich import box
from game.character import Character, Warrior, Mage, Thief, Archer, Druid
from game.dungeons import Dungeon, create_dungeons, Floor
from utils.utils import strip_rich_markup, center_panel, clean_emoji, box_combat, box_damages
from rich.align import Align
from rich.rule import Rule
from game import menu
import random
import time
import sys


console = Console()


class GameState:
    def __init__(self, current_dungeon_index=0, current_floor_index=0):
        self.current_dungeon_index = current_dungeon_index
        self.current_floor_index = current_floor_index


class Quest:
    def __init__(self, name, description, objective, reward):
        self.name = name
        self.description = description
        self.objective = objective
        self.reward = reward
        self.completed = False

    def check_completion(self, player):
        if self.completed:
            return
            
        quest_complete = False
        if self.objective == "Tuer 5 zombies" and getattr(player, 'zombies_killed', 0) >= 5:
            quest_complete = True
        elif self.objective == "Tuer 3 gobelins" and getattr(player, 'goblins_killed', 0) >= 3:
            quest_complete = True
            
        if quest_complete:
            self.completed = True
            player.gain_exp(self.reward["exp"])
            player.get_coins(self.reward["coins"])
            
            quest_text = Text()
            quest_text.append("📜 ", style="yellow")
            quest_text.append(f"Quête : {self.name}\n\n", style="bold yellow")
            quest_text.append(f"{self.description}\n", style="white")
            quest_text.append("\nRécompenses :\n", style="bold yellow")
            quest_text.append("✨ ", style="yellow")
            quest_text.append(f"Expérience : +{self.reward['exp']} XP\n", style="bold cyan")
            quest_text.append("💰 ", style="yellow")
            quest_text.append(f"Pièces : +{self.reward['coins']} pièces", style="bold gold1")
            
            console.print(Panel(
                Align.center(quest_text),
                title="[bold yellow]🎉 Quête Terminée ! 🎉[/bold yellow]",
                border_style="yellow",
                box=box.HEAVY,
                padding=(1, 2)
            ))
            console.print("\n") 



def show_health_bar(character):
    health_ratio = character.hp / character.hp_max

    if health_ratio > 0.6:
        bar_color = "green"
        health_text = "En pleine forme"
    elif health_ratio > 0.3:
        bar_color = "yellow"
        health_text = "Blessé"
    else:
        bar_color = "red"
        health_text = "Critique"

    panel_content = Text()
    panel_content.append(f"{strip_rich_markup(character.name)}\n", style=f"bold {bar_color}")
    panel_content.append(f"{health_text}\n", style=bar_color)
    
    progress_text = Text()
    progress_text.append("♥ ", style=f"bold {bar_color}")
    
    bar_width = 30
    filled = int(bar_width * health_ratio)
    empty = bar_width - filled
    
    progress_text.append("━" * filled, style=bar_color)
    if empty > 0:
        progress_text.append("─" * empty, style="dim")
    
    progress_text.append(f" {character.hp}/{character.hp_max}", style=bar_color)
    
    panel_content.append("\n")
    panel_content.append(progress_text)

    console.print(
        Panel(
            panel_content,
            border_style=bar_color,
            box=box.ROUNDED,
            width=50,
            padding=(0, 2),
        )
    )


def show_mana_bar(character):
    if hasattr(character, "mana_max"):
        mana_ratio = character.mana / character.mana_max
        
        panel_content = Text()
        panel_content.append("Mana\n", style="bold blue")
        
        progress_text = Text()
        progress_text.append("✨ ", style="bold blue")
        
        bar_width = 30
        filled = int(bar_width * mana_ratio)
        empty = bar_width - filled
        
        progress_text.append("━" * filled, style="blue")
        if empty > 0:
            progress_text.append("─" * empty, style="dim")
            
        progress_text.append(f" {character.mana}/{character.mana_max}", style="blue")
        
        panel_content.append("\n")
        panel_content.append(progress_text)

        console.print(
            Panel(
                panel_content,
                border_style="blue",
                box=box.ROUNDED,
                width=50,
                padding=(0, 2),
            )
        )


def show_combat_menu():
    menu_text = Text()
    menu_text.append("Actions disponibles:\n\n", style="bold cyan")
    menu_text.append(clean_emoji("⚔️  "), style="yellow")
    menu_text.append("1) Attaquer\n", style="bold white")
    menu_text.append("🎒  ", style="cyan")
    menu_text.append("2) Utiliser un objet\n", style="bold white")
    menu_text.append("🏃  ", style="red")
    menu_text.append("3) Fuir", style="bold white")
    
    panel = Panel(
        Align.center(menu_text),
        title="[bold cyan]📜 Menu de Combat[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        width=40,
        padding=(1, 2)
    )
    console.print(panel)


def show_enemies(enemies):
    table = Table(
        show_header=True,
        header_style="bold red",
        box=box.ROUNDED,
        border_style="red",
        width=60
    )
    
    table.add_column("№", justify="center", style="dim", width=4)
    table.add_column("Ennemi", justify="left", style="bold red")
    table.add_column("PV", justify="center", style="bold green")
    table.add_column(clean_emoji("⚔️"), justify="center", style="bold yellow")
    table.add_column(clean_emoji("🛡️"), justify="center", style="bold blue")
    
    for i, enemy in enumerate(enemies, 1):
        health_ratio = enemy.hp / enemy.hp_max
        if health_ratio > 0.6:
            health_color = "green"
        elif health_ratio > 0.3:
            health_color = "yellow"
        else:
            health_color = "red"
            
        table.add_row(
            str(i),
            _Text(enemy.name, style="bold red"),
            _Text(f"{enemy.hp}/{enemy.hp_max}", style=f"bold {health_color}"),
            _Text(str(enemy.attack_value), style="bold yellow"),
            _Text(str(enemy.defense_value), style="bold blue")
        )
    
    console.print(box_combat(
        table,
        title=clean_emoji("[bold red]⚔️ Ennemis[/bold red]"),
        border_style="red"
    ))


def get_valid_input(prompt, valid_options, error_message="Choix invalide."):
    while True:
        try:
            choice = input(prompt)
            if choice in valid_options:
                return choice
            console.print(Panel(f"[red]{error_message}[/red]", border_style="purple4"))
        except (ValueError, EOFError):
            console.print(Panel("[red]Erreur de saisie.[/red]", border_style="purple4"))


def get_valid_enemy_choice(enemies):
    while True:
        try:
            enemy_choice = int(input("Entrez le numéro de l'ennemi: "))
            if 1 <= enemy_choice <= len(enemies):
                return enemy_choice
            console.print(Panel("[red]Numéro d'ennemi invalide.[/red]", border_style="purple4"))
        except ValueError:
            console.print(Panel("[red]Entrée invalide. Veuillez entrer un nombre.[/red]", border_style="purple4"))


def handle_player_attack(player, enemies):
    show_enemies(enemies)
    enemy_choice = get_valid_enemy_choice(enemies)
    enemy = enemies[enemy_choice - 1]
    
    attack_text = Text()
    attack_text.append(clean_emoji("⚔️ "), style="yellow")
    attack_text.append(player.name, style="bold cyan")
    attack_text.append(" attaque ", style="white")
    attack_text.append(enemy.name, style="bold red")
    attack_text.append(" !", style="white")
    
    console.print(box_damages(
        Align.center(attack_text),
        border_style="yellow",
        padding=(0, 2)
    ))
    
    player.attack(enemy)
    return enemy, enemy_choice - 1


def handle_enemy_counterattack(enemy, player):
    counter_text = Text()
    counter_text.append("💢 ", style="red")
    counter_text.append(enemy.name, style="bold red")
    counter_text.append(" contre-attaque !", style="white")
    
    console.print(box_damages(
        Align.center(counter_text),
        border_style="red",
        padding=(0, 2)
    ))
    
    enemy.attack(player)
    
    if not player.is_alive():
        defeat_text = Text()
        defeat_text.append("💀 ", style="red")
        defeat_text.append(player.name, style="bold white")
        defeat_text.append(" a été vaincu !", style="red")
        
        console.print(Panel(
            Align.center(defeat_text),
            title="[bold red]Défaite[/bold red]",
            border_style="red",
            box=box.HEAVY,
            padding=(1, 2)
        ))
        return False
    else:
        resist_text = Text()
        resist_text.append(clean_emoji("🛡️ "), style="cyan")
        resist_text.append(player.name, style="bold cyan")
        resist_text.append(" résiste à l'attaque de ", style="white")
        resist_text.append(enemy.name, style="bold red")
        resist_text.append(" !", style="white")
        
        console.print(box_damages(
            Align.center(resist_text),
            border_style="cyan",
            padding=(0, 2)
        ))
        return True

def apply_group_combat_nerf(enemies):
    if len(enemies) >= 2:
        for enemy in enemies:
            enemy.attack_value = max(1, int(enemy.attack_value * 0.85))
            enemy.defense_value = max(0, int(enemy.defense_value * 0.9))


def update_kill_counters(player, enemy):
    from enemies import Zombie, Goblin
    if not hasattr(player, 'zombies_killed'):
        player.zombies_killed = 0
    if not hasattr(player, 'goblins_killed'):
        player.goblins_killed = 0
    if isinstance(enemy, Zombie):
        player.zombies_killed += 1
    elif isinstance(enemy, Goblin):
        player.goblins_killed += 1


def combat(player, enemies):
    console.print("\n")
    console.print(center_panel(
        Align.center(clean_emoji("[bold yellow]⚔️ ✨ Le combat commence ! ✨ ⚔️[/bold yellow]")),
        border_style="yellow",
        box_style=box.DOUBLE
    ))
    console.print("\n")
    time.sleep(0.4)
    apply_group_combat_nerf(enemies)

    while enemies:
        console.print(Rule(style="gold1", characters="─"))
        
        console.print(box_combat(
            "[bold cyan]État du Combat[/bold cyan]",
            border_style="cyan"
        ))
        
        show_health_bar(player)
        if hasattr(player, "mana_max"):
            show_mana_bar(player)
        console.print("\n")
        
        show_combat_menu()
        choice = get_valid_input("\n👉 Choisissez votre action (1/2/3): ", ["1", "2", "3"])

        if choice == "1":
            enemy, enemy_index = handle_player_attack(player, enemies)
            if not enemy.is_alive():
                victory_text = Text()
                victory_text.append(clean_emoji("🗡️ "), style="yellow")
                victory_text.append(f"{enemy.name} a été vaincu !", style="bold green")
                victory_text.append("\n\n")
                
                victory_text.append("Récompenses obtenues :\n", style="bold yellow")
                victory_text.append("✨ ", style="yellow")
                victory_text.append(f"Expérience : +{enemy.exp_reward} XP\n", style="bold cyan")
                victory_text.append("💰 ", style="yellow")
                victory_text.append(f"Pièces : +{enemy.coins_reward} pièces", style="bold gold1")
                
                console.print(box_damages(
                    Align.center(victory_text),
                    title="[bold yellow]💥 Victoire ! 💥[/bold yellow]",
                    border_style="yellow",
                    padding=(1, 2)
                ))
                
                console.print("\n") 
                
                player.gain_exp(enemy.exp_reward)
                player.get_coins(enemy.coins_reward)
                update_kill_counters(player, enemy)
                enemies.pop(enemy_index)
            else:
                if not handle_enemy_counterattack(enemy, player):
                    return False
        elif choice == "2":
            if not player.inventory:
                console.print(box_combat("[yellow]Aucun objet n'est disponible pour le moment.[/yellow]", border_style="purple4"))
            else:
                table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
                table.add_column("N°", justify="center", style="dim", width=6)
                table.add_column("Objet", style="bold yellow")
                for i, it in enumerate(player.inventory, start=1):
                    table.add_row(str(i), it.name)
                table.add_row("0", "🔙 Annuler")

                console.print(box_combat(Align.center(table), title="[bold cyan]🎒 Inventaire[/bold cyan]", border_style="cyan"))

                try:
                    sel = int(input("🎯 Entrez le numéro de l'objet à utiliser (0 pour annuler) : "))
                except ValueError:
                    console.print(Panel("[red]Choix invalide.[/red]", border_style="purple4"))
                    continue

                if sel == 0:
                    continue

                if 1 <= sel <= len(player.inventory):
                    item = player.inventory[sel - 1]
                    if hasattr(player, 'use_item'):
                        used = player.use_item(item.name)
                        if used:
                            if enemies:
                                if not handle_enemy_counterattack(enemies[0], player):
                                    return False
                        else:
                            console.print(box_combat("[yellow]Impossible d'utiliser cet objet.[/yellow]", border_style="purple4"))
                else:
                    console.print(box_combat("[red]Numéro d'objet invalide.[/red]", border_style="purple4"))
        elif choice == "3":
            console.print(box_combat("[red]Tu fuis la bataille ![/red]", border_style="purple4"))
            break

        if not enemies:
            victory_text = Text()
            victory_text.append("🎊 ", style="yellow")
            victory_text.append("Félicitations !", style="bold yellow")
            victory_text.append("\n\n")
            victory_text.append("Vous avez vaincu tous vos ennemis !", style="bold green")
            
            console.print(Panel(
                Align.center(victory_text),
                title="[bold yellow]🏆 Combat Terminé ! 🏆[/bold yellow]",
                border_style="yellow",
                box=box.HEAVY,
                padding=(1, 2)
            ))
            console.print("\n")
            check_quests(player)
            break

    return True


def show_floor_completion_menu_and_save(player, state, current_floor, total_floors):
    menu.save_game(player, state)
    console.print(Panel("✅ Progression sauvegardée automatiquement !", border_style="green"))
    
    if current_floor < total_floors:
        console.print("\n")
        panel = Panel(
            f"[bold cyan]Étage {current_floor}/{total_floors} terminé ![/bold cyan]\n\n"
            "1) Continuer vers l'étage suivant\n"
            "2) Retourner au menu principal\n"
            "3) Quitter le jeu",
            title="[bold magenta]Fin d'étage[/bold magenta]",
            border_style="gold1"
        )
        console.print(panel)
        
        choice = get_valid_input("👉 Entrez votre choix (1/2/3) : ", ["1", "2", "3"])
        if choice == "1":
            console.print(Panel("Passons à l'étage suivant... ✨", border_style="purple4"))
            return "continue"
        elif choice == "2":
            console.print(Panel("Retour au menu principal...", border_style="purple4"))
            return "menu"
        elif choice == "3":
            console.print(Panel("Au revoir ! Merci d'avoir joué.", border_style="purple4"))
            return "quit"
    else:
        console.print(Panel("🏆 Félicitations ! Vous avez terminé ce donjon !", border_style="gold1"))
        input("Appuyez sur Entrée pour continuer...")
        return "continue"


def check_quests(player):
    for quest in quests:
        quest.check_completion(player)





def run_dungeon(player, state, dungeon, dungeon_index):
    for floor_num, floor in enumerate(dungeon.floors, start=1):
        if state.current_dungeon_index > dungeon_index:
            break
        if floor_num - 1 < state.current_floor_index:
            continue
        console.print(center_panel(clean_emoji(f"⚔️ Tu rentres dans le {dungeon.name}, étage {floor_num}!"), border_style="gold1"))

        if isinstance(floor, Floor):
            total_rooms = len(floor.rooms)
            for room_idx, room in enumerate(floor.rooms, start=1):
                console.print(center_panel(clean_emoji(f"🧭 Salle {room_idx}/{total_rooms}"), border_style="purple4"))
                time.sleep(0.2)

                if getattr(room, 'enemies', None):
                    enemies = room.enemies
                    if not combat(player, enemies):
                        choice = menu.show_death_menu()
                        if choice == "restart":
                            player.reset_stats()
                            state.current_dungeon_index = 0
                            state.current_floor_index = 0
                            return False
                        elif choice == "quit":
                            return False

                elif getattr(room, 'chest', None):
                    chest = room.chest
                    console.print(box_combat(f"Vous trouvez un coffre : [bold]{chest.name}[/bold]", border_style="gold1"))
                    choice = get_valid_input("👉 Voulez-vous ouvrir le coffre ? (1) Oui (2) Non : ", ["1", "2"])
                    if choice == "1":
                        loot = chest.open()
                        loot_names = [getattr(i, 'name', str(i)) for i in loot]
                        obtained_text = []
                        for it in loot:
                            if hasattr(it, 'coins_amount'):
                                player.get_coins(it.coins_amount)
                                obtained_text.append(f"{getattr(it,'name')} (+{it.coins_amount} pièces)")
                            elif hasattr(it, 'exp_amount'):
                                player.gain_exp(it.exp_amount)
                                obtained_text.append(f"{getattr(it,'name')} (+{it.exp_amount} EXP)")
                            else:
                                try:
                                    player.inventory.append(it)
                                    player.auto_equip(it)
                                    obtained_text.append(getattr(it, 'name', str(it)))
                                except Exception:
                                    obtained_text.append(getattr(it, 'name', str(it)))

                        console.print(box_combat(f"Vous récupérez : {', '.join(obtained_text)}", border_style="green"))
                    else:
                        console.print(box_combat("Vous laissez le coffre intact.", border_style="yellow"))

                time.sleep(0.3)

        else:
            enemies = floor
            if not combat(player, enemies):
                choice = menu.show_death_menu()
                if choice == "restart":
                    player.reset_stats()
                    state.current_dungeon_index = 0
                    state.current_floor_index = 0
                    return False
                elif choice == "quit":
                    return False
        state.current_floor_index = floor_num
        player.reset_stats()
        result = show_floor_completion_menu_and_save(player, state, floor_num, dungeon.get_total_floors())
        if result == "menu":
            return False
        elif result == "quit":
            sys.exit()
    return True


def start_game(player, state: GameState):
    console.print(box_combat("[bold blue]Bienvenue dans le Donjon des Légendes ![/bold blue]", border_style="purple4"))
    time.sleep(0.5)
    if not hasattr(player, 'zombies_killed'):
        player.zombies_killed = 0
    if not hasattr(player, 'goblins_killed'):
        player.goblins_killed = 0
    dungeons = create_dungeons()
    for i, dungeon in enumerate(dungeons):
        if not run_dungeon(player, state, dungeon, i):
            break
        console.print(Panel(f"Félicitations ! Vous avez vaincu tous les étages du {dungeon.name}.", border_style="gold1"))
        if state.current_dungeon_index == i:
            state.current_dungeon_index = i + 1
            state.current_floor_index = 0
        menu.save_game(player, state)


def add_reset_stats_method():
    def reset_stats(self):
        self.hp = self.hp_max
        if hasattr(self, "mana_max"):
            self.mana = self.mana_max
    Character.reset_stats = reset_stats

add_reset_stats_method()


quests = [
    Quest(
        name="La Menace Zombie",
        description="Tuez 5 zombies pour protéger le village.",
        objective="Tuer 5 zombies",
        reward={"exp": 100, "coins": 50},
    ),
    Quest(
        name="Le Trésor des Gobelins",
        description="Tuez 3 gobelins pour récupérer leur trésor.",
        objective="Tuer 3 gobelins",
        reward={"exp": 150, "coins": 75},
    ),
]
