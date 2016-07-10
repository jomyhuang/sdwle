import abc
import copy

import random
from SDWLE.cards.base import Card


class Agent(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def do_card_check(self, cards):
        pass

    @abc.abstractmethod
    def do_turn(self, player):
        pass

    @abc.abstractmethod
    def choose_target(self, targets):
        pass

    @abc.abstractmethod
    def choose_index(self, card, player):
        pass

    @abc.abstractmethod
    def choose_option(self, options, player):
        pass

    def filter_options(self, options, player):
        if isinstance(options[0], Card):
            return [option for option in options if option.can_choose(player)]
        return [option for option in options if option.card.can_choose(player)]

    #SDW rule
    def playinfo(self,text):
        print( 'Agent:' + text)

    @abc.abstractmethod
    def choose_support_card(self, player):
        pass

class DoNothingAgent(Agent):
    def __init__(self):
        self.game = None

    def do_card_check(self, cards):
        return [True, True, True, True, True]

    def do_turn(self, player):
        self.playinfo('DoNothingAgent I pass this turn')
        pass

    def choose_target(self, targets):
        return targets[0]

    def choose_index(self, card, player):
        return 0

    def choose_option(self, options, player):
        return self.filter_options(options, player)[0]

    def choose_support_card(self, player):
        return player.hand[0]



class PredictableAgent(Agent):
    def do_card_check(self, cards):
        return [True, True, True, True, True]

    def do_turn(self, player):
        # done_something = True

        attack_minions = [minion for minion in filter(lambda minion: minion.can_attack(), player.minions)]
        attacker = attack_minions[0]
        attacker.attack()

        # 能够使用的就使用 - 英雄、卡、进攻
        # if player.hero.power.can_use():
        #     player.hero.power.use()
        #
        # if player.hero.can_attack():
        #     player.hero.attack()
        # while done_something:
        #     done_something = False
        #     for card in player.hand:
        #         if card.can_use(player, player.game):
        #             player.game.play_card(card)
        #             done_something = True
        #             break
        #
        # for minion in copy.copy(player.minions):
        #     if minion.can_attack():
        #         minion.attack()

    def choose_target(self, targets):
        return targets[0]

    def choose_index(self, card, player):
        return 0

    def choose_option(self, options, player):
        return self.filter_options(options, player)[0]

    def choose_support_card(self, player):
        return player.hand[0]


class RandomAgent(DoNothingAgent):
    def __init__(self):
        super().__init__()

    def do_card_check(self, cards):
        return [True, True, True, True, True]

    def do_turn(self, player):
        attack_minions = [minion for minion in filter(lambda minion: minion.can_attack(), player.minions)]
        # if player.hero.can_attack():
        #     attack_minions.append(player.hero)
        #playable_cards = [card for card in filter(lambda card: card.can_use(player, player.game), player.hand)]
        # if player.hero.power.can_use():
        #     possible_actions = len(attack_minions) + len(playable_cards) + 1
        # else:
        #     possible_actions = len(attack_minions) + len(playable_cards
        attacker = attack_minions[random.randint(0, len(attack_minions)-1)]

        self.playinfo('my turn! I play attacker %s' % attacker)

        if attacker is not None:
            # card = attacker.card
            # if card.is_facedown():
            #     card.use(card.player, player.game)
            #     attacker = card.main_minion
            # # SDW 发动进攻
            attacker.attack()
        else:
            raise ValueError('Random Agent Attacker is None error')


    def choose_target(self, targets):
        return targets[random.randint(0, len(targets) - 1)]

    def choose_index(self, card, player):
        return random.randint(0, len(player.minions))

    def choose_option(self, options, player):
        options = self.filter_options(options, player)
        return options[random.randint(0, len(options) - 1)]

    def choose_support_card(self, player):
        return player.hand[random.randint(0, len(player.hand) - 1)]


