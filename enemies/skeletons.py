from enemies.base_enemy import BaseEnemy

class Skeleton(BaseEnemy):
    def __init__(self):
        super().__init__(
            name="Squelette", hp=20, attack_value=5, defense_value=3,
            exp_reward=6, coins_reward=5,
        )

    def compute_damages(self,target):
        return super().compute_damages(target) + 3


class ReinforcedSkeleton(Skeleton):
    def __init__(self):
        super().__init__()
        self.name = "Squelette Renforcé"
        self.hp, self.attack_value, self.defense_value = 30, 10, 6
        self.exp_reward, self.coins_reward = 12, 7

    def compute_damages(self, target):
        return super().compute_damages(target) + 5

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 3)


class ArmoredSkeleton(ReinforcedSkeleton):
    def __init__(self):
        super().__init__()
        self.name = "Squelette à Armure"
        self.hp, self.attack_value, self.defense_value = 40, 12, 10
        self.exp_reward, self.coins_reward = 15, 10

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 6)
