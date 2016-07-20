import random
import unittest
from SDWLE.agents.basic_agents import RandomAgent, PredictableAgent
# from SDWLE.cards import MogushanWarden, StonetuskBoar, MurlocRaider, BloodfenRaptor, FrostwolfGrunt, \
#     GoldshireFootman, IronfurGrizzly, MagmaRager, SilverbackPatriarch, ChillwindYeti, SenjinShieldmasta, BootyBayBodyguard, \
#     FenCreeper, BoulderfistOgre, WarGolem, Shieldbearer, FlameImp, YoungPriestess, DarkIronDwarf, DireWolfAlpha, \
#     Voidwalker, HarvestGolem, KnifeJuggler, ShatteredSunCleric, ArgentSquire, Doomguard, Soulfire, DefenderOfArgus, \
#     AbusiveSergeant, NerubianEgg, KeeperOfTheGrove, RiverCrocolisk
# from SDWLE.cards.heroes import Jaina, Guldan, Malfurion
from SDWLE.engine import Game, Deck
from testsSDW.testing_utils import generate_game_for, StackedDeck, Stacked5Deck
from SDWLE.cards import SDW01, SDW02, SDW03, SDW04, SDWBasicA, SDWBasicH, SDWBasicT, SDWBasic01
from SDWLE.constants import CARD_RARITY, CHARACTER_CLASS, MINION_TYPE, TROOP_TYPE, COLOR_TYPE, NATURE_TYPE

class BasicCardTest(unittest.TestCase):

    def setUp(self):
        random.seed()
        self.deckA_attack = None
        self.deckA_support = None
        self.deckA_draw = None
        self.deckB_attack = None
        self.deckB_support = None
        self.deckB_draw = None
        self.game = None

    def tearDown(self):
        pass

    def singleCard_game_init(self, deckA_attack, deckA_support, deckA_draw,
                             deckB_attack, deckB_support, deckB_draw):

        self.deckA_attack = deckA_attack
        self.deckA_support = deckA_support
        self.deckA_draw = deckA_draw
        self.deckB_attack = deckB_attack
        self.deckB_support = deckB_support
        self.deckB_draw = deckB_draw

        game = generate_game_for([self.deckA_support, self.deckA_attack, self.deckA_draw],
                                 [self.deckB_support, self.deckB_attack, self.deckB_draw],
                                 PredictableAgent, PredictableAgent,
                                 run_pre_game=True, random_order=False,
                                 deck_func1=Stacked5Deck, deck_func2=Stacked5Deck)

        # test hand, minions face-down
        self.assertIsInstance(game.players[0].minions[0].card, self.deckA_attack)
        self.assertTrue(game.players[0].minions[0].card.is_facedown())
        self.assertIsInstance(game.players[0].hand[0], self.deckA_support)
        self.assertIsInstance(game.players[1].minions[0].card, self.deckB_attack)
        self.assertTrue(game.players[1].minions[0].card.is_facedown())
        self.assertIsInstance(game.players[1].hand[0], self.deckB_support)

        self.game = game

        return game

    def singleCard_combat_test(self, turns=1):

        game = self.game
        self.assertEqual(len(game.players[0].graveyard), 1)
        self.assertEqual(len(game.players[0].graveyard_blackhole), 0)
        self.assertEqual(game.players[0].graveyard[0], self.deckA_attack().name)
        self.assertIsInstance(game.players[0].minions[0].card, self.deckA_support)

        self.assertEqual(len(game.players[1].graveyard), 0)
        self.assertEqual(len(game.players[1].graveyard_blackhole), 2)
        self.assertEqual(game.players[1].graveyard_blackhole[0], self.deckB_attack().name)
        self.assertEqual(game.players[1].graveyard_blackhole[1], self.deckB_support().name)

        self.assertEqual(game.players[0].combat_win_times, turns)
        self.assertEqual(game.players[0].combat_lose_times, 0)
        self.assertEqual(game.players[0].combat_draw_times, 0)

        self.assertEqual(game.players[1].combat_win_times, 0)
        self.assertEqual(game.players[1].combat_lose_times, turns)
        self.assertEqual(game.players[1].combat_draw_times, 0)

        return game


    def test_basic_tool(self):

        deckA_attack = SDW04
        deckA_support = SDW03
        deckA_draw = SDW03
        # mock card
        deckB_attack = SDWBasicA
        deckB_support = SDWBasicA
        deckB_draw = SDWBasicA

        game = self.singleCard_game_init( deckA_attack, deckA_support, deckA_draw,
                                          deckB_attack, deckB_support, deckB_draw )

        game.play_single_turn()

        #always deck A win
        self.singleCard_combat_test(1)

        game.play_single_turn()
        # self.singleCard_combat_test(2)

    def test_effect_engage(self):

        deckA_attack = SDWBasic01
        deckA_support = SDWBasic01
        deckA_draw = SDW03
        # mock card
        deckB_attack = SDWBasic01
        deckB_support = SDWBasicA
        deckB_draw = SDWBasicA

        game = self.singleCard_game_init( deckA_attack, deckA_support, deckA_draw,
                                          deckB_attack, deckB_support, deckB_draw )

        game.play_single_turn()

        #always deck A win
        self.singleCard_combat_test(1)

        attacker = game.players[0].combat_minion
        defender = game.players[1].combat_minion

        # self.assertEqual(attacker.calculate_attack(), 300)

        self.assertEqual(attacker.combat_power, 550)
        self.assertEqual(defender.combat_power, 250)


        # game.play_single_turn()
        # self.singleCard_combat_test(2)
