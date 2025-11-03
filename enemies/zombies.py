from enemies.base_enemy import BaseEnemy

class Zombie(BaseEnemy):
    def __init__(self):
        super().__init__(
            name="Zombie", hp=20, attack_value=15, defense_value=5,
            exp_reward=5, coins_reward=5,
        )

class Zombie2_0(Zombie):
    def __init__(self):
        super().__init__()
        self.name = "Zombie Robuste"
        self.hp, self.attack_value, self.defense_value = 30, 18, 8
        self.exp_reward, self.coins_reward = 10, 7

    def compute_damages(self, target):
        return super().compute_damages( target) + 2

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 2)


class ZombieGuerrier(Zombie):
    def __init__(self):
        super().__init__()
        self.name = "Zombie Guerrier"
        self.hp, self.attack_value, self.defense_value = 40, 20, 10
        self.exp_reward, self.coins_reward = 15, 10

    def compute_damages(self, target):
        return super().compute_damages(target) + 5

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 5)
