from __future__ import annotations
import random
from typing import List, Dict, Any, Iterable, Tuple
from items.objects import ITEM_REGISTRY



def _weighted_sample_without_replacement(population: Iterable[str], weights: Dict[str, int], k: int) -> List[str]:
    pop = [p for p in population]
    w = {p: weights.get(p, 0) for p in pop}
    picked: List[str] = []
    for _ in range(min(k, len(pop))):
        total = sum(w[p] for p in pop)
        if total <= 0:
            break
        r = random.uniform(0, total)
        cum = 0.0
        for p in pop:
            cum += w[p]
            if r <= cum:
                picked.append(p)
                pop.remove(p)
                break
    return picked


class Chest:
    def __init__(self, name: str):
        self.name = name
        self.items: List[Any] = []
        self.opened: bool = False

    def describe(self) -> str:
        if self.opened:
            if not self.items:
                return f"{self.name} (ouvert) — vide"
            names = ", ".join(getattr(it, "name", str(it)) for it in self.items)
            return f"{self.name} (ouvert) — Contient: {names}"
        return f"{self.name} (fermé) — Contient un nombre d'objets aléatoire"

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "opened": self.opened, "items": [getattr(i, "name", str(i)) for i in self.items]}

    def open(self) -> List[Any]:
        if self.opened:
            return []
        self.opened = True
        taken = list(self.items)
        self.items = []
        return taken


WOODEN_WEIGHTS: Dict[str, int] = {
    "Potion de santé": 40,
    "Épée en bois": 50,
    "Bouclier en bois": 50,
    "Armure en cuir": 41,
    "Dague en bois": 50,
    "Arc classique": 50,
    "Cape de défense": 41,
    "Charbon": 50,
    "Petit Sac de pièces": 45,
    "Parchemin d'EXP moyen": 15,
    "Grand Parchemin d'EXP": 5,
    "Géant Parchemin d'EXP": 0.5,
    "Petit Parchemin d'EXP": 45,
    "Sac de pièces moyen": 15,
    "Grand Sac de pièces": 5,
    "Sac de pièces large": 0.5,
}

SILVER_WEIGHTS: Dict[str, int] = {
    "Charbon": 35,
    "Épée en bois": 35,
    "Super Potion de santé": 45,
    "Épée en fer": 40,
    "Bouclier en fer": 40,
    "Armure en fer": 40,
    "Dague en argent": 40,
    "Arc long": 40,
    "Bâton de feu": 40,
    "Cape de Mana": 20,
    "Petit Sac de pièces": 35,
    "Parchemin d'EXP moyen": 35,
    "Grand Parchemin d'EXP": 15,
    "Géant Parchemin d'EXP": 4.5,
    "Petit Parchemin d'EXP": 35,
    "Sac de pièces moyen": 35,
    "Grand Sac de pièces": 15,
    "Sac de pièces large": 4.5,
}

GOLD_WEIGHTS: Dict[str, int] = {
    "Hyper Potion de santé": 20,
    "Épée en diamant": 25,
    "Bouclier en os": 70,
    "Cotte de mailles": 25,
    "Dague en cuivre": 25,
    "Arbalète": 25,
    "Bâton de vent": 25,
    "Cape de soin": 25,
    "Armure en Endium": 25,
    "Petit Sac de pièces": 45,
    "Parchemin d'EXP moyen": 15,
    "Grand Parchemin d'EXP": 5,
    "Géant Parchemin d'EXP": 0.5,
    "Petit Parchemin d'EXP": 45,
    "Sac de pièces moyen": 15,
    "Grand Sac de pièces": 5,
    "Sac de pièces large": 0.5,
}

LEGENDARY_WEIGHTS: Dict[str, int] = {
    "Potion Max": 40,
    "Excalibur": 15,
    "Bâton ultime": 15,
    "Dague en or": 15,
    "Arc triple": 15,
    "Cape ultime": 15,
    "Épée en diamant": 45,
    "Bâton de feu": 45,
    "Petit Sac de pièces": 65,
    "Parchemin d'EXP moyen": 55,
    "Grand Parchemin d'EXP": 35,
    "Géant Parchemin d'EXP": 25,
    "Petit Parchemin d'EXP": 65,
    "Sac de pièces moyen": 55,
    "Grand Sac de pièces": 35,
    "Sac de pièces large": 25,
}


class RarityChest(Chest):
    def __init__(self, name: str, weights: Dict[str, int], num_range: Tuple[int, int], allow_duplicates: bool = True):
        super().__init__(name)
        self.weights = weights
        self.num_range = num_range
        self.allow_duplicates = allow_duplicates
        self.generate_contents()

    def generate_contents(self) -> None:
        pool = [k for k in self.weights.keys() if k in ITEM_REGISTRY]
        if not pool:
            self.items = []
            return

        count = random.randint(self.num_range[0], self.num_range[1])

        if self.allow_duplicates:
            population = pool
            w = [self.weights.get(p, 0) for p in population]
            chosen_keys = random.choices(population, weights=w, k=count)
        else:
            chosen_keys = _weighted_sample_without_replacement(pool, self.weights, count)

        chosen_instances: List[Any] = []
        for key in chosen_keys:
            cls = ITEM_REGISTRY.get(key)
            if cls is None:
                continue
            try:
                chosen_instances.append(cls())
            except Exception:
                chosen_instances.append(key)

        self.items = chosen_instances


class WoodenChest(RarityChest):
    def __init__(self, num_items: Tuple[int, int] | None = None, allow_duplicates: bool = True):
        num_range = num_items if num_items is not None else (1, 1)
        super().__init__("Coffre en bois", WOODEN_WEIGHTS, num_range, allow_duplicates)


class SilverChest(RarityChest):
    def __init__(self, num_items: Tuple[int, int] | None = None, allow_duplicates: bool = True):
        num_range = num_items if num_items is not None else (1, 1)
        super().__init__("Coffre en argent", SILVER_WEIGHTS, num_range, allow_duplicates)


class GoldenChest(RarityChest):
    def __init__(self, num_items: Tuple[int, int] | None = None, allow_duplicates: bool = True):
        num_range = num_items if num_items is not None else (1, 1)
        super().__init__("Coffre doré", GOLD_WEIGHTS, num_range, allow_duplicates)


class LegendaryChest(RarityChest):
    def __init__(self, num_items: Tuple[int, int] | None = None, allow_duplicates: bool = False):
        num_range = num_items if num_items is not None else (1, 1)
        super().__init__("Coffre légendaire", LEGENDARY_WEIGHTS, num_range, allow_duplicates)


def create_chest(rarity: str, **kwargs) -> Chest:
    rarity = rarity.lower()
    if rarity in ("wood", "wooden", "bois"):
        return WoodenChest(**kwargs)
    if rarity in ("silver", "argent"):
        return SilverChest(**kwargs)
    if rarity in ("gold", "golden", "doré", "dore"):
        return GoldenChest(**kwargs)
    if rarity in ("legendary", "légendaire", "legendaire"):
        return LegendaryChest(**kwargs)
    raise ValueError(f"Rareté inconnue: {rarity}")


__all__ = ["Chest", "WoodenChest", "SilverChest", "GoldenChest", "LegendaryChest", "create_chest"]


if __name__ == "__main__":
    for cls in (WoodenChest, SilverChest, GoldenChest, LegendaryChest):
        c = cls()
        print(c.describe())
        items = c.open()
        print(" -> Obtenu:", [getattr(i, "name", str(i)) for i in items])
        print()

