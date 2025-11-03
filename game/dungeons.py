from rich.console import Console
from rich import box
import random

from enemies import (
    Zombie, Zombie2_0, ZombieGuerrier,
    Skeleton, ReinforcedSkeleton, ArmoredSkeleton,
    Goblin, BigGoblin,
    Troll, OlogHai,
    Cadaverus_Devorator, Kondylos_o_Sarantapus, Roi_Gobelin, Garrok_le_Féroce
)

console = Console()

class Dungeon:
    def __init__(self, name):
        self.name = name
        self.floors = []

    def add_floor(self, enemies):
        self.floors.append(enemies)

    def get_total_floors(self):
        return len(self.floors)

def create_zombie_dungeon():
    dungeon = Dungeon("Donjon Zombie")
    dungeon.add_floor([Zombie.create_enemy() for _ in range(2)])
    dungeon.add_floor([Zombie2_0.create_enemy() for _ in range(2)])
    dungeon.add_floor([ZombieGuerrier.create_enemy() for _ in range(2)])
    if random.random() < 0.4: 
        dungeon.add_floor([Cadaverus_Devorator.create_boss()])
    return dungeon

def create_skeleton_dungeon():
    dungeon = Dungeon("Donjon Squelettes")
    dungeon.add_floor([Skeleton.create_enemy() for _ in range(2)])
    dungeon.add_floor([ReinforcedSkeleton.create_enemy() for _ in range(2)])
    dungeon.add_floor([ArmoredSkeleton.create_enemy() for _ in range(2)])
    if random.random() < 0.4:
        dungeon.add_floor([Kondylos_o_Sarantapus.create_boss()])
    return dungeon

def create_goblin_dungeon():
    dungeon = Dungeon("Donjon Gobelins")
    dungeon.add_floor([Goblin.create_enemy() for _ in range(2)])
    dungeon.add_floor([BigGoblin.create_enemy() for _ in range(2)])
    if random.random() < 0.4:
        dungeon.add_floor([Roi_Gobelin.create_boss()])
    return dungeon

def create_troll_dungeon():
    dungeon = Dungeon("Donjon Trolls")
    dungeon.add_floor([Troll.create_enemy() for _ in range(2)])
    dungeon.add_floor([OlogHai.create_enemy() for _ in range(2)])
    if random.random() < 0.4:
        dungeon.add_floor([Garrok_le_Féroce.create_boss()])
    return dungeon

def create_dungeons():
    return [
        create_zombie_dungeon(),
        create_skeleton_dungeon(),
        create_goblin_dungeon(),
        create_troll_dungeon()
    ]