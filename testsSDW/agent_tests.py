import random
import unittest
from SDWLE.agents.basic_agents import RandomAgent
from SDWLE.cards import MogushanWarden, StonetuskBoar, GoldshireFootman, MurlocRaider, BloodfenRaptor, FrostwolfGrunt, RiverCrocolisk, \
    IronfurGrizzly, MagmaRager, SilverbackPatriarch, ChillwindYeti, SenjinShieldmasta, BootyBayBodyguard, \
    FenCreeper, BoulderfistOgre, WarGolem, Shieldbearer, FlameImp, YoungPriestess, DarkIronDwarf, DireWolfAlpha, \
    Voidwalker, HarvestGolem, KnifeJuggler, ShatteredSunCleric, ArgentSquire, Doomguard, Soulfire, DefenderOfArgus, \
    AbusiveSergeant, NerubianEgg, KeeperOfTheGrove
from SDWLE.cards.heroes import Jaina, Guldan, Malfurion
from SDWLE.engine import Game, Deck


class TestAgents(unittest.TestCase):

    def setUp(self):
        # random.seed(1857)
        pass

    def test_RandomAgent(self):
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


        game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])
        game.pre_game()
        game.current_player = game.players[1]

        game.play_single_turn()

        # self.assertEqual(5, len(game.current_player.minions))

        # game.play_single_turn()
        # self.assertEqual(4, len(game.current_player.minions))
        # # self.assertEqual(3, game.current_player.minions[1].health)
        # self.assertEqual("Young Priestess", game.current_player.minions[0].card.name)
        #
        # game.play_single_turn()
        # self.assertEqual(1, len(game.current_player.minions))
        # self.assertEqual("Frostwolf Grunt", game.current_player.minions[0].card.name)
        #
        # game.play_single_turn()
        # self.assertEqual(0, len(game.other_player.minions))
        # self.assertEqual(28, game.other_player.hero.health)
        # self.assertEqual(3, len(game.current_player.minions))
        # self.assertEqual("Dire Wolf Alpha", game.current_player.minions[2].card.name)

        count = 0
        while not game.game_ended and count < 15:
            game.play_single_turn()
            count += 1

        # self.assertEqual(0, game.current_player.hero.health)
        # self.assertEqual(21, game.other_player.hero.health)

        self.assertTrue(game.game_ended)
