from enemies.base_enemy import BaseEnemy

class Goblin(BaseEnemy):
    def __init__(self):
        super().__init__(
            name="Gobelin", hp=20, attack_value=5, defense_value=5,
            exp_reward=7, coins_reward=7,
        )


class BigGoblin(Goblin):
    def __init__(self):
        super().__init__()
        self.name = "Gros Gobelin"
        self.hp_max = 40
        self.hp = 40
        self.attack_value = 10
        self.defense_value = 8
        self.exp_reward, self.coins_reward = 18, 12

    def compute_damages(self, target):
        return super().compute_damages(target) + 5

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 4)
