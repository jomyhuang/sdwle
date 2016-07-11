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
        deck1 = Deck([
            FrostwolfGrunt(),
            FrostwolfGrunt(),
            FrostwolfGrunt(),
            FrostwolfGrunt(),
            FrostwolfGrunt(),
            FrostwolfGrunt(),
            FrostwolfGrunt(),
            FrostwolfGrunt(),
            FrostwolfGrunt(),
            FrostwolfGrunt(),
            MurlocRaider(),
            MurlocRaider(),
            MurlocRaider(),
            MurlocRaider(),
            MurlocRaider(),
            MurlocRaider(),
            MurlocRaider(),
            MurlocRaider(),
            MurlocRaider(),
            MurlocRaider(),
            BloodfenRaptor(),
            BloodfenRaptor(),
            BloodfenRaptor(),
            BloodfenRaptor(),
            BloodfenRaptor(),
            BloodfenRaptor(),
            BloodfenRaptor(),
            BloodfenRaptor(),
            BloodfenRaptor(),
            BloodfenRaptor()
        ], Jaina())

        deck2 = Deck([
            Shieldbearer(),
            Shieldbearer(),
            Shieldbearer(),
            Shieldbearer(),
            Shieldbearer(),
            Shieldbearer(),
            Shieldbearer(),
            Shieldbearer(),
            Shieldbearer(),
            Shieldbearer(),
            MogushanWarden(),
            MogushanWarden(),
            MogushanWarden(),
            MogushanWarden(),
            MogushanWarden(),
            MogushanWarden(),
            MogushanWarden(),
            MogushanWarden(),
            MogushanWarden(),
            MogushanWarden(),
            WarGolem(),
            WarGolem(),
            WarGolem(),
            WarGolem(),
            WarGolem(),
            WarGolem(),
            WarGolem(),
            WarGolem(),
            WarGolem(),
            WarGolem()
        ], Guldan())

        game = Game([deck1, deck2], [RandomAgent(), PredictableAgent()])

        print('test auto battle ------------')
        game.start()

        self.assertTrue(game.game_ended)

        print('end test auto battle ---------')


    def test_SingleBattle(self):
        game = generate_game_for([Shieldbearer, StonetuskBoar, BloodfenRaptor],[MogushanWarden, WarGolem, FrostwolfGrunt], PredictableAgent, PredictableAgent)

        for turn in range(8):
            game.play_single_turn()

        # The mana should not go over 10 on turn 9 (or any other turn)
        self.assertEqual(10, game.current_player.mana)