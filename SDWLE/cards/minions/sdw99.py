from SDWLE.cards.base import MinionCard
from SDWLE.cards.heroes import Ragnaros
from SDWLE.game_objects import Minion
from SDWLE.constants import CARD_RARITY, CHARACTER_CLASS, MINION_TYPE, TROOP_TYPE

# from SDWLE.tags.action import Heal, Summon, Draw, \
#     Kill, Damage, ResurrectFriendly, Steal, Duplicate, Give, SwapWithHand, AddCard, Transform, ApplySecret, \
#     Silence, Bounce, GiveManaCrystal, Equip, GiveAura, Replace, SetHealth, ChangeTarget, Discard, \
#     RemoveDivineShields, DecreaseDurability, IncreaseDurability, IncreaseWeaponAttack, Destroy, GiveEffect, SwapStats, \
#     Joust, RemoveFromDeck, RemoveSecret
# from SDWLE.tags.base import Effect, Deathrattle, Battlecry, Aura, BuffUntil, Buff, AuraUntil, ActionTag
# from SDWLE.tags.card_source import CardList, LastCard, DeckSource, Same, CollectionSource
# from SDWLE.tags.condition import Adjacent, IsType, MinionHasDeathrattle, IsMinion, IsSecret, \
#     MinionIsTarget, IsSpell, IsDamaged, InGraveyard, ManaCost, OpponentMinionCountIsGreaterThan, AttackGreaterThan, \
#     IsWeapon, HasStatus, AttackLessThanOrEqualTo, OneIn, NotCurrentTarget, HasDivineShield, HasSecret, \
#     BaseAttackEqualTo, GreaterThan, And, TargetAdjacent, Matches, HasBattlecry, Not, IsRarity, MinionIsNotTarget, \
#     IsClass
# from SDWLE.tags.event import TurnEnded, CardPlayed, MinionSummoned, TurnStarted, DidDamage, AfterAdded, \
#     SpellCast, CharacterHealed, CharacterDamaged, MinionDied, CardUsed, Damaged, Attack, CharacterAttack, \
#     MinionPlaced, CardDrawn, SpellTargeted, UsedPower
# from SDWLE.tags.selector import MinionSelector, BothPlayer, SelfSelector, \
#     PlayerSelector, TargetSelector, EnemyPlayer, CharacterSelector, WeaponSelector, \
#     HeroSelector, OtherPlayer, UserPicker, RandomPicker, CurrentPlayer, Count, Attribute, CardSelector, \
#     Difference, LastDrawnSelector, RandomAmount, DeadMinionSelector, FriendlyPlayer
# from SDWLE.tags.status import ChangeAttack, ChangeHealth, Charge, Taunt, Windfury, CantAttack, \
#     SpellDamage, DoubleDeathrattle, Frozen, ManaChange, DivineShield, MegaWindfury, CanAttack
import SDWLE.targeting
import copy


class SDW01(MinionCard):
    def __init__(self):
        super().__init__("雷伊", 1, CHARACTER_CLASS.ALL, CARD_RARITY.FREE,
                         minion_type=MINION_TYPE.BEAST)


    def create_minion(self, player):
        return Minion(100, 150, troop=TROOP_TYPE.A)


class SDW02(MinionCard):
    def __init__(self):
        super().__init__("布莱克", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         minion_type=MINION_TYPE.BEAST)


    def create_minion(self, player):
        return Minion(110, 120, troop=TROOP_TYPE.T)


class SDW03(MinionCard):
    def __init__(self):
        super().__init__("卡修斯", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         minion_type=MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(130, 150, troop=TROOP_TYPE.H)


class SDW04(MinionCard):
    def __init__(self):
        super().__init__("盖亚", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         minion_type=MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(150, 180, troop=TROOP_TYPE.A)


