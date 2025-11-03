from game.character import Character
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

console = Console()

def show_ascii_panel(title: str, art: str, subtitle: str = ""):
    content = f"{art}\n\n{subtitle}"
    console.print(
        Panel(
            Align.center(Text(content, style="gold1")),
            title=f"[bold purple4]{title}[/bold purple4]",
            border_style="purple4"
        )
    )

class BaseEnemy(Character):
    def __init__(self, name, hp, attack_value, defense_value, exp_reward, coins_reward, ascii_art=""):
        super().__init__(name, hp, attack_value, defense_value, exp_reward, coins_reward)
        self.ascii_art = ascii_art

    @classmethod
    def create_enemy(cls):
        return cls()

    def compute_damages(self, target):
        return super().compute_damages(target)

    def compute_raw_damages(self, damages, attacker):
        return super().compute_raw_damages(damages, attacker)

    def defeat(self, player: Character, number_defeated: int):
        player.gain_exp(self.exp_reward * number_defeated)
