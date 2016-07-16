from SDWLE.cards.base import WeaponCard
from SDWLE.game_objects import Weapon
from SDWLE.tags.action import Give, IncreaseDurability
from SDWLE.tags.condition import IsHero
from SDWLE.tags.event import AttackCompleted, SecretRevealed, CharacterAttack
from SDWLE.tags.selector import HeroSelector, MinionSelector, RandomPicker, WeaponSelector
from SDWLE.constants import CHARACTER_CLASS, CARD_RARITY
from SDWLE.tags.base import Effect, BuffUntil, Battlecry, ActionTag
from SDWLE.tags.status import ChangeAttack, Immune


class EaglehornBow(WeaponCard):
    def __init__(self):
        super().__init__("Eaglehorn Bow", 3, CHARACTER_CLASS.HUNTER,
                         CARD_RARITY.RARE)

    def create_weapon(self, player):
        return Weapon(3, 2, effects=[Effect(SecretRevealed(), ActionTag(IncreaseDurability(), WeaponSelector()))])


class GladiatorsLongbow(WeaponCard):
    def __init__(self):
        super().__init__("Gladiator's Longbow", 7, CHARACTER_CLASS.HUNTER,
                         CARD_RARITY.EPIC)

    def create_weapon(self, player):
        return Weapon(5, 2, effects=[Effect(CharacterAttack(IsHero()),
                                            ActionTag(Give(BuffUntil(Immune(), AttackCompleted())), HeroSelector()))])


class Glaivezooka(WeaponCard):
    def __init__(self):
        super().__init__("Glaivezooka", 2, CHARACTER_CLASS.HUNTER, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Give(ChangeAttack(1)), MinionSelector(None, picker=RandomPicker())))

    def create_weapon(self, player):
        return Weapon(2, 2)
