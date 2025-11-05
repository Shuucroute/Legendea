import random
from enemies.base_enemy import BaseEnemy

class Zombie(BaseEnemy):
    def __init__(self):
        super().__init__(
            name="Zombie", hp=20, attack_value=15, defense_value=5,
            exp_reward=5, coins_reward=5,
        )
    
    def get_loot(self):
        """Retourne le loot potentiel du zombie (chance de drop de chair putréfiée)."""
        from items.objects import ChairPutrefiee
        
        if random.random() < 0.30:
            return [ChairPutrefiee()]
        return []


class ZombieFaible(Zombie):
    def __init__(self):
        super().__init__()
        self.name = "Zombie Faible"
        self.hp_max = 10
        self.hp = 10
        self.attack_value = 8
        self.defense_value = 2
        self.exp_reward = 2
        self.coins_reward = 1

    def compute_damages(self, target):
        return super().compute_damages(target) - 2


class Zombie2_0(Zombie):
    def __init__(self):
        super().__init__()
        self.name = "Zombie Robuste"
        self.hp_max = 30
        self.hp = 30
        self.attack_value = 18
        self.defense_value = 8
        self.exp_reward = 10
        self.coins_reward = 7

    def compute_damages(self, target):
        return super().compute_damages(target) + 2

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 2)


class ZombieGuerrier(Zombie):
    def __init__(self):
        super().__init__()
        self.name = "Zombie Guerrier"
        self.hp_max = 40
        self.hp = 40
        self.attack_value = 20
        self.defense_value = 10
        self.exp_reward = 15
        self.coins_reward = 10

    def compute_damages(self, target):
        return super().compute_damages(target) + 5

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 5)


class ZombieElite(ZombieGuerrier):
    def __init__(self):
        super().__init__()
        self.name = "Zombie Élite"
        self.hp_max = 60
        self.hp = 60
        self.attack_value = 25
        self.defense_value = 12
        self.exp_reward = 25
        self.coins_reward = 15

    def compute_damages(self, target):
        return super().compute_damages(target) + 3

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 3)


class ZombieMage(Zombie):
    def __init__(self):
        super().__init__()
        self.name = "Zombie Mage"
        self.hp_max = 25
        self.hp = 25
        self.attack_value = 30 
        self.defense_value = 4
        self.exp_reward = 20
        self.coins_reward = 12

    def compute_damages(self, target):
        return super().compute_damages(target) + 10

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker))
    
    
class ZombieRapide(Zombie):
    def __init__(self):
        super().__init__()
        self.name = "Zombie Rapide"
        self.hp_max = 15
        self.hp = 15
        self.attack_value = 12
        self.defense_value = 3
        self.exp_reward = 6
        self.coins_reward = 4

    def compute_damages(self, target):
        return super().compute_damages(target) + 1


class ZombieLent(Zombie):
    def __init__(self):
        super().__init__()
        self.name = "Zombie Lent"
        self.hp_max = 35
        self.hp = 35
        self.attack_value = 10
        self.defense_value = 10
        self.exp_reward = 8
        self.coins_reward = 6

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 1)


class ZombieRegenerant(Zombie):
    def __init__(self):
        super().__init__()
        self.name = "Zombie Régénérant"
        self.hp_max = 28
        self.hp = 28
        self.attack_value = 13
        self.defense_value = 6
        self.exp_reward = 12
        self.coins_reward = 10

    def end_turn_effect(self):
        """Régénère un peu de vie à la fin de son tour."""
        regen = 2
        self.hp = min(self.hp_max, self.hp + regen)
        return regen


class ZombieExplosif(Zombie):
    def __init__(self):
        super().__init__()
        self.name = "Zombie Explosif"
        self.hp_max = 18
        self.hp = 18
        self.attack_value = 16
        self.defense_value = 3
        self.exp_reward = 15
        self.coins_reward = 10

    def on_death(self, target):
        """Explose à sa mort, infligeant des dégâts de zone."""
        explosion_damage = 10
        return {"explosion": explosion_damage}


class ZombieBlindé(Zombie):
    def __init__(self):
        super().__init__()
        self.name = "Zombie Blindé"
        self.hp_max = 45
        self.hp = 45
        self.attack_value = 12
        self.defense_value = 15
        self.exp_reward = 18
        self.coins_reward = 12

    def compute_raw_damages(self, damages, attacker):
        return max(0, super().compute_raw_damages(damages, attacker) - 3)