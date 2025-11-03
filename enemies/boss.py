from game.character import Character

class Boss(Character):
    boss_killed_count = 0
    
    def __init__(self, name="Boss", hp=50, attack_value=20, defense_value=20, exp_reward=1, coins_reward=20):
        super().__init__(name, hp, attack_value, defense_value, exp_reward, coins_reward)
    
    @classmethod
    def increase_boss_killed_count(cls):
        cls.boss_killed_count += 1
        if cls.boss_killed_count == 5:
            print("Cinq Boss sont morts ! Le Balrog apparait !")
            return Balrog.create_mega_boss()

def kill_boss():
    Boss.increase_boss_killed_count()

class Cadaverus_Devorator(Boss):
    def compute_damages(self, target):
        print("Cadaverus Devorator vous attaque ! (+5 dmg)")
        return super().compute_damages(target) + 5
    
    def compute_raw_damages(self, damages, attacker):
        print("Cadaverus Devorator prend des dégâts ! (-5 dmg)")
        raw_damages = super().compute_raw_damages(damages, attacker) - 5
        return max(0, raw_damages)
    
    @classmethod
    def create_boss(cls):
        return cls(name="Cadaverus Devorator", exp_reward=50, coins_reward=30)

class Kondylos_o_Sarantapus(Boss):
    def compute_damages(self, target):
        print("Le Kondylos o Sarantapus vous attaque ! (+6 dmg)")
        return super().compute_damages(target) + 6
    
    def compute_raw_damages(self, damages, attacker):
        print("Le Kondylos o Sarantapus prend des dégâts ! (-4 dmg)")
        raw_damages = super().compute_raw_damages(damages, attacker) - 4
        return max(0, raw_damages)
    
    @classmethod
    def create_boss(cls):
        return cls(name="Kondylos o Sarantapus", exp_reward=55, coins_reward=30)

class Roi_Gobelin(Boss):
    def compute_damages(self, target):
        print("Le Roi Gobelin vous attaque ! (+7 dmg)")
        return super().compute_damages(target) + 7
    
    def compute_raw_damages(self, damages, attacker):
        print("Le Roi Gobelin prend des dégâts ! (-7 dmg)")
        raw_damages = super().compute_raw_damages(damages, attacker) - 7
        return max(0, raw_damages)
    
    @classmethod
    def create_boss(cls):
        return cls(name="Roi Gobelin", exp_reward=55, coins_reward=25)

class Garrok_le_Féroce(Boss):
    def compute_damages(self, target):
        print("Garrok le Féroce vous attaque ! (+10 dmg)")
        return super().compute_damages(target) + 10
    
    def compute_raw_damages(self, damages, attacker):
        print("Garrok le Féroce prend des dégâts ! (-10 dmg)")
        raw_damages = super().compute_raw_damages(damages, attacker) - 10
        return max(0, raw_damages)
    
    @classmethod
    def create_boss(cls):
        return cls(name="Garrok le Féroce", exp_reward=60, coins_reward=26)

class Balrog(Character):
    def __init__(self, name="Balrog", hp=120, attack_value=45, defense_value=35, exp_reward=300, coins_reward=100):
        super().__init__(name, hp, attack_value, defense_value, exp_reward, coins_reward)
    
    @classmethod
    def summon_balrog(cls):
        print("Cinq Boss sont morts ! Le Balrog apparait !")
        return cls()
    
    @classmethod
    def create_mega_boss(cls):
        return cls(exp_reward=300, coins_reward=150)