import random
import unittest
from SDWLE.agents.basic_agents import RandomAgent, PredictableAgent
from SDWLE.cards import MogushanWarden, StonetuskBoar, GoldshireFootman, MurlocRaider, BloodfenRaptor, FrostwolfGrunt, RiverCrocolisk, \
    IronfurGrizzly, MagmaRager, SilverbackPatriarch, ChillwindYeti, SenjinShieldmasta, BootyBayBodyguard, \
    FenCreeper, BoulderfistOgre, WarGolem, Shieldbearer, FlameImp, YoungPriestess, DarkIronDwarf, DireWolfAlpha, \
    Voidwalker, HarvestGolem, KnifeJuggler, ShatteredSunCleric, ArgentSquire, Doomguard, Soulfire, DefenderOfArgus, \
    AbusiveSergeant, NerubianEgg, KeeperOfTheGrove
from SDWLE.cards.heroes import Jaina, Guldan, Malfurion
from SDWLE.engine import Game, Deck
from testsSDW.testing_utils import generate_game_for, StackedDeck, mock


class BattleTests(unittest.TestCase):

    def setUp(self):
        random.seed()

    def test_AutoGame(self):
        # deck1 = Deck([
        #     FrostwolfGrunt(),
        #     FrostwolfGrunt(),
        #     FrostwolfGrunt(),
        #     FrostwolfGrunt(),
        #     FrostwolfGrunt(),
        #     FrostwolfGrunt(),
        #     FrostwolfGrunt(),
        #     FrostwolfGrunt(),
        #     FrostwolfGrunt(),
        #     FrostwolfGrunt(),
        #     MurlocRaider(),
        #     MurlocRaider(),
        #     MurlocRaider(),
        #     MurlocRaider(),
        #     MurlocRaider(),
        #     MurlocRaider(),
        #     MurlocRaider(),
        #     MurlocRaider(),
        #     MurlocRaider(),
        #     MurlocRaider(),
        #     BloodfenRaptor(),
        #     BloodfenRaptor(),
        #     BloodfenRaptor(),
        #     BloodfenRaptor(),
        #     BloodfenRaptor(),
        #     BloodfenRaptor(),
        #     BloodfenRaptor(),
        #     BloodfenRaptor(),
        #     BloodfenRaptor(),
        #     BloodfenRaptor()
        # ], Jaina())
        #
        # deck2 = Deck([
        #     Shieldbearer(),
        #     Shieldbearer(),
        #     Shieldbearer(),
        #     Shieldbearer(),
        #     Shieldbearer(),
        #     Shieldbearer(),
        #     Shieldbearer(),
        #     Shieldbearer(),
        #     Shieldbearer(),
        #     Shieldbearer(),
        #     MogushanWarden(),
        #     MogushanWarden(),
        #     MogushanWarden(),
        #     MogushanWarden(),
        #     MogushanWarden(),
        #     MogushanWarden(),
        #     MogushanWarden(),
        #     MogushanWarden(),
        #     MogushanWarden(),
        #     MogushanWarden(),
        #     WarGolem(),
        #     WarGolem(),
        #     WarGolem(),
        #     WarGolem(),
        #     WarGolem(),
        #     WarGolem(),
        #     WarGolem(),
        #     WarGolem(),
        #     WarGolem(),
        #     WarGolem()
        # ], Guldan())

        game = generate_game_for([FrostwolfGrunt, MurlocRaider, BloodfenRaptor],
                                 [Shieldbearer, MogushanWarden, WarGolem],
                                 RandomAgent, PredictableAgent, random_order=True,
                                 deck_func1=StackedDeck)

        # game = Game([deck1, deck2], [RandomAgent(), PredictableAgent()])

        print('test auto battle ------------')
        game.start()

        self.assertTrue(game.game_ended)

        print('end test auto battle ---------')


    def test_SingleBattle(self):
        game = generate_game_for([Shieldbearer, StonetuskBoar, BloodfenRaptor],
                                 [MogushanWarden, WarGolem, FrostwolfGrunt],
                                 PredictableAgent, PredictableAgent)

        # test hand, minions face-down
        self.assertIsInstance(game.players[0].minions[0].card, StonetuskBoar)
        self.assertTrue(game.players[0].minions[0].card.is_facedown())
        self.assertIsInstance(game.players[0].hand[0], Shieldbearer)
        self.assertIsInstance(game.players[1].minions[0].card, WarGolem)
        self.assertTrue(game.players[1].minions[0].card.is_facedown())
        self.assertIsInstance(game.players[1].hand[0], MogushanWarden)

        game.play_single_turn()

        self.assertEqual(len(game.players[0].graveyard), 0)
        self.assertEqual(len(game.players[0].graveyard_blackhole), 2)
        self.assertEqual(len(game.players[1].graveyard), 1)
        self.assertEqual(len(game.players[1].graveyard_blackhole), 0)
        self.assertIsInstance(game.players[1].minions[0].card, MogushanWarden)
        self.assertEqual(game.players[1].graveyard[0], WarGolem().name)

        # test combat tag
        minion = game.players[0].combat_minion
        support = game.players[0].support_minion

        self.assertIsInstance(minion.card, StonetuskBoar)
        self.assertIsInstance(support.card, Shieldbearer)
        self.assertEqual(minion.combat_power, 1 + 0)

        self.assertTrue(minion.attacker)
        self.assertFalse(minion.defender)
        self.assertFalse(minion.supporter)

        self.assertTrue(support.supporter)
        self.assertFalse(support.attacker)
        self.assertFalse(support.defender)

        minion = game.players[1].combat_minion
        support = game.players[1].support_minion

        self.assertIsInstance(minion.card, WarGolem)
        self.assertIsInstance(support.card, MogushanWarden)
        self.assertEqual(minion.combat_power, 7 + 1)

        self.assertFalse(minion.attacker)
        self.assertTrue(minion.defender)
        self.assertFalse(minion.supporter)

        self.assertTrue(support.supporter)
        self.assertFalse(support.attacker)
        self.assertFalse(support.defender)


        game.play_single_turn()

        self.assertEqual(len(game.players[0].graveyard), 0)
        self.assertEqual(len(game.players[0].graveyard_blackhole), 4)
        self.assertEqual(len(game.players[1].graveyard), 2)
        self.assertEqual(len(game.players[1].graveyard_blackhole), 0)
        self.assertIsInstance(game.players[1].minions[0].card, MogushanWarden)
        self.assertEqual(game.players[1].graveyard[1], MogushanWarden().name)

        # test combat tag 2
        minion = game.players[0].combat_minion
        support = game.players[0].support_minion

        self.assertIsInstance(minion.card, StonetuskBoar)
        self.assertIsInstance(support.card, Shieldbearer)
        self.assertEqual(minion.combat_power, 1 + 0)

        self.assertFalse(minion.attacker)
        self.assertTrue(minion.defender)
        self.assertFalse(minion.supporter)

        self.assertTrue(support.supporter)
        self.assertFalse(support.attacker)
        self.assertFalse(support.defender)

        minion = game.players[1].combat_minion
        support = game.players[1].support_minion

        self.assertIsInstance(minion.card, MogushanWarden)
        self.assertIsInstance(support.card, MogushanWarden)
        self.assertEqual(minion.combat_power, 1 + 1)

        self.assertTrue(minion.attacker)
        self.assertFalse(minion.defender)
        self.assertFalse(minion.supporter)

        self.assertTrue(support.supporter)
        self.assertFalse(support.attacker)
        self.assertFalse(support.defender)


        self.assertEqual(game.players[0].combat_win_times, 0)
        self.assertEqual(game.players[0].combat_lose_times, 2)
        self.assertEqual(game.players[0].combat_draw_times, 0)

        self.assertEqual(game.players[1].combat_win_times, 2)
        self.assertEqual(game.players[1].combat_lose_times, 0)
        self.assertEqual(game.players[1].combat_draw_times, 0)


