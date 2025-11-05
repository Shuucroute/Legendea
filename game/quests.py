from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich import box
from rich.console import Console

console = Console()


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
        
        # Quêtes de tuer des ennemis
        if self.objective == "Tuer 5 zombies" and getattr(player, 'zombies_killed', 0) >= 5:
            quest_complete = True
        elif self.objective == "Tuer 3 gobelins" and getattr(player, 'goblins_killed', 0) >= 3:
            quest_complete = True
        elif self.objective == "Tuer 10 zombies" and getattr(player, 'zombies_killed', 0) >= 10:
            quest_complete = True
        elif self.objective == "Tuer 7 gobelins" and getattr(player, 'goblins_killed', 0) >= 7:
            quest_complete = True
        elif self.objective == "Tuer 8 squelettes" and getattr(player, 'skeletons_killed', 0) >= 8:
            quest_complete = True
        elif self.objective == "Tuer 5 trolls" and getattr(player, 'trolls_killed', 0) >= 5:
            quest_complete = True
        elif self.objective == "Tuer 15 zombies" and getattr(player, 'zombies_killed', 0) >= 15:
            quest_complete = True
        elif self.objective == "Tuer 20 ennemis" and (getattr(player, 'zombies_killed', 0) + getattr(player, 'goblins_killed', 0) + getattr(player, 'skeletons_killed', 0) + getattr(player, 'trolls_killed', 0)) >= 20:
            quest_complete = True
        
        # Quêtes de collecte d'items
        elif self.objective == "Collecter 3 chairs putréfiées":
            chair_count = sum(1 for item in player.inventory if hasattr(item, 'name') and item.name == "Chair putréfiée")
            if chair_count >= 3:
                quest_complete = True
        elif self.objective == "Collecter 5 chairs putréfiées":
            chair_count = sum(1 for item in player.inventory if hasattr(item, 'name') and item.name == "Chair putréfiée")
            if chair_count >= 5:
                quest_complete = True
        elif self.objective == "Collecter 5 os":
            bone_count = sum(1 for item in player.inventory if hasattr(item, 'name') and item.name == "Os")
            if bone_count >= 5:
                quest_complete = True
        elif self.objective == "Collecter 10 os":
            bone_count = sum(1 for item in player.inventory if hasattr(item, 'name') and item.name == "Os")
            if bone_count >= 10:
                quest_complete = True
        
        # Quêtes de niveau
        elif self.objective == "Atteindre le niveau 3" and player.level >= 3:
            quest_complete = True
        elif self.objective == "Atteindre le niveau 5" and player.level >= 5:
            quest_complete = True
        elif self.objective == "Atteindre le niveau 10" and player.level >= 10:
            quest_complete = True
        
        # Quêtes d'argent
        elif self.objective == "Avoir 100 pièces" and player.coins >= 100:
            quest_complete = True
        elif self.objective == "Avoir 200 pièces" and player.coins >= 200:
            quest_complete = True
        elif self.objective == "Avoir 500 pièces" and player.coins >= 500:
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
    
    # Quêtes squelettes
    Quest(
        name="L'Armée des Morts",
        description="Les squelettes envahissent les catacombes. Éliminez 8 squelettes pour les repousser.",
        objective="Tuer 8 squelettes",
        reward={"exp": 200, "coins": 100},
    ),
    
    # Quêtes trolls
    Quest(
        name="Le Roi des Trolls",
        description="Les trolls sont une menace pour les caravanes. Vaincre 5 trolls pour sécuriser les routes.",
        objective="Tuer 5 trolls",
        reward={"exp": 300, "coins": 150},
    ),
    
    # Quêtes zombies avancées
    Quest(
        name="L'Apocalypse Zombie",
        description="L'épidémie zombie s'aggrave. Tuez 10 zombies pour contenir la menace.",
        objective="Tuer 10 zombies",
        reward={"exp": 250, "coins": 120},
    ),
    Quest(
        name="Le Purificateur",
        description="Une véritable horde de zombies menace le royaume. Éliminez 15 zombies pour sauver la région.",
        objective="Tuer 15 zombies",
        reward={"exp": 400, "coins": 200},
    ),
    
    # Quêtes gobelins avancées
    Quest(
        name="La Tribu Gobeline",
        description="Les gobelins se multiplient. Tuez 7 gobelins pour réduire leur nombre.",
        objective="Tuer 7 gobelins",
        reward={"exp": 300, "coins": 150},
    ),
    
    # Quêtes de collecte
    Quest(
        name="Collecte Macabre",
        description="Un alchimiste recherche de la chair putréfiée pour ses expériences. Collectez 3 chairs putréfiées.",
        objective="Collecter 3 chairs putréfiées",
        reward={"exp": 180, "coins": 90},
    ),
    Quest(
        name="L'Alchimiste Fou",
        description="L'alchimiste a besoin de plus de matériel. Apportez-lui 5 chairs putréfiées.",
        objective="Collecter 5 chairs putréfiées",
        reward={"exp": 350, "coins": 175},
    ),
    Quest(
        name="Les Restes des Tombes",
        description="Le forgeron a besoin d'os pour renforcer des manches. Collectez 5 os.",
        objective="Collecter 5 os",
        reward={"exp": 200, "coins": 110},
    ),
    Quest(
        name="Mandat du Fossoyeur",
        description="Le fossoyeur vous missionne pour une grande collecte. Rapportez 10 os.",
        objective="Collecter 10 os",
        reward={"exp": 420, "coins": 220},
    ),
    
    # Quêtes de niveau
    Quest(
        name="Premiers Pas",
        description="Progressez dans votre aventure en atteignant le niveau 3.",
        objective="Atteindre le niveau 3",
        reward={"exp": 150, "coins": 100},
    ),
    Quest(
        name="Aventurier Confirmé",
        description="Prouvez votre valeur en atteignant le niveau 5.",
        objective="Atteindre le niveau 5",
        reward={"exp": 300, "coins": 200},
    ),
    Quest(
        name="Héros Légendaire",
        description="Atteignez le niveau 10 et devenez une légende vivante.",
        objective="Atteindre le niveau 10",
        reward={"exp": 600, "coins": 400},
    ),
    
    # Quêtes d'argent
    Quest(
        name="Le Marchand",
        description="Économisez 100 pièces pour acheter de meilleurs équipements.",
        objective="Avoir 100 pièces",
        reward={"exp": 200, "coins": 50},
    ),
    Quest(
        name="Le Riche Aventurier",
        description="Amassez 200 pièces pour prouver votre prospérité.",
        objective="Avoir 200 pièces",
        reward={"exp": 400, "coins": 100},
    ),
    Quest(
        name="Le Trésor Royal",
        description="Rassemblez 500 pièces et devenez l'aventurier le plus riche du royaume.",
        objective="Avoir 500 pièces",
        reward={"exp": 800, "coins": 200},
    ),
    
    # Quêtes de massacre
    Quest(
        name="Le Chasseur d'Élite",
        description="Vainquez 20 ennemis de toutes sortes pour prouver votre maîtrise du combat.",
        objective="Tuer 20 ennemis",
        reward={"exp": 500, "coins": 250},
    ),
]

__all__ = ["Quest", "quests"]
