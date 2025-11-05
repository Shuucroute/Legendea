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
        self.hp_max = 50
        self.hp = 50
        self.attack_value = 20
        self.defense_value = 15
        self.exp_reward, self.coins_reward = 30, 20

    def compute_damages(self, target):
        return super().compute_damages(target) + 5


class CaveTroll(Troll):
    def __init__(self):
        super().__init__()
        self.name = "Troll des Cavernes"
        self.hp_max = 45
        self.hp = 45
        self.attack_value = 17
        self.defense_value = 8
        self.exp_reward, self.coins_reward = 28, 18

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 3)


class RegeneratingTroll(Troll):
    def __init__(self):
        super().__init__()
        self.name = "Troll Régénérant"
        self.hp_max = 40
        self.hp = 40
        self.attack_value = 14
        self.defense_value = 9
        self.exp_reward, self.coins_reward = 27, 16
        self.regen_value = 3

    def on_turn_end(self):
        self.hp = min(self.hp_max, self.hp + self.regen_value)


class FireTroll(Troll):
    def __init__(self):
        super().__init__()
        self.name = "Troll de Feu"
        self.hp_max = 38
        self.hp = 38
        self.attack_value = 22
        self.defense_value = 8
        self.exp_reward, self.coins_reward = 32, 22

    def compute_damages(self, target):
        return super().compute_damages(target) + 8

    def on_attack(self, target):
        if hasattr(target, "apply_status"):
            target.apply_status("brûlure", turns=3, damage_per_turn=3)


class IceTroll(Troll):
    def __init__(self):
        super().__init__()
        self.name = "Troll des Glaces"
        self.hp_max = 42
        self.hp = 42
        self.attack_value = 18
        self.defense_value = 11
        self.exp_reward, self.coins_reward = 30, 20

    def on_attack(self, target):
        if hasattr(target, "apply_status"):
            target.apply_status("gel", turns=1)


class StormTroll(Troll):
    def __init__(self):
        super().__init__()
        self.name = "Troll des Tempêtes"
        self.hp_max = 45
        self.hp = 45
        self.attack_value = 25
        self.defense_value = 10
        self.exp_reward, self.coins_reward = 35, 25

    def compute_damages(self, target):
        import random
        base = super().compute_damages(target)
        if random.random() < 0.2:
            return base * 2
        return base + 5


class ShamanTroll(Troll):
    def __init__(self):
        super().__init__()
        self.name = "Troll Chaman"
        self.hp_max = 36
        self.hp = 36
        self.attack_value = 16
        self.defense_value = 8
        self.exp_reward, self.coins_reward = 28, 19

    def compute_damages(self, target):
        base = super().compute_damages(target)
        return base + int(target.defense_value * 0.5)


class NecroticTroll(Troll):
    def __init__(self):
        super().__init__()
        self.name = "Troll Nécrotique"
        self.hp_max = 40
        self.hp = 40
        self.attack_value = 19
        self.defense_value = 9
        self.exp_reward, self.coins_reward = 33, 23

    def on_attack(self, target):
        damage = super().compute_damages(target)
        self.hp = min(self.hp_max, self.hp + 3)
        return damage


class WarTroll(OlogHai):
    def __init__(self):
        super().__init__()
        self.name = "Troll de Guerre"
        self.hp_max = 60
        self.hp = 60
        self.attack_value = 25
        self.defense_value = 17
        self.exp_reward, self.coins_reward = 40, 28

    def compute_damages(self, target):
        return super().compute_damages(target) + 10


class TrollKing(WarTroll):
    def __init__(self):
        super().__init__()
        self.name = "Roi des Trolls"
        self.hp_max = 100
        self.hp = 100
        self.attack_value = 30
        self.defense_value = 20
        self.exp_reward, self.coins_reward = 80, 50

    def compute_damages(self, target):
        return super().compute_damages(target) + 15

    def on_turn_start(self):
        pass
