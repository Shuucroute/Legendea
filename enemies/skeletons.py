import random
from enemies.base_enemy import BaseEnemy

class Skeleton(BaseEnemy):
    def __init__(self):
        super().__init__(
            name="Squelette", hp=20, attack_value=5, defense_value=3,
            exp_reward=6, coins_reward=5,
        )

    def compute_damages(self, target):
        return super().compute_damages(target) + 3

    def get_loot(self):
        """Retourne les os potentiels lootés par un squelette."""
        from items.objects import Bone
        # 35% de chance de dropper un os
        if random.random() < 0.35:
            return [Bone()]
        return []


class ReinforcedSkeleton(Skeleton):
    def __init__(self):
        super().__init__()
        self.name = "Squelette Renforcé"
        self.hp_max = 30
        self.hp = 30
        self.attack_value = 10
        self.defense_value = 6
        self.exp_reward, self.coins_reward = 12, 7

    def compute_damages(self, target):
        return super().compute_damages(target) + 5

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 3)


class ArmoredSkeleton(ReinforcedSkeleton):
    def __init__(self):
        super().__init__()
        self.name = "Squelette à Armure"
        self.hp_max = 40
        self.hp = 40
        self.attack_value = 12
        self.defense_value = 10
        self.exp_reward, self.coins_reward = 15, 10

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 6)


class SkeletonMage(Skeleton):
    def __init__(self):
        super().__init__()
        self.name = "Squelette Mage"
        self.hp_max = 25
        self.hp = 25
        self.attack_value = 15
        self.defense_value = 2
        self.exp_reward, self.coins_reward = 10, 8

    def compute_damages(self, target):
        base = super().compute_damages(target)
        return base + 8 if self.hp > 10 else base + 4


class AgileSkeleton(Skeleton):
    def __init__(self):
        super().__init__()
        self.name = "Squelette Agile"
        self.hp_max = 18
        self.hp = 18
        self.attack_value = 8
        self.defense_value = 2
        self.exp_reward, self.coins_reward = 8, 6

    def compute_damages(self, target):
        import random
        base = super().compute_damages(target)
        if random.random() < 0.2:
            return base * 2
        return base


class BurningSkeleton(ReinforcedSkeleton):
    def __init__(self):
        super().__init__()
        self.name = "Squelette Enflammé"
        self.hp_max = 35
        self.hp = 35
        self.attack_value = 13
        self.defense_value = 5
        self.exp_reward, self.coins_reward = 14, 9

    def compute_damages(self, target):
        return super().compute_damages(target) + 6

    def on_attack(self, target):
        target.apply_status("brûlure", turns=3, damage_per_turn=2)


class NecromancerSkeleton(SkeletonMage):
    def __init__(self):
        super().__init__()
        self.name = "Squelette Nécromancien"
        self.hp_max = 45
        self.hp = 45
        self.attack_value = 18
        self.defense_value = 6
        self.exp_reward, self.coins_reward = 25, 20

    def compute_damages(self, target):
        return super().compute_damages(target) + 10

    def on_defeat(self):
        return Skeleton()


class SkeletonArcher(Skeleton):
    def __init__(self):
        super().__init__()
        self.name = "Squelette Archer"
        self.hp_max = 22
        self.hp = 22
        self.attack_value = 9
        self.defense_value = 3
        self.exp_reward, self.coins_reward = 9, 7

    def compute_damages(self, target):
        base_damage = super().compute_damages(target)
        return int(base_damage + (target.defense_value * 0.25))


class PoisonSkeleton(ReinforcedSkeleton):
    def __init__(self):
        super().__init__()
        self.name = "Squelette Empoisonné"
        self.hp_max = 28
        self.hp = 28
        self.attack_value = 11
        self.defense_value = 5
        self.exp_reward, self.coins_reward = 13, 9

    def compute_damages(self, target):
        return super().compute_damages(target) + 4

    def on_attack(self, target):
        if hasattr(target, "apply_status"):
            target.apply_status("poison", turns=3, damage_per_turn=2)


class SpectralSkeleton(Skeleton):
    def __init__(self):
        super().__init__()
        self.name = "Squelette Spectral"
        self.hp_max = 18
        self.hp = 18
        self.attack_value = 10
        self.defense_value = 1
        self.exp_reward, self.coins_reward = 15, 10

    def compute_raw_damages(self, damages, attacker):
        import random
        if random.random() < 0.3:
            return 0
        return super().compute_raw_damages(damages, attacker)


class GiantSkeleton(ArmoredSkeleton):
    def __init__(self):
        super().__init__()
        self.name = "Squelette Géant"
        self.hp_max = 80
        self.hp = 80
        self.attack_value = 20
        self.defense_value = 12
        self.exp_reward, self.coins_reward = 35, 25

    def compute_damages(self, target):
        import random
        if random.random() < 0.15:
            return 0
        return super().compute_damages(target) + 12

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 5)
