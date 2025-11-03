from enemies.base_enemy import BaseEnemy

class Troll(BaseEnemy):
    def __init__(self):
        super().__init__(
            name="Troll", hp=35, attack_value=15, defense_value=10,
            exp_reward=25, coins_reward=15,
        )


class OlogHai(Troll):
    def __init__(self):
        super().__init__()
        self.name = "Olog-Hai"
        self.hp, self.attack_value, self.defense_value = 50, 20, 15
        self.exp_reward, self.coins_reward = 30, 20

    def compute_damages(self, target):
        return super().compute_damages(target) + 5
