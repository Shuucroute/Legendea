from rich.console import Console
from rich import box
import random

from enemies import (
    Zombie, ZombieFaible, ZombieRapide, ZombieMage, ZombieElite, ZombieLent, ZombieRegenerant, Zombie2_0, ZombieGuerrier, ZombieExplosif, ZombieBlindé,
    Skeleton, ReinforcedSkeleton, ArmoredSkeleton, SkeletonMage, AgileSkeleton, BurningSkeleton, PoisonSkeleton, SpectralSkeleton, GiantSkeleton, NecromancerSkeleton, SkeletonArcher,
    Goblin, BigGoblin, ThiefGoblin, WarriorGoblin, MageGoblin, ArcherGoblin, AlchemistGoblin, ArmoredGoblin, AgileGoblin, BomberGoblin, GoblinChief,
    Troll, OlogHai, CaveTroll, RegeneratingTroll, FireTroll, IceTroll, StormTroll, ShamanTroll, NecroticTroll, WarTroll, TrollKing,
    Cadaverus_Devorator, Kondylos_o_Sarantapus, Roi_Gobelin, Garrok_le_Féroce
)
from items.chests import create_chest
from items.objects import ITEM_REGISTRY

console = Console()

class Dungeon:
    def __init__(self, name):
        self.name = name
        self.floors = []

    def add_floor(self, enemies):
        self.floors.append(enemies)

    def get_total_floors(self):
        return len(self.floors)


class Room:
    def __init__(self, enemies=None, chest=None):
        self.enemies = enemies
        self.chest = chest


class Floor:
    def __init__(self, rooms: list[Room]):
        self.rooms = rooms


def create_zombie_dungeon():
    dungeon = Dungeon("Donjon Zombie")

    rooms1 = []
    num_rooms = 10
    chest_chance = 0.4
    for i in range(num_rooms):
        if random.random() < chest_chance:
            r = random.random()
            if r < 0.70:
                chest = create_chest('wood')
            elif r < 0.95:
                chest = create_chest('silver')
            elif r < 0.995:
                chest = create_chest('gold')
            else:
                chest = create_chest('legendary')
            rooms1.append(Room(chest=chest))
        else:
            count = random.randint(1, 3)
            choices = [Zombie.create_enemy, Zombie2_0.create_enemy, ZombieFaible.create_enemy,
                       ZombieLent.create_enemy, ZombieRegenerant.create_enemy]
            enemies = [random.choice(choices)() for _ in range(count)]
            rooms1.append(Room(enemies=enemies))
    dungeon.add_floor(Floor(rooms1))

    rooms2 = []
    num_rooms2 = 10
    chest_chance = 0.3
    for i in range(num_rooms2):
        if random.random() < chest_chance:
            r = random.random()
            if r < 0.50:
                chest = create_chest('wood')
            elif r < 0.85:
                chest = create_chest('silver')
            elif r < 0.895:
                chest = create_chest('gold')
            else:
                chest = create_chest('legendary')
            rooms2.append(Room(chest=chest))
        else:
            count = random.randint(1, 3)
            choices = [ZombieRapide.create_enemy, ZombieMage.create_enemy,
                       Zombie2_0.create_enemy, ZombieExplosif.create_enemy]
            enemies = [random.choice(choices)() for _ in range(count)]
            rooms2.append(Room(enemies=enemies))
    dungeon.add_floor(Floor(rooms2))

    rooms3 = []
    num_rooms3 = 10
    chest_chance = 0.2
    for i in range(num_rooms3):
        if random.random() < chest_chance:
            r = random.random()
            if r < 0.30:
                chest = create_chest('wood')
            elif r < 0.70:
                chest = create_chest('silver')
            elif r < 0.90:
                chest = create_chest('gold')
            else:
                chest = create_chest('legendary')
            rooms3.append(Room(chest=chest))
        else:
            count = random.randint(1, 3)
            choices = [ZombieElite.create_enemy, ZombieGuerrier.create_enemy,
                       ZombieExplosif.create_enemy, ZombieBlindé.create_enemy]
            enemies = [random.choice(choices)() for _ in range(count)]
            rooms3.append(Room(enemies=enemies))
    dungeon.add_floor(Floor(rooms3))

    if random.random() < 0.4:
        dungeon.add_floor([Cadaverus_Devorator.create_boss()])
    return dungeon

def create_skeleton_dungeon():
    dungeon = Dungeon("Donjon Squelettes")
    rooms = []
    num_rooms = 10
    chest_chance = 0.4
    for i in range(num_rooms):
        if random.random() < chest_chance:
            r = random.random()
            if r < 0.70:
                chest = create_chest('wood')
            elif r < 0.95:
                chest = create_chest('silver')
            elif r < 0.995:
                chest = create_chest('gold')
            else:
                chest = create_chest('legendary')
            rooms.append(Room(chest=chest))
        else:
            count = random.randint(1, 3)
            choices = [Skeleton.create_enemy, SkeletonArcher.create_enemy, AgileSkeleton.create_enemy,
                       SpectralSkeleton.create_enemy]
            enemies = [random.choice(choices)() for _ in range(count)]
            rooms.append(Room(enemies=enemies))
    dungeon.add_floor(Floor(rooms))

    rooms2 = []
    num_rooms2 = 10
    chest_chance = 0.3
    for i in range(num_rooms2):
        if random.random() < chest_chance:
            r = random.random()
            if r < 0.50:
                chest = create_chest('wood')
            elif r < 0.85:
                chest = create_chest('silver')
            elif r < 0.895:
                chest = create_chest('gold')
            else:
                chest = create_chest('legendary')
            rooms2.append(Room(chest=chest))
        else:
            count = random.randint(1, 3)
            choices = [SpectralSkeleton.create_enemy, ReinforcedSkeleton.create_enemy, SkeletonMage.create_enemy,
                       BurningSkeleton.create_enemy, PoisonSkeleton.create_enemy]
            enemies = [random.choice(choices)() for _ in range(count)]
            rooms2.append(Room(enemies=enemies))
    dungeon.add_floor(Floor(rooms2))

    rooms3 = []
    num_rooms3 = 10
    chest_chance = 0.2
    for i in range(num_rooms3):
        if random.random() < chest_chance:
            r = random.random()
            if r < 0.30:
                chest = create_chest('wood')
            elif r < 0.70:
                chest = create_chest('silver')
            elif r < 0.90:
                chest = create_chest('gold')
            else:
                chest = create_chest('legendary')
            rooms3.append(Room(chest=chest))
        else:
            count = random.randint(1, 3)
            choices = [GiantSkeleton.create_enemy, NecromancerSkeleton.create_enemy,
                       ArmoredSkeleton.create_enemy]
            enemies = [random.choice(choices)() for _ in range(count)]
            rooms3.append(Room(enemies=enemies))
    dungeon.add_floor(Floor(rooms3))

    if random.random() < 0.4:
        dungeon.add_floor([Kondylos_o_Sarantapus.create_boss()])
    return dungeon

def create_goblin_dungeon():
    dungeon = Dungeon("Donjon Gobelins")
    rooms = []
    num_rooms = 10
    chest_chance = 0.4
    for i in range (num_rooms):
        if random.random() < chest_chance:
            r = random.random()
            if r < 0.70:
                chest = create_chest('wood')
            elif r < 0.95:
                chest = create_chest('silver')
            elif r < 0.995:
                chest = create_chest('gold')
            else:
                chest = create_chest('legendary')
            rooms.append(Room(chest=chest))
        else: 
            count = random.randint(1, 3)
            choices = [Goblin.create_enemy, AgileGoblin.create_enemy, ThiefGoblin.create_enemy,
                       BomberGoblin.create_enemy]
            enemies = [random.choice(choices)() for _ in range(count)]
            rooms.append(Room(enemies=enemies))
    dungeon.add_floor(Floor(rooms))

    rooms2 = []
    num_rooms2 = 10
    chest_chance = 0.3
    for i in range(num_rooms2):
        if random.random() < chest_chance:
            r = random.random()
            if r < 0.50:
                chest = create_chest('wood')
            elif r < 0.85:
                chest = create_chest('silver')
            elif r < 0.895:
                chest = create_chest('gold')
            else:
                chest = create_chest('legendary')
            rooms2.append(Room(chest=chest))
        else:
            count = random.randint(1, 3)
            choices = [BigGoblin.create_enemy, WarriorGoblin.create_enemy, MageGoblin.create_enemy,
                       ArcherGoblin.create_enemy, AlchemistGoblin.create_enemy]
            enemies = [random.choice(choices)() for _ in range(count)]
            rooms2.append(Room(enemies=enemies))
    dungeon.add_floor(Floor(rooms2))

    rooms3 = []
    num_rooms3 = 10
    chest_chance = 0.2
    for i in range(num_rooms3):
        if random.random() < chest_chance:
            r = random.random()
            if r < 0.30:
                chest = create_chest('wood')
            elif r < 0.70:
                chest = create_chest('silver')
            elif r < 0.90:
                chest = create_chest('gold')
            else:
                chest = create_chest('legendary')
            rooms3.append(Room(chest=chest))
        else:
            count = random.randint(1, 3)
            choices = [GoblinChief.create_enemy, ArmoredGoblin.create_enemy,
                       BigGoblin.create_enemy]
            enemies = [random.choice(choices)() for _ in range(count)]
            rooms3.append(Room(enemies=enemies))
    dungeon.add_floor(Floor(rooms3))

    if random.random() < 0.4:
        dungeon.add_floor([Roi_Gobelin.create_boss()])
    return dungeon

def create_troll_dungeon():
    dungeon = Dungeon("Donjon Trolls")
    rooms = []
    num_rooms = 10
    chest_chance = 0.4
    for i in range(num_rooms):
        if random.random() < chest_chance:
            r = random.random()
            if r < 0.70:
                chest = create_chest('wood')
            elif r < 0.95:
                chest = create_chest('silver')
            elif r < 0.995:
                chest = create_chest('gold')
            else:
                chest = create_chest('legendary')
            rooms.append(Room(chest=chest))
        else:
            count = random.randint(1, 3)
            choices = [Troll.create_enemy, CaveTroll.create_enemy, RegeneratingTroll.create_enemy,
                       FireTroll.create_enemy]
            enemies = [random.choice(choices)() for _ in range(count)]
            rooms.append(Room(enemies=enemies))
    dungeon.add_floor(Floor(rooms))

    rooms2 = []
    num_rooms2 = 10
    chest_chance = 0.3
    for i in range(num_rooms2):
        if random.random() < chest_chance:
            r = random.random()
            if r < 0.50:
                chest = create_chest('wood')
            elif r < 0.85:
                chest = create_chest('silver')
            elif r < 0.895:
                chest = create_chest('gold')
            else:
                chest = create_chest('legendary')
            rooms2.append(Room(chest=chest))
        else:
            count = random.randint(1, 3)
            choices = [OlogHai.create_enemy, IceTroll.create_enemy, StormTroll.create_enemy,
                       ShamanTroll.create_enemy]
            enemies = [random.choice(choices)() for _ in range(count)]
            rooms2.append(Room(enemies=enemies))
    dungeon.add_floor(Floor(rooms2))

    rooms3 = []
    num_rooms3 = 10
    chest_chance = 0.2
    for i in range(num_rooms3):
        if random.random() < chest_chance:
            r = random.random()
            if r < 0.30:
                chest = create_chest('wood')
            elif r < 0.70:
                chest = create_chest('silver')
            elif r < 0.90:
                chest = create_chest('gold')
            else:
                chest = create_chest('legendary')
            rooms3.append(Room(chest=chest))
        else:
            count = random.randint(1, 3)
            choices = [NecroticTroll.create_enemy, WarTroll.create_enemy,
                       TrollKing.create_enemy]
            enemies = [random.choice(choices)() for _ in range(count)]
            rooms3.append(Room(enemies=enemies))
    dungeon.add_floor(Floor(rooms3))
    
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