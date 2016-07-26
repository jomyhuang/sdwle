from SDWLE.cards.base import MinionCard
from SDWLE.cards.heroes import Ragnaros
from SDWLE.game_objects import Minion
from SDWLE.constants import CARD_RARITY, CHARACTER_CLASS, MINION_TYPE, TROOP_TYPE, COLOR_TYPE, NATURE_TYPE

from SDWLE.tags.action import Heal, Summon, Draw, \
    Kill, Damage, ResurrectFriendly, Steal, Duplicate, Give, SwapWithHand, AddCard, Transform, ApplySecret, \
    Silence, Bounce, GiveManaCrystal, Equip, GiveAura, Replace, SetHealth, ChangeTarget, Discard, \
    RemoveDivineShields, DecreaseDurability, IncreaseDurability, IncreaseWeaponAttack, Destroy, GiveEffect, SwapStats, \
    Joust, RemoveFromDeck, RemoveSecret
from SDWLE.tags.base import Effect, Deathrattle, Battlecry, Aura, BuffUntil, Buff, AuraUntil, ActionTag, \
    EngageAttack, EngageDefender, EngageSupporter, BuffOneTurn, EngageWin, EngageDraw, EngageLose
from SDWLE.tags.card_source import CardList, LastCard, DeckSource, Same, CollectionSource
from SDWLE.tags.condition import Adjacent, IsType, MinionHasDeathrattle, IsMinion, IsSecret, \
    MinionIsTarget, IsSpell, IsDamaged, InGraveyard, ManaCost, OpponentMinionCountIsGreaterThan, AttackGreaterThan, \
    IsWeapon, HasStatus, AttackLessThanOrEqualTo, OneIn, NotCurrentTarget, HasDivineShield, HasSecret, \
    BaseAttackEqualTo, GreaterThan, And, TargetAdjacent, Matches, HasBattlecry, Not, IsRarity, MinionIsNotTarget, \
    IsClass
from SDWLE.tags.event import TurnEnded, CardPlayed, MinionSummoned, TurnStarted, DidDamage, AfterAdded, \
    SpellCast, CharacterHealed, CharacterDamaged, MinionDied, CardUsed, Damaged, Attack, CharacterAttack, \
    MinionPlaced, CardDrawn, SpellTargeted, UsedPower
from SDWLE.tags.selector import MinionSelector, BothPlayer, SelfSelector, \
    PlayerSelector, TargetSelector, EnemyPlayer, CharacterSelector, WeaponSelector, \
    HeroSelector, OtherPlayer, UserPicker, RandomPicker, CurrentPlayer, Count, Attribute, CardSelector, \
    Difference, LastDrawnSelector, RandomAmount, DeadMinionSelector, FriendlyPlayer
from SDWLE.tags.status import ChangeAttack, ChangeHealth, Charge, Taunt, Windfury, CantAttack, \
    SpellDamage, DoubleDeathrattle, Frozen, ManaChange, DivineShield, MegaWindfury, CanAttack
import SDWLE.targeting
import copy


class SDW01(MinionCard):
    def __init__(self):
        super().__init__("雷伊", 1, CHARACTER_CLASS.ALL, CARD_RARITY.FREE,
                         color=COLOR_TYPE.YELLOW, star=9, nature=NATURE_TYPE.THUNDER,
                         alliance='战神联盟', rank=None, ID='SDW01', boxset='01',
                         minion_type=MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(100, 150, attack_name='普通攻击', attack_sp_name='瞬间一击', troop=TROOP_TYPE.A)


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


class SDWBasicA(MinionCard):
    def __init__(self):
        super().__init__("Basic A", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         minion_type=MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(100, 120, troop=TROOP_TYPE.A)


class SDWBasicT(MinionCard):
    def __init__(self):
        super().__init__("Basic T", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         minion_type=MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(100, 120, troop=TROOP_TYPE.T)


class SDWBasicH(MinionCard):
    def __init__(self):
        super().__init__("Basic H", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         minion_type=MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(100, 120, troop=TROOP_TYPE.H)


class SDWBasic01(MinionCard):
    def __init__(self):
        super().__init__("SDWBasic01-engage", 1, CHARACTER_CLASS.ALL, CARD_RARITY.FREE,
                         color=COLOR_TYPE.YELLOW, star=7, nature=NATURE_TYPE.THUNDER,
                         alliance='战神联盟', rank=None, ID='SDWBasic01', boxset='test',
                         minion_type=MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(100, 120, troop=TROOP_TYPE.A,
                      engage=(EngageAttack(Give(BuffOneTurn(ChangeAttack(1000)))),
                              # engage=(EngageAttack(Give(Buff(ChangeAttack(1000)))),
                              EngageAttack(Draw(3), PlayerSelector()),
                              EngageWin(Draw(3), PlayerSelector()),
                              EngageLose(Draw(2), PlayerSelector())),
                      engage_attacker=200, engage_supporter=150, engage_defender=50)


class SDWBasic02(MinionCard):
    def __init__(self):
        super().__init__("SDWBasic02-battrycry", 1, CHARACTER_CLASS.ALL, CARD_RARITY.FREE,
                         color=COLOR_TYPE.YELLOW, star=7, nature=NATURE_TYPE.THUNDER,
                         alliance='战神联盟', rank=None, ID='SDWBasic02', boxset='test',
                         minion_type=MINION_TYPE.BEAST,
                         battlecry=(Battlecry(Give(Buff(ChangeAttack(200))), SelfSelector()),
                                    Battlecry(Draw(4), PlayerSelector()))
                         )

    def create_minion(self, player):
        return Minion(100, 120, troop=TROOP_TYPE.A)
