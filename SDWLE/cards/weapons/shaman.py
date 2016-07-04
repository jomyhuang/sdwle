from SDWLE.cards.base import WeaponCard
from SDWLE.constants import CHARACTER_CLASS, CARD_RARITY, MINION_TYPE
from SDWLE.game_objects import Weapon
from SDWLE.tags.action import Give
from SDWLE.tags.base import Buff, Deathrattle
from SDWLE.tags.condition import IsType
from SDWLE.tags.status import Windfury, ChangeAttack, ChangeHealth
from SDWLE.tags.selector import MinionSelector, RandomPicker


class Doomhammer(WeaponCard):
    def __init__(self):
        super().__init__("Doomhammer", 5, CHARACTER_CLASS.SHAMAN, CARD_RARITY.EPIC, overload=2)

    def create_weapon(self, player):
        return Weapon(2, 8, buffs=[Buff(Windfury())])


class StormforgedAxe(WeaponCard):
    def __init__(self):
        super().__init__("Stormforged Axe", 2, CHARACTER_CLASS.SHAMAN, CARD_RARITY.COMMON, overload=1)

    def create_weapon(self, player):
        return Weapon(2, 3)


class Powermace(WeaponCard):
    def __init__(self):
        super().__init__("Powermace", 3, CHARACTER_CLASS.SHAMAN, CARD_RARITY.RARE)

    def create_weapon(self, player):
        return Weapon(3, 2, deathrattle=Deathrattle(Give([Buff(ChangeHealth(2)), Buff(ChangeAttack(2))]),
                                                    MinionSelector(IsType(MINION_TYPE.MECH), picker=RandomPicker())))
