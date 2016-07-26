import copy
import random
from SDWLE.cards.heroes import hero_from_name
from SDWLE.constants import GAMESTATE
from SDWLE.game_objects import Bindable, GameException, Minion, Hero, Weapon
import SDWLE.tags
from SDWLE.tags.base import Effect, AuraUntil
import SDWLE.targeting

card_table = {}


def __create_card_table():
    from SDWLE.cards.base import WeaponCard, SpellCard, MinionCard, SecretCard, ChoiceCard, HeroCard

    def __card_lookup_rec(card_type):
        subclasses = card_type.__subclasses__()
        for sc in subclasses:
            c = sc()
            card_table[c.ref_name] = sc

    for card_class in [WeaponCard, SpellCard, MinionCard, SecretCard, ChoiceCard, HeroCard]:
        __card_lookup_rec(card_class)


def card_lookup(card_name):
    """
    Given a the name of a card as a string, return an object corresponding to that card

    :param str card_name: A string representing the name of the card in English
    :return: An instance of a subclass of Card corresponding to the given card name or None if no Card
             by that name exists.
    :rtype: hearthbreaker.game_objects.Card
    """

    card = card_table[card_name]
    if card is not None:
        return card()
    return None


def get_cards():
    card_list = filter(lambda c: c.collectible,
                       [card() for card in card_table.values()])
    return card_list


class Game(Bindable):
    Session = None

    def __init__(self, decks, agents, random_order=True):
        super().__init__()
        self.delayed_minions = set()
        if random_order:
            self.first_player = self._generate_random_between(0, 1)
            if self.first_player is 0:
                play_order = [0, 1]
            else:
                play_order = [1, 0]
        else:
            play_order = [0, 1]
        # SDW rule
        # player name / 判定胜负的玩家标示 player_id
        play_name = ["deck-A", "deck-B"]
        self.players = [Player(play_name[play_order[0]] + '#one', decks[play_order[0]], agents[play_order[0]], self,
                               player_id=play_order[0]),
                        Player(play_name[play_order[1]] + '#two', decks[play_order[1]], agents[play_order[1]], self,
                               player_id=play_order[1])]
        # self.players = [Player("one", decks[play_order[0]], agents[play_order[0]], self),
        #                 Player("two", decks[play_order[1]], agents[play_order[1]], self)]
        self.current_player = self.players[0]
        self.other_player = self.players[1]
        self.current_player.opponent = self.other_player
        self.other_player.opponent = self.current_player
        self.game_ended = False
        self.minion_counter = 0
        self.__pre_game_run = False
        self.last_card = None
        self._has_turn_ended = True
        self._all_cards_played = []
        self._turns_passed = 0
        self.selected_card = None
        # SDW rule
        Game.Session = self
        self.winner = None
        self.state = GAMESTATE.NONE
        self.next_state = None

    def state_init(self, state):
        self.state = state
        self.state_step()

    def state_step(self):

        if not self.next_state is None:
            self.state = self.next_state
            self.next_state = None

        print('state engine: enter [{}]'.format(GAMESTATE.to_str(self.state)))

        assert isinstance(self.state, object)
        if self.state is GAMESTATE.START:
            print('SDW Game start, have fun!')
            for player in self.players:
                print('player %s %s deck %s' % (player.name, type(player.agent), type(player.deck)))

            self.next_state = GAMESTATE.PRE_GAME
        elif self.state is GAMESTATE.PRE_GAME:
            self.pre_game()
            self.current_player = self.players[1]

            self.next_state = GAMESTATE.TURN
        elif self.state is GAMESTATE.TURN:
            # self.play_single_turn()
            self._start_turn()
            print('engine---player %s start Turn:%d' % (self.current_player.name, self._turns_passed))
            if not self.game_ended:
                self.current_player.agent.do_turn(self.current_player)

            self.next_state = GAMESTATE.NEXT_TURN
            if self.game_ended:
                self.next_state = GAMESTATE.GAME_OVER
        elif self.state is GAMESTATE.NEXT_TURN:
            self._end_turn()
            print('engine---end Turn')

            self.next_state = GAMESTATE.TURN
            if self.game_ended:
                self.next_state = GAMESTATE.GAME_OVER
        elif self.state is GAMESTATE.GAME_OVER:
            if self.winner:
                print('engine: winner is player %s' % self.winner.name)
            else:
                print('engine: game is draw')
        else:
            raise GameException('out of state {}'.format(self.state))

    def random_draw(self, cards, requirement):
        filtered_cards = [card for card in filter(requirement, cards)]
        if len(filtered_cards) > 0:
            return filtered_cards[self._generate_random_between(0, len(filtered_cards) - 1)]
        return None

    def random_choice(self, choice):
        return choice[self._generate_random_between(0, len(choice) - 1)]

    def random_amount(self, minimum, maximum):
        return self._generate_random_between(minimum, maximum)

    def _generate_random_between(self, lowest, highest):
        return random.randint(lowest, highest)

    def check_delayed(self):
        sorted_minions = sorted(self.delayed_minions, key=lambda m: m.born)
        self.delayed_minions = set()
        for minion in sorted_minions:
            minion.activate_delayed()

    def pre_game(self):
        if self.__pre_game_run:
            return
        self.__pre_game_run = True

        # SDW rule 起始手牌5张
        p1_draw = [self.players[0].deck.draw(self) for i in range(5)]
        p2_draw = [self.players[1].deck.draw(self) for i in range(5)]

        # 调度手牌
        card_keep_index = self.players[0].agent.do_card_check(p1_draw)
        self.trigger("kept_cards", p1_draw, card_keep_index)

        put_back_cards = []
        for card_index in range(5):
            if not card_keep_index[card_index]:
                put_back_cards.append(p1_draw[card_index])
                p1_draw[card_index] = self.players[0].deck.draw(self)
        self.players[0].hand = p1_draw
        for card in put_back_cards:
            self.players[0].put_back(card)

        for card in self.players[0].hand:
            card.attach(card, self.players[0])

        card_keep_index = self.players[1].agent.do_card_check(p2_draw)
        self.trigger("kept_cards", p2_draw, card_keep_index)
        put_back_cards = []
        for card_index in range(5):
            if not card_keep_index[card_index]:
                put_back_cards.append(p2_draw[card_index])
                p2_draw[card_index] = self.players[1].deck.draw(self)
        self.players[1].hand = p2_draw
        for card in put_back_cards:
            self.players[1].put_back(card)

        for card in self.players[1].hand:
            card.attach(card, self.players[1])

        # SDW delete
        # coin = card_lookup("The Coin")
        # coin.player = self.players[1]
        # self.players[1].hand.append(coin)

        # SDW rule 部署5张起始牌
        for card_index in range(5):
            card = self.players[0].deck.draw(self)
            card.attach(card, self.players[0])
            self.play_card_facedown(card)
            card = self.players[1].deck.draw(self)
            card.attach(card, self.players[1])
            self.play_card_facedown(card)

    def start(self):
        print('engine: SDW Game start, have fun!')
        for player in self.players:
            print('player %s %s deck %s' % (player.name, type(player.agent), type(player.deck)))

        self.pre_game()
        self.current_player = self.players[1]
        while not self.game_ended:
            self.play_single_turn()

        if self.winner:
            print('engine: winner is player %s' % self.winner.name)
        else:
            print('engine: game is draw')

    def play_single_turn(self):
        self._start_turn()
        print('engine---player %s start Turn:%d' % (self.current_player.name, self._turns_passed))
        if not self.game_ended:
            self.current_player.agent.do_turn(self.current_player)
        self._end_turn()
        print('engine---end Turn')

    def _start_turn(self):
        if not self._has_turn_ended:  # when a game is copied, the turn isn't ended before the next one starts
            self._end_turn()
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
            self.other_player = self.players[0]
        else:
            self.current_player = self.players[0]
            self.other_player = self.players[1]
            # self._turns_passed += 1
        # SDW rule 更换玩家就增加回合数
        self._turns_passed += 1
        # SDW rule TODO 超过一定回合自动结束游戏?
        if self._turns_passed >= 15:
            self.players[0].hero.dead = True
            self.players[1].hero.dead = True
            self.game_over()

        if self.current_player.max_mana < 10:
            self.current_player.max_mana += 1
        # for secret in self.other_player.secrets:
        #     secret.activate(self.other_player)
        for minion in self.current_player.minions:
            if minion:
                minion.attacks_performed = 0
        self.current_player.mana = self.current_player.max_mana - self.current_player.upcoming_overload
        self.current_player.current_overload = self.current_player.upcoming_overload
        self.current_player.upcoming_overload = 0
        self.current_player.cards_played = 0
        self.current_player.dead_this_turn = []
        self.current_player.hero.power.used = False
        self.current_player.hero.attacks_performed = 0
        self.current_player.draw()
        self.current_player.trigger("turn_started", self.current_player)
        self._has_turn_ended = False

    def game_over(self):
        self.game_ended = True

    def _end_turn(self):
        from SDWLE.tags.status import Frozen
        self.current_player.trigger("turn_ended")
        if self.current_player.hero.frozen and \
                        self.current_player.hero.attacks_performed < self.current_player.hero.attacks_allowed():
            self.current_player.hero.frozen = 0
            self.current_player.hero.buffs = \
                [buff for buff in self.current_player.hero.buffs if not isinstance(buff, Frozen)]

        for minion in self.current_player.minions:
            if minion.attacks_performed < minion.attacks_allowed() and minion.frozen:
                minion.frozen = False
                minion.buffs = [buff for buff in minion.buffs if not isinstance(buff, Frozen)]
            minion.exhausted = False
            minion.used_windfury = False
            minion.attacks_performed = 0

        # for aura in copy.copy(self.current_player.object_auras):
        #     if aura.expires:
        #         self.current_player.object_auras.remove(aura)
        #         aura.unapply()
        #
        # for secret in self.other_player.secrets:
        #     secret.deactivate(self.other_player)

        self.check_delayed()
        self._has_turn_ended = True

        # SDW rule 胜负判定与游戏结束
        if self.players[0].minions.is_empty():
            self.winner = self.players[1]
            self.game_over()
        if self.players[1].minions.is_empty():
            self.winner = self.players[0]
            self.game_over()

        # SDW rule 游戏结束但是 winner=None 则为平手
        if self.players[0].minions.is_empty() and self.players[1].minions.is_empty():
            self.winner = None
            self.game_over()

    def copy(self):
        copied_game = copy.copy(self)
        copied_game.events = {}
        copied_game._all_cards_played = []
        copied_game.players = [player.copy(copied_game) for player in self.players]
        if self.current_player is self.players[0]:
            copied_game.current_player = copied_game.players[0]
            copied_game.other_player = copied_game.players[1]
        else:
            copied_game.current_player = copied_game.players[1]
            copied_game.other_player = copied_game.players[0]

        copied_game.current_player.opponent = copied_game.other_player
        copied_game.other_player.opponent = copied_game.current_player
        copied_game._has_turn_ended = self._has_turn_ended

        for player in copied_game.players:
            player.hero.attach(player.hero, player)
            if player.weapon:
                player.weapon.attach(player.hero, player)
            for minion in player.minions:
                minion.attach(minion, player)

        for secret in copied_game.other_player.secrets:
            secret.activate(copied_game.other_player)
        return copied_game

    # SDW rule
    def play_card_facedown(self, card):
        if self.game_ended:
            raise GameException("The game has ended")
        # if not card.can_use(self.current_player, self):
        #    raise GameException("That card cannot be used")
        self._all_cards_played.append(card)
        card.target = None
        card.current_target = None
        self.last_card = card

        # SDW rule
        card.facedown = True

        facedown_minion = card.create_minion_facedown(card.player)
        facedown_minion.linkcard(card, card.player, self)
        facedown_minion.add_to_board()

        # facedown_minion.card = card
        # facedown_minion.player = card.player
        # facedown_minion.game = self
        # index = len(card.player.minions)
        # #fix placeholder 需要?
        # card._placeholder = facedown_minion

        # if card.is_minion():
        # if True:
        #    card._placeholder = Minion(0, 0)
        #    index = len(card.player.minions)+1
        #    #for minion in self.current_player.minions[index:]:
        #    #    minion.index += 1
        #    card.player.minions.append(card._placeholder)
        #    card._placeholder.index = index
        #    card._placeholder.card = card
        #    card._placeholder.player = card.player
        card.player.trigger("card_played_facedown", card, facedown_minion)

        # if not card.cancel:
        #    card.use(self.current_player, self)
        #    card.unattach()
        #    self.current_player.trigger("card_used", card)
        #    self.current_player.cards_played += 1
        #    self.check_delayed()
        # card.current_target = None

    def play_support_card(self, card, target_card):
        if self.game_ended:
            raise GameException("The game has ended")
        if not card.can_use(self.current_player, self):
            raise GameException("That card cannot be used")
        if card.facedown:
            raise GameException("play support card is facedown/error")
        if not card.is_minion():
            raise GameException('support card is not minion card')

        # SDW rule fix card player from Card not/ game.current_player
        # 修正非玩家回合出牌的函数绑定
        card_player = card.player
        # card_index = self.current_player.hand.index(card)
        card_index = card_player.hand.index(card)
        card_player.hand.pop(card_index)

        # self.current_player.mana -= card.mana_cost()
        self._all_cards_played.append(card)
        card.target = target_card
        card.current_target = None
        # if card.targetable and card.targets:
        #     card.target = self.current_player.agent.choose_target(card.targets)

        self.last_card = card
        # if card.is_minion():
        # card._placeholder = Minion(0, 0)
        # index = self.current_player.agent.choose_index(card, self.current_player)
        # for minion in self.current_player.minions[index:]:
        #     minion.index += 1
        # self.current_player.minions.insert(index, card._placeholder)
        # card._placeholder.index = index
        # card._placeholder.card = card
        # card._placeholder.player = self.current_player
        card_player.trigger("support_card_played", card, target_card)

        if not card.cancel:
            card.use(card_player, self, support=True, target_card=target_card)
            card.unattach()
            card_player.trigger("support_card_used", card)
            card_player.cards_played += 1
            self.check_delayed()

        card.current_target = None

        # overload is applied regardless of counterspell, but after the card is played
        self.current_player.upcoming_overload += card.overload

    def play_card(self, card):
        # TODO fix play_card function
        raise GameException('play_card not work yet!')
        if self.game_ended:
            raise GameException("The game has ended")
        if not card.can_use(self.current_player, self):
            raise GameException("That card cannot be used")
        if card.facedown:
            raise GameException("play card is facedown/error")

        card_index = self.current_player.hand.index(card)
        self.current_player.hand.pop(card_index)
        self.current_player.mana -= card.mana_cost()
        self._all_cards_played.append(card)
        card.target = None
        card.current_target = None
        if card.targetable and card.targets:
            card.target = self.current_player.agent.choose_target(card.targets)

        self.last_card = card
        if card.is_minion():
            card._placeholder = Minion(0, 0)
            index = self.current_player.agent.choose_index(card, self.current_player)
            for minion in self.current_player.minions[index:]:
                minion.index += 1
            # TODO 取消insert?
            self.current_player.minions.insert(index, card._placeholder)
            card._placeholder.index = index
            card._placeholder.card = card
            card._placeholder.player = self.current_player
        self.current_player.trigger("card_played", card, card_index)

        if not card.cancel:
            card.use(self.current_player, self)
            card.unattach()
            self.current_player.trigger("card_used", card)
            self.current_player.cards_played += 1
            self.check_delayed()
        card.current_target = None

        # overload is applied regardless of counterspell, but after the card is played
        self.current_player.upcoming_overload += card.overload

    def __to_json__(self):
        if self.current_player == self.players[0]:
            active_player = 1
        else:
            active_player = 2
        return {
            'players': self.players,
            'active_player': active_player,
            'current_sequence_id': self.minion_counter,
            'turn_count': self._turns_passed,
        }

    @staticmethod
    def __from_json__(d, agents):
        new_game = Game.__new__(Game)
        new_game._all_cards_played = []
        new_game.minion_counter = d["current_sequence_id"]
        new_game._turns_passed = d['turn_count']
        new_game.delayed_minions = set()
        new_game.game_ended = False
        new_game.random_func = random.randint
        new_game.events = {}
        new_game.players = [Player.__from_json__(pd, new_game, None) for pd in d["players"]]
        new_game._has_turn_ended = False
        if d["active_player"] == 1:
            new_game.current_player = new_game.players[0]
            new_game.other_player = new_game.players[1]
            new_game.current_player.opponent = new_game.players[1]
            new_game.other_player.opponent = new_game.players[0]
        else:
            new_game.current_player = new_game.players[1]
            new_game.other_player = new_game.players[0]
            new_game.current_player.opponent = new_game.players[0]
            new_game.other_player.opponent = new_game.players[1]

        index = 0
        for player in new_game.players:
            player.agent = agents[index]
            for effect_json in d['players'][index]['effects']:
                player.add_effect(Effect.from_json(**effect_json))
            player.player_auras = []
            for aura_json in d['players'][index]['auras']:
                player.add_aura(AuraUntil.from_json(**aura_json))
            player.hero.attach(player.hero, player)
            if player.weapon:
                player.weapon.attach(player.weapon, player)

            for minion in player.minions:
                minion.attach(minion, player)
                if minion.health != minion.calculate_max_health():
                    minion.enraged = True
            index += 1
        return new_game


# SDW rule
class BattleField(list):
    MAX_FIELDS = 5

    # TODO
    # minions 保留建立在场的list, 另外建立battle field的index

    def __init__(self):
        self.ready = False

    def append(self, p_object):
        if len(self) >= BattleField.MAX_FIELDS:
            raise GameException("battlefield can't append")
        super().append(p_object)

    def insert(self, index, p_object):
        if len(self) >= BattleField.MAX_FIELDS:
            raise GameException("battlefield can't insert")
        super().insert(index, p_object)

    def is_empty(self):
        return len(self) <= 0


class Player(Bindable):
    def __init__(self, name, deck, agent, game, player_id=None):
        super().__init__()
        self.game = game
        self.hero = deck.hero.create_hero(self)
        self.hero.card = deck.hero
        self.name = name
        self.deck = deck
        self.hand = []
        self.agent = agent
        self.opponent = None
        # TODO check usages
        self.cards_played = 0
        # SDW rule
        # player_id 用于标示实际玩家标示
        self.player_id = player_id
        self.minions = BattleField()
        self.combat_win_times = 0
        self.combat_lose_times = 0
        self.combat_draw_times = 0
        self.combat_minion = None
        self.support_minion = None
        # 回收基地区
        self.graveyard = []
        self.base_this_turn = []
        # 黑洞区
        self.graveyard_blackhole = []
        self.dead_this_turn = []

        # hearthbreaker attribute
        self.spell_damage = 0
        self.mana = 0
        self.max_mana = 0
        self.object_auras = []
        self.player_auras = []
        self.fatigue = 0
        self.effects = []
        self.secrets = []
        self.weapon = None
        self.spell_multiplier = 1
        self.heal_multiplier = 1
        self.heal_does_damage = 0
        self.double_deathrattle = 0
        self.mana_filters = []
        self.upcoming_overload = 0
        self.current_overload = 0

    def __str__(self):  # pragma: no cover
        return "Player: " + self.name

    # SDW rule
    def _remove_combat_tag(self):
        self.combat_minion = None
        self.support_minion = None

    def copy(self, new_game):
        copied_player = Player(self.name, self.deck.copy(), self.agent, new_game)

        copied_player.hero = self.hero.copy(copied_player)
        copied_player.graveyard = copy.copy(self.graveyard)
        copied_player.minions = [minion.copy(copied_player, new_game) for minion in self.minions]
        copied_player.hand = [copy.copy(card) for card in self.hand]
        for card in copied_player.hand:
            card._attached = False
            card.attach(card, copied_player)
        copied_player.spell_damage = self.spell_damage
        copied_player.mana = self.mana
        copied_player.max_mana = self.max_mana
        copied_player.upcoming_overload = self.upcoming_overload
        copied_player.current_overload = self.current_overload
        copied_player.dead_this_turn = copy.copy(self.dead_this_turn)
        if self.weapon:
            copied_player.weapon = self.weapon.copy(copied_player)
        for effect in self.effects:
            effect = copy.copy(effect)
            copied_player.add_effect(effect)
        copied_player.secrets = []
        for secret in self.secrets:
            new_secret = type(secret)()
            new_secret.player = copied_player
            copied_player.secrets.append(new_secret)
        for aura in filter(lambda a: isinstance(a, AuraUntil), self.player_auras):
            aura = copy.deepcopy(aura)
            aura.owner = copied_player.hero
            copied_player.add_aura(aura)
        for aura in filter(lambda a: isinstance(a, AuraUntil), self.object_auras):
            aura = copy.deepcopy(aura)
            aura.owner = copied_player.hero
            copied_player.add_aura(aura)
        copied_player.effect_count = dict()
        return copied_player

    def draw(self):
        if self.can_draw():
            card = self.deck.draw(self.game)
            self.game.selected_card = card
            if len(self.hand) < 15:
                self.hand.append(card)
                card.attach(card, self)
                self.trigger("card_drawn", card)
                card.trigger("drawn")
            else:
                self.trigger("card_destroyed", card)
                raise GameException('draw: over 15 cards in hand')
        else:
            self.fatigue += 1
            self.hero.trigger("fatigue_damage", self.fatigue)
            self.hero.damage(self.fatigue, None)
            self.hero.activate_delayed()
            raise GameException('draw: out of deck')

    def can_draw(self):
        return self.deck.can_draw()

    def effective_spell_damage(self, base_damage):
        return (base_damage + self.spell_damage) * self.spell_multiplier

    def effective_heal_power(self, base_heal):
        if self.heal_does_damage:
            return -(base_heal + self.spell_damage) * self.spell_multiplier
        else:
            return base_heal * self.heal_multiplier

    def put_back(self, card):
        card.unattach()
        self.deck.put_back(card)
        self.trigger("card_put_back", card)

    def discard(self):
        if len(self.hand) > 0:
            targets = self.hand
            target = self.game.random_choice(targets)
            self.hand.remove(target)
            target.unattach()
            self.game.selected_card = target
            self.trigger("card_discarded", target)

    def add_effect(self, effect):
        def remove_effect(*args):
            effect.unapply()
            self.effects.remove(effect)
            effect.event.unbind(self.hero, remove_effect)

        self.effects.append(effect)
        effect.set_owner(self.hero)
        effect.apply()
        effect.event.bind(self.hero, remove_effect)

    def add_aura(self, aura):
        if isinstance(aura.selector, SDWLE.tags.selector.PlayerSelector):
            self.player_auras.append(aura)
        else:
            self.object_auras.append(aura)
        if not aura.owner:
            aura.set_owner(self.hero)
        aura.apply()

    def remove_aura(self, aura):
        if isinstance(aura.selector, SDWLE.tags.selector.PlayerSelector):
            self.player_auras = [au for au in filter(lambda a: a is not aura, self.player_auras)]
        else:
            for an_aura in self.object_auras:
                if an_aura.eq(aura):
                    self.object_auras.remove(an_aura)
                    aura = an_aura
                    break
        aura.unapply()

    def choose_target(self, targets):
        return self.agent.choose_target(targets)

    # SDW rule
    def playinfo(self, text):
        return self.agent.playinfo(text)

    def choose_support_card(self, targets):
        return self.agent.choose_support_card(targets)

    def is_valid(self):
        return True

    def is_player(self):
        return True

    def __to_json__(self):
        auras = copy.copy(self.player_auras)
        auras.extend(self.object_auras)
        return {
            'hero': self.hero,
            'deck': self.deck,
            'graveyard': self.graveyard,
            'hand': self.hand,
            'secrets': [secret.name for secret in self.secrets],
            'weapon': self.weapon,
            'effects': self.effects,
            'auras': [aura for aura in filter(lambda a: isinstance(a, AuraUntil), auras)],
            'minions': self.minions,
            'mana': self.mana,
            'max_mana': self.max_mana,
            'current_overload': self.current_overload,
            'upcoming_overload': self.upcoming_overload,
            'name': self.name,
        }

    @classmethod
    def __from_json__(cls, pd, game, agent):
        deck = Deck.__from__to_json__(pd["deck"],
                                      hero_from_name(pd["hero"]["name"]))
        player = Player("whatever", deck, agent, game)
        hero = Hero.__from_json__(pd["hero"], player)
        player.hero = hero
        hero.player = player
        if pd['weapon']:
            player.weapon = Weapon.__from_json__(pd['weapon'], player)
            player.weapon.player = player
        player.mana = pd["mana"]
        player.max_mana = pd["max_mana"]
        player.upcoming_overload = pd['upcoming_overload']
        player.current_overload = pd['current_overload']
        player.name = pd['name']
        player.hand = []
        for card_def in pd['hand']:
            card = card_lookup(card_def['name'])
            card.__from_json__(card, **card_def)
            card.attach(card, player)
            player.hand.append(card)
        player.graveyard = pd["graveyard"]

        player.secrets = []
        for secret_name in pd["secrets"]:
            secret = card_lookup(secret_name)
            secret.player = player
            player.secrets.append(secret)
        i = 0
        player.minions = []
        for md in pd["minions"]:
            minion = Minion.__from_json__(md, player, game)
            minion.index = i
            player.minions.append(minion)
            i += 1
        return player


class Deck:
    def __init__(self, cards, hero):
        # SDW rule TODO deck numbers
        if len(cards) != 30:
            raise GameException("Deck must have exactly 30 cards in it")
        self.cards = cards
        self.hero = hero
        for card in cards:
            card.drawn = False
        self.left = 30

    def copy(self):
        def copy_card(card):
            new_card = type(card)()
            new_card.drawn = card.drawn
            return new_card

        new_deck = Deck.__new__(Deck)
        new_deck.cards = [copy_card(card) for card in self.cards]
        new_deck.hero = self.hero
        new_deck.left = self.left
        return new_deck

    def can_draw(self):
        return self.left > 0

    def draw(self, game):
        if not self.can_draw():
            raise GameException("Cannot draw more than 30 cards")
        card = game.random_draw(self.cards, lambda c: not c.drawn)
        card.drawn = True
        self.left -= 1
        return card

    def put_back(self, card):
        if not card:
            raise TypeError("Expected a card, not None")
        for deck_card in self.cards:
            if deck_card == card:
                if not card.drawn:
                    raise GameException("Tried to put back a card that hadn't been used yet")
                deck_card.drawn = False
                self.left += 1
                return
        card.drawn = False
        self.cards.append(card)
        self.left += 1

    def __to_json__(self):
        card_list = []
        for card in self.cards:
            card_list.append({
                'name': card.name,
                'used': card.drawn
            })
        return card_list

    @classmethod
    def __from__to_json__(cls, dd, hero):
        cards = []
        used = []
        left = 30
        for entry in dd:
            card = card_lookup(entry["name"])
            card.drawn = entry["used"]
            cards.append(card)
            used.append(entry["used"])
            if entry["used"]:
                left -= 1
        deck = Deck.__new__(Deck)
        deck.cards = cards
        deck.used = used
        deck.left = left
        deck.hero = hero
        return deck


__create_card_table()
