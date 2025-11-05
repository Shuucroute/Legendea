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


class ThiefGoblin(Goblin):
    def __init__(self):
        super().__init__()
        self.name = "Gobelin Voleur"
        self.hp_max = 18
        self.hp = 18
        self.attack_value = 7
        self.defense_value = 3
        self.exp_reward, self.coins_reward = 9, 10

    def on_attack(self, target):
        stolen = 2
        if hasattr(target, "coins"):
            target.coins = max(0, target.coins - stolen)
        self.coins_reward += stolen


class WarriorGoblin(Goblin):
    def __init__(self):
        super().__init__()
        self.name = "Gobelin Guerrier"
        self.hp_max = 30
        self.hp = 30
        self.attack_value = 9
        self.defense_value = 7
        self.exp_reward, self.coins_reward = 12, 8

    def compute_damages(self, target):
        return super().compute_damages(target) + 4


class MageGoblin(Goblin):
    def __init__(self):
        super().__init__()
        self.name = "Gobelin Sorcier"
        self.hp_max = 22
        self.hp = 22
        self.attack_value = 13
        self.defense_value = 3
        self.exp_reward, self.coins_reward = 15, 10

    def compute_damages(self, target):
        base = super().compute_damages(target)
        return base + 6 if self.hp > (self.hp_max / 2) else base + 3


class ArcherGoblin(Goblin):
    def __init__(self):
        super().__init__()
        self.name = "Gobelin Archer"
        self.hp_max = 24
        self.hp = 24
        self.attack_value = 8
        self.defense_value = 4
        self.exp_reward, self.coins_reward = 11, 8

    def compute_damages(self, target):
        base = super().compute_damages(target)
        return int(base + target.defense_value * 0.2)


class AlchemistGoblin(Goblin):
    def __init__(self):
        super().__init__()
        self.name = "Gobelin Alchimiste"
        self.hp_max = 28
        self.hp = 28
        self.attack_value = 7
        self.defense_value = 4
        self.exp_reward, self.coins_reward = 13, 9

    def on_attack(self, target):
        import random
        if random.random() < 0.25:
            target.apply_status("brûlure", turns=2, damage_per_turn=3)


class ArmoredGoblin(BigGoblin):
    def __init__(self):
        super().__init__()
        self.name = "Gobelin Blindé"
        self.hp_max = 45
        self.hp = 45
        self.attack_value = 11
        self.defense_value = 12
        self.exp_reward, self.coins_reward = 20, 15

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 5)


class AgileGoblin(Goblin):
    def __init__(self):
        super().__init__()
        self.name = "Gobelin Agile"
        self.hp_max = 16
        self.hp = 16
        self.attack_value = 6
        self.defense_value = 2
        self.exp_reward, self.coins_reward = 9, 7

    def compute_damages(self, target):
        import random
        base = super().compute_damages(target)
        if random.random() < 0.25:
            return base * 2
        return base


class BomberGoblin(Goblin):
    def __init__(self):
        super().__init__()
        self.name = "Gobelin Kamikaze"
        self.hp_max = 15
        self.hp = 15
        self.attack_value = 20
        self.defense_value = 1
        self.exp_reward, self.coins_reward = 16, 10

    def compute_damages(self, target):
        dmg = super().compute_damages(target) + 10
        self.hp = 0
        return dmg


class GoblinChief(ArmoredGoblin):
    def __init__(self):
        super().__init__()
        self.name = "Chef Gobelin"
        self.hp_max = 70
        self.hp = 70
        self.attack_value = 18
        self.defense_value = 15
        self.exp_reward, self.coins_reward = 40, 30

    def compute_damages(self, target):
        return super().compute_damages(target) + 10

