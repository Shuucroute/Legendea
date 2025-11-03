import random
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.progress import Progress, BarColumn, TextColumn

console = Console()


from rich import box

def styled_message(message: str, title: str = None, style: str = "gold1", icon: str = None):
    text = Text()
    if icon:
        text.append(f"{icon} ", style=style)
    text.append(message, style=style)
    
    console.print(Panel(
        Align.center(text),
        title=title if title else None,
        border_style=style,
        box=box.ROUNDED,
        padding=(0, 2)
    ))


# ╔══════════════════════════════════════════════════════════════════╗
# ║                           CLASSE DE BASE                         ║
# ╚══════════════════════════════════════════════════════════════════╝

class Character:
    def __init__(self, name, hp_max, attack_value, defense_value, exp_reward, coins_reward):
        self.name = name
        self.hp_max = hp_max
        self.hp = hp_max
        self.attack_value = attack_value
        self.defense_value = defense_value

        self.exp = 0
        self.level = 1
        self.exp_reward = exp_reward
        self.coins = 20
        self.coins_reward = coins_reward

        self.inventory = []
        self.equipped_items = set()
        self.equipment_attack_bonus = 0
        self.equipment_defense_bonus = 0
        self.temporary_bonuses = {}
        self.status_effects = []

    # ════════════════════════════════════════════════════════════════
    #                           EXP / NIVEAU
    # ════════════════════════════════════════════════════════════════

    def gain_exp(self, amount):
        self.exp += amount
        exp_text = Text()
        exp_text.append("✨ ", style="yellow")
        exp_text.append(f"{self.name} ", style="bold yellow")
        exp_text.append("a gagné ", style="white")
        exp_text.append(f"{amount} ", style="bold cyan")
        exp_text.append("points d'expérience", style="white")
        
        console.print(Panel(
            Align.center(exp_text),
            border_style="yellow",
            box=box.ROUNDED,
            padding=(0, 2)
        ))
        
        self._check_level_up()
        self._show_expbar()

    def _check_level_up(self):
        leveled_up = False

        while self.exp >= int(50 * self.level * 1.5):
            self.exp -= int(50 * self.level * 1.5)
            self.level += 1
            leveled_up = True

            level_text = Text()
            level_text.append("🎉 ", style="yellow")
            level_text.append(f"{self.name}", style="bold yellow")
            level_text.append(" a atteint le ", style="white")
            level_text.append(f"niveau {self.level}", style="bold cyan")
            level_text.append(" !\n\n", style="white")
            
            level_text.append("Bonus obtenus :\n", style="bold yellow")
            level_text.append("❤️ ", style="red")
            level_text.append("PV Max +10\n", style="bold red")
            level_text.append("⚔️ ", style="yellow")
            level_text.append("Attaque +2\n", style="bold yellow")
            level_text.append("🛡️ ", style="blue")
            level_text.append("Défense +1", style="bold blue")

            console.print(Panel(
                Align.center(level_text),
                title="[bold yellow]↑ Niveau Supérieur ! ↑[/bold yellow]",
                border_style="yellow",
                box=box.HEAVY,
                padding=(1, 2)
            ))

            self.hp_max += 10
            self.attack_value += 2
            self.defense_value += 1
            self.exp_reward += 1

        if leveled_up:
            self.hp = self.hp_max

    def _show_expbar(self):
        next_threshold = int(50 * self.level * 1.5)
        current_exp = min(self.exp, next_threshold)
        
        exp_text = Text()
        exp_text.append(f"{self.name}\n", style="bold yellow")
        exp_text.append("✨ ", style="yellow")
        
        bar_width = 30
        filled = int(bar_width * (current_exp / next_threshold))
        empty = bar_width - filled
        
        exp_text.append("━" * filled, style="yellow")
        if empty > 0:
            exp_text.append("─" * empty, style="dim")
            
        exp_text.append(f" {current_exp}/{next_threshold} EXP", style="yellow")
        
        console.print(Panel(
            Align.center(exp_text),
            border_style="yellow",
            box=box.ROUNDED,
            padding=(0, 2)
        ))

    # ════════════════════════════════════════════════════════════════
    #                              COMBAT
    # ════════════════════════════════════════════════════════════════

    def is_alive(self):
        return self.hp > 0

    def get_total_attack(self):
        total = self.attack_value + self.equipment_attack_bonus
        total += int(self.temporary_bonuses.get("attack", 0))
        return total

    def get_total_defense(self):
        total = self.defense_value + self.equipment_defense_bonus
        total += int(self.temporary_bonuses.get("defense", 0))
        return total

    def compute_damages(self, target):
        return self.get_total_attack()

    def compute_raw_damages(self, damages, attacker):
        return max(0, damages - self.get_total_defense())

    def attack(self, target):
        if not self.is_alive():
            return

        damages = self.compute_damages(target)
        attack_text = Text()
        attack_text.append("⚔️ ", style="yellow")
        attack_text.append(self.name, style="bold yellow")
        attack_text.append(" attaque avec ", style="white")
        attack_text.append(f"{damages}", style="bold red")
        attack_text.append(" points de dégâts !", style="white")
        
        console.print(Panel(
            Align.center(attack_text),
            border_style="yellow",
            box=box.ROUNDED,
            padding=(0, 2)
        ))
        
        target.defend(damages, self)

    def defend(self, damages, attacker):
        raw_damages = self.compute_raw_damages(damages, attacker)
        defense_text = Text()
        defense_text.append("🛡️ ", style="blue")
        defense_text.append(self.name, style="bold blue")
        defense_text.append(" défend et subit ", style="white")
        defense_text.append(f"{raw_damages}", style="bold red")
        defense_text.append(" points de dégâts !", style="white")
        
        console.print(Panel(
            Align.center(defense_text),
            border_style="blue",
            box=box.ROUNDED,
            padding=(0, 2)
        ))
        
        self.decrease_hp(raw_damages)

    # ════════════════════════════════════════════════════════════════
    #                              RÉINITIALISATION
    # ════════════════════════════════════════════════════════════════

    def reset_stats(self):
        self.hp = self.hp_max

        if hasattr(self, "mana_max"):
            try:
                self.mana = self.mana_max
            except Exception:
                pass

        self.temporary_bonuses.clear()
        self.status_effects.clear()
        styled_message(f"{self.name} a été réinitialisé(e). PV et états remis à zéro.", style="gold1")

    # ════════════════════════════════════════════════════════════════
    #                              HP / COINS
    # ════════════════════════════════════════════════════════════════

    def decrease_hp(self, amount):
        self.hp = max(0, self.hp - amount)
        self.show_healthbar()

    def increase_hp(self, amount):
        self.hp = min(self.hp_max, self.hp + amount)
        self.show_healthbar()

    def show_healthbar(self):
        health_ratio = self.hp / self.hp_max if self.hp_max > 0 else 0
        
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
        panel_content.append(f"{self.name}\n", style=f"bold {bar_color}")
        panel_content.append(f"{health_text}\n", style=bar_color)
        
        progress_text = Text()
        progress_text.append("♥ ", style=f"bold {bar_color}")
        
        bar_width = 30
        filled = int(bar_width * health_ratio)
        empty = bar_width - filled
        
        progress_text.append("━" * filled, style=bar_color)
        if empty > 0:
            progress_text.append("─" * empty, style="dim")
            
        progress_text.append(f" {self.hp}/{self.hp_max} PV", style=bar_color)
        
        panel_content.append(progress_text)
        
        console.print(Panel(
            Align.center(panel_content),
            border_style=bar_color,
            box=box.ROUNDED,
            padding=(0, 2)
        ))

    def get_coins(self, amount):
        self.coins += amount
        coins_text = Text()
        coins_text.append("💰 ", style="yellow")
        coins_text.append(self.name, style="bold yellow")
        coins_text.append(" a gagné ", style="white")
        coins_text.append(f"{amount}", style="bold gold1")
        coins_text.append(" pièces !", style="white")
        
        console.print(Panel(
            Align.center(coins_text),
            border_style="yellow",
            box=box.ROUNDED,
            padding=(0, 2)
        ))

    def show_coins(self):
        coins_text = Text()
        coins_text.append("💰 ", style="yellow")
        coins_text.append(self.name, style="bold yellow")
        coins_text.append(" possède ", style="white")
        coins_text.append(f"{self.coins}", style="bold gold1")
        coins_text.append(" pièces", style="white")
        
        console.print(Panel(
            Align.center(coins_text),
            border_style="yellow",
            box=box.ROUNDED,
            padding=(0, 2)
        ))

    # ════════════════════════════════════════════════════════════════
    #                            ÉQUIPEMENT
    # ════════════════════════════════════════════════════════════════

    def auto_equip(self, item):
        if getattr(item, 'name', None) in self.equipped_items:
            return

        allowed = getattr(item, 'allowed_classes', None)
        my_class = type(self).__name__
        if allowed is not None and my_class not in allowed:
            return

        improved = False
        if hasattr(item, 'attack_bonus') and item.attack_bonus > 0:
            self.equipment_attack_bonus += item.attack_bonus
            improved = True

        if hasattr(item, 'defense_bonus') and item.defense_bonus > 0:
            self.equipment_defense_bonus += item.defense_bonus
            improved = True

        if improved:
            self.equipped_items.add(item.name)
            
    def use_item(self, item_name):
        for item in list(self.inventory):
            if item.name == item_name and hasattr(item, 'usable') and item.usable:
                healed = 0
                try:
                    healed = item.use(self)
                except Exception:
                    healed = 0

                if healed and healed > 0:
                    styled_message(f"🧪 {self.name} utilise {item.name} et récupère {healed} PV!", style="green")
                    try:
                        self.inventory.remove(item)
                    except ValueError:
                        pass
                    return True
                else:
                    styled_message(f"{item.name} n'a eu aucun effet (PV déjà au maximum).", style="yellow")
                    return False
        return False


# ╔══════════════════════════════════════════════════════════════════╗
# ║                          CLASSES SPÉCIALES                       ║
# ╚══════════════════════════════════════════════════════════════════╝

class Warrior(Character):
    def compute_damages(self, target):
        return super().compute_damages(target) + 3


class Mage(Character):
    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 3)


class Thief(Character):
    def compute_damages(self, target):
        return super().compute_damages(target) + target.defense_value


class Archer(Character):
    def compute_damages(self, target):
        return super().compute_damages(target) + 5


class Druid(Character):
    def __init__(self, name, hp_max, attack_value, defense_value, mana_max, exp_reward, healing_value, coins_reward):
        super().__init__(name, hp_max, attack_value, defense_value, exp_reward, coins_reward)
        self.mana_max = mana_max
        self.mana = mana_max
        self.healing_value = healing_value

    def heal(self, target):
        if self.mana <= 0:
            styled_message("Pas assez de mana pour lancer un sort.", style="red")
            return

        heal_amount = min(self.healing_value, target.hp_max - target.hp)
        target.increase_hp(heal_amount)
        self.mana -= 1

        styled_message(f"{self.name} soigne {target.name} de {heal_amount} PV.", style="green")
        target.show_healthbar()

    def show_manabar(self):
        mana_ratio = self.mana / self.mana_max
        panel_content = Text()
        panel_content.append(f"{self.name}\n", style="bold blue")
        
        progress_text = Text()
        progress_text.append("✨ ", style="bold blue")
        
        bar_width = 30
        filled = int(bar_width * mana_ratio)
        empty = bar_width - filled
        
        progress_text.append("━" * filled, style="blue")
        if empty > 0:
            progress_text.append("─" * empty, style="dim")
            
        progress_text.append(f" {self.mana}/{self.mana_max} Mana", style="blue")
        
        panel_content.append(progress_text)
        
        console.print(Panel(
            Align.center(panel_content),
            border_style="blue",
            box=box.ROUNDED,
            padding=(0, 2)
        ))
