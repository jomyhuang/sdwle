from SDWLE.cards.base import WeaponCard
from SDWLE.game_objects import Weapon
from SDWLE.tags.action import Give, DecreaseDurability, Heal, Joust, IncreaseDurability
from SDWLE.tags.condition import IsHero
from SDWLE.tags.event import MinionSummoned, CharacterAttack
from SDWLE.tags.selector import TargetSelector, HeroSelector, MinionSelector, RandomPicker, WeaponSelector, \
    SelfSelector
from SDWLE.tags.base import Buff, Effect, Battlecry, ActionTag
from SDWLE.tags.status import DivineShield, Taunt, ChangeAttack, ChangeHealth
from SDWLE.constants import CHARACTER_CLASS, CARD_RARITY


class LightsJustice(WeaponCard):
    def __init__(self):
        super().__init__("Light's Justice", 1, CHARACTER_CLASS.PALADIN, CARD_RARITY.FREE)

    def create_weapon(self, player):
        return Weapon(1, 4)


class SwordOfJustice(WeaponCard):
    def __init__(self):
        super().__init__("Sword of Justice", 3, CHARACTER_CLASS.PALADIN, CARD_RARITY.EPIC)

    def create_weapon(self, player):
        return Weapon(1, 5, effects=[Effect(MinionSummoned(), ActionTag(Give([Buff(ChangeAttack(1)),
                                                                              Buff(ChangeHealth(1))]),
                                            TargetSelector())),
                                     Effect(MinionSummoned(), ActionTag(DecreaseDurability(), WeaponSelector()))])


class TruesilverChampion(WeaponCard):
    def __init__(self):
        super().__init__("Truesilver Champion", 4, CHARACTER_CLASS.PALADIN, CARD_RARITY.COMMON)

    def create_weapon(self, player):
        return Weapon(4, 2, effects=[Effect(CharacterAttack(IsHero()), ActionTag(Heal(2), HeroSelector()))])


class Coghammer(WeaponCard):
    def __init__(self):
        super().__init__("Coghammer", 3, CHARACTER_CLASS.PALADIN, CARD_RARITY.EPIC,
                         battlecry=Battlecry(Give([Buff(DivineShield()), Buff(Taunt())]),
                                             MinionSelector(picker=RandomPicker())))

    def create_weapon(self, player):
        return Weapon(2, 3)


class ArgentLance(WeaponCard):
    def __init__(self):
        super().__init__("Argent Lance", 2, CHARACTER_CLASS.PALADIN, CARD_RARITY.RARE,
                         battlecry=Battlecry(Joust(IncreaseDurability()), SelfSelector()))

    def create_weapon(self, player):
        return Weapon(2, 2)
