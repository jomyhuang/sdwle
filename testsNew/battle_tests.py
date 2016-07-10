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


class BattleTests(unittest.TestCase):

    def setUp(self):
        random.seed()

    def test_AutoBattle(self):
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

