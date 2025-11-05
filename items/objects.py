class Shield:
    def __init__(self, name: str, price: int, defense_bonus: int, allowed_classes: list | None = None):
        self.name = name
        self.price = price
        self.defense_bonus = defense_bonus
        self.allowed_classes = allowed_classes


class WoodenShield(Shield):
    def __init__(self):
        super().__init__("Bouclier en bois", 10, 5)


class BoneShield(Shield):
    def __init__(self):
        super().__init__("Bouclier en os", 20, 8)


class IronShield(Shield):
    def __init__(self):
        super().__init__("Bouclier en fer", 30, 12)


class CopperShield(Shield):
    def __init__(self):
        super().__init__("Bouclier en cuivre", 40, 16)

class EndiumShield(Shield):
    def __init__(self):
        super().__init__("Bouclier en Endium", 500, 30)


class Sword:
    def __init__(self, name: str, price: int, attack_bonus: int, allowed_classes: list | None = None):
        self.name = name
        self.price = price
        self.attack_bonus = attack_bonus
        self.allowed_classes = allowed_classes


class WoodenSword(Sword):
    def __init__(self):
        super().__init__("Épée en bois", 10, 2, allowed_classes=["Warrior"])


class IronSword(Sword):
    def __init__(self):
        super().__init__("Épée en fer", 20, 4, allowed_classes=["Warrior"])


class DiamondSword(Sword):
    def __init__(self):
        super().__init__("Épée en diamant", 30, 6, allowed_classes=["Warrior"])


class Excalibur(Sword):
    def __init__(self):
        super().__init__("Excalibur", 40, 8, allowed_classes=["Warrior"])


class Armor:
    def __init__(self, name: str, price: int, defense_bonus: int, allowed_classes: list | None = None):
        self.name = name
        self.price = price
        self.defense_bonus = defense_bonus
        self.allowed_classes = allowed_classes


class LeatherArmor(Armor):
    def __init__(self):
        super().__init__("Armure en cuir", 10, 1)


class IronArmor(Armor):
    def __init__(self):
        super().__init__("Armure en fer", 20, 2)


class Chainmail(Armor):
    def __init__(self):
        super().__init__("Cotte de mailles", 30, 3)


class EndiumArmor(Armor):
    def __init__(self):
        super().__init__("Armure en Endium", 40, 4)



class Stick:
    def __init__(self, name: str, price: int, magic_bonus: int, allowed_classes: list | None = None):
        self.name = name
        self.price = price
        self.magic_bonus = magic_bonus
        self.allowed_classes = allowed_classes
        self.attack_bonus = magic_bonus


class FireStick(Stick):
    def __init__(self):
        super().__init__("Bâton de feu", 10, 2, allowed_classes=["Mage"])


class IceStick(Stick):
    def __init__(self):
        super().__init__("Bâton de glace", 20, 4, allowed_classes=["Mage"])


class WindStick(Stick):
    def __init__(self):
        super().__init__("Bâton de vent", 30, 6, allowed_classes=["Mage"])


class UltimateStick(Stick):
    def __init__(self):
        super().__init__("Bâton ultime", 40, 8, allowed_classes=["Mage"])



class Dagger:
    def __init__(self, name: str, price: int, attack_bonus: int, allowed_classes: list | None = None):
        self.name = name
        self.price = price
        self.attack_bonus = attack_bonus
        self.allowed_classes = allowed_classes


class WoodenDagger(Dagger):
    def __init__(self):
        super().__init__("Dague en bois", 10, 2, allowed_classes=["Thief"])


class SilverDagger(Dagger):
    def __init__(self):
        super().__init__("Dague en argent", 20, 4, allowed_classes=["Thief"])


class CopperDagger(Dagger):
    def __init__(self):
        super().__init__("Dague en cuivre", 30, 6, allowed_classes=["Thief"])


class GoldDagger(Dagger):
    def __init__(self):
        super().__init__("Dague en or", 40, 8, allowed_classes=["Thief"])



class Bow:
    def __init__(self, name: str, price: int, attack_bonus: int, allowed_classes: list | None = None):
        self.name = name
        self.price = price
        self.attack_bonus = attack_bonus
        self.allowed_classes = allowed_classes


class ClassicBow(Bow):
    def __init__(self):
        super().__init__("Arc classique", 10, 2, allowed_classes=["Archer"])


class LongBow(Bow):
    def __init__(self):
        super().__init__("Arc long", 20, 4, allowed_classes=["Archer"])


class Crossbow(Bow):
    def __init__(self):
        super().__init__("Arbalète", 30, 6, allowed_classes=["Archer"])


class TripleBow(Bow):
    def __init__(self):
        super().__init__("Arc triple", 40, 8, allowed_classes=["Archer"])



class Cape:
    def __init__(self, name: str, price: int, bonus: dict, allowed_classes: list | None = None):
        self.name = name
        self.price = price
        self.bonus = bonus
        self.allowed_classes = allowed_classes

    def apply_effects(self, character):
        pass


class ManaCape(Cape):
    def __init__(self):
        super().__init__("Cape de Mana", 10, {"ManaBonus": 10})


class HealCape(Cape):
    def __init__(self):
        super().__init__("Cape de soin", 15, {"HealBonus": 15})


class DefenseCape(Cape):
    def __init__(self):
        super().__init__("Cape de défense", 5, {"DefenseBonus": 5})


class UltimateCape(Cape):
    def __init__(self):
        super().__init__(
            "Cape ultime",
            40,
            {"ManaBonus": 10, "HealBonus": 15, "DefenseBonus": 5},
        )
 
class potion:
    def __init__(self, name: str, price: int, heal_amount: int):
        self.name = name
        self.price = price
        self.heal_amount = heal_amount

    def use(self, character):
        if not self.usable:
            return 0
        heal_amount = min(self.heal_amount, character.hp_max - character.hp)
        if heal_amount <= 0:
            return 0
        character.increase_hp(heal_amount)
        return heal_amount


class Potion(potion):
    def __init__(self):
        super().__init__("Potion de santé", 10, 10) 

class SuperPotion(potion):
    def __init__(self):
        super().__init__("Super Potion de santé", 25, 25)

class HyperPotion(potion):
    def __init__(self):
        super().__init__("Hyper Potion de santé", 50, 50)

class MaxPotion(potion):
    def __init__(self):
        super().__init__("Potion Max", 100, 1000)


class CoinBag:
    def __init__(self, name: str, coins: int):
        self.name = name
        self.coins_amount = coins

class LittleCoinBag(CoinBag):
    def __init__(self):
        super().__init__("Petit Sac de pièces", 10)

class MediumCoinBag(CoinBag):
    def __init__(self):
        super().__init__("Sac de pièces moyen", 21)

class LargeCoinBag(CoinBag):
    def __init__(self):
        super().__init__("Grand Sac de pièces", 36)

class GiantCoinBag(CoinBag):
    def __init__(self):
        super().__init__("Géant Sac de pièces", 87)


class XPScroll:
    def __init__(self, name: str, exp: int):
        self.name = name
        self.exp_amount = exp

class LittleXPScroll(XPScroll):
    def __init__(self):
        super().__init__("Petit Parchemin d'EXP", 20)

class MediumXPScroll(XPScroll):
    def __init__(self):
        super().__init__("Parchemin d'EXP moyen", 35)

class LargeXPScroll(XPScroll):
    def __init__(self):
        super().__init__("Grand Parchemin d'EXP", 60)

class GiantXPScroll(XPScroll):
    def __init__(self):
        super().__init__("Géant Parchemin d'EXP", 105)

class Charcoal:
    def __init__(self):
        self.name = "Charbon"
        self.price = 1
        self.attack_bonus = 1
        self.allowed_classes = None

class ChairPutrefiee:
    def __init__(self):
        self.name = "Chair putréfiée"
        self.price = 5
        self.allowed_classes = None

class Bone:
    def __init__(self):
        self.name = "Os"
        self.price = 3
        self.allowed_classes = None

ITEM_REGISTRY = {
    WoodenShield().name: WoodenShield,
    BoneShield().name: BoneShield,
    IronShield().name: IronShield,
    CopperShield().name: CopperShield,
    EndiumShield().name: EndiumShield,

    WoodenSword().name: WoodenSword,
    IronSword().name: IronSword,
    DiamondSword().name: DiamondSword,
    Excalibur().name: Excalibur,

    LeatherArmor().name: LeatherArmor,
    IronArmor().name: IronArmor,
    Chainmail().name: Chainmail,
    EndiumArmor().name: EndiumArmor,

    FireStick().name: FireStick,
    IceStick().name: IceStick,
    WindStick().name: WindStick,
    UltimateStick().name: UltimateStick,

    WoodenDagger().name: WoodenDagger,
    SilverDagger().name: SilverDagger,
    CopperDagger().name: CopperDagger,
    GoldDagger().name: GoldDagger,

    ClassicBow().name: ClassicBow,
    LongBow().name: LongBow,
    Crossbow().name: Crossbow,
    TripleBow().name: TripleBow,

    ManaCape().name: ManaCape,
    HealCape().name: HealCape,
    DefenseCape().name: DefenseCape,
    UltimateCape().name: UltimateCape,

    Potion().name: Potion,
    SuperPotion().name: SuperPotion,
    HyperPotion().name: HyperPotion,
    MaxPotion().name: MaxPotion,

    LittleCoinBag().name: LittleCoinBag,
    MediumCoinBag().name: MediumCoinBag,
    LargeCoinBag().name: LargeCoinBag,
    GiantCoinBag().name: GiantCoinBag,

    LittleXPScroll().name: LittleXPScroll,
    MediumXPScroll().name: MediumXPScroll,
    LargeXPScroll().name: LargeXPScroll,
    GiantXPScroll().name: GiantXPScroll,

    Charcoal().name: Charcoal,
    ChairPutrefiee().name: ChairPutrefiee,
    Bone().name: Bone,
}


