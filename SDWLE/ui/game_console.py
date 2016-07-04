from hearthbreaker.constants import CHARACTER_CLASS

card_abbreviations = {
    'Mark of the Wild': 'Mrk Wild',
    'Power of the Wild': 'Pow Wild',
    'Wild Growth': 'Wld Grth',
    'Healing Touch': 'Hlng Tch',
    'Mark of Nature': 'Mrk Ntr',
    'Savage Roar': 'Svg Roar',
    'Soul of the Forest': 'Sol Frst',
    'Force of Nature': 'Frce Nat',
    'Keeper of the Grove': 'Kpr Grve',
    'Druid of the Claw': 'Drd Claw',
    'Stonetusk Boar': 'Stntsk Br',
    'Raging Worgen': 'Rgng Wrgn',
}


def abbreviate(card_name):
    return card_abbreviations.get(card_name, card_name)


def game_to_string(game):
    pass

def console(y=0, x=0, info='dummy', color=0):
    print(info)


class ConsoleGameRender:
    def __init__(self, window, game, viewing_player):
        if viewing_player is game.players[0]:
            self.top_player = game.players[1]
            self.bottom_player = game.players[0]
        else:
            self.top_player = game.players[0]
            self.bottom_player = game.players[1]

        # curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        # curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
        # curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        # curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)

        # self.top_minion_window = window.derwin(3, 80, 4, 0)
        # self.bottom_minion_window = window.derwin(3, 80, 8, 0)
        # self.card_window = window.derwin(5, 80, 16, 0)
        # self.card_window = window.derwin(5, 80, 16, 0)
        self.top_minion_window = None
        self.bottom_minion_window = None
        self.card_window = None
        self.card_window = None
        self.window = window
        self.game = game
        self.targets = None
        self.selected_target = None
        self.selection_index = -1

    def draw_minion(self, minion, window, y, x, main=True):
        status_array = []
        color = 0
        if minion.can_attack():
            status_array.append("*")
            if not self.targets:
                 color = 2
        else:
            if not self.targets:
                color = 1
        if "attack" in minion.events:
            status_array.append("a")
        if "turn_start" in minion.events:
            status_array.append("b")
        if minion.charge:
            status_array.append("c")
        if minion.deathrattle is not None:
            status_array.append("d")
        if minion.enraged:
            status_array.append("e")
        if minion.frozen:
            status_array.append("f")
        if minion.immune:
            status_array.append("i")
        if minion.stealth:
            status_array.append("s")
        if minion.taunt:
            status_array.append("t")
        if minion.exhausted and not minion.charge:
            status_array.append("z")

        # if self.targets:
        #     if minion is self.selected_target:
        #         color = curses.color_pair(4)
        #     elif minion in self.targets:
        #         color = curses.color_pair(3)

        spaces = ''
        if not main:
            spaces = ' ' * 30

        name = abbreviate(minion.card.name)[:9]
        status = ''.join(status_array)
        power_line = "({0}) ({1})".format(minion.calculate_attack(), minion.health)

        if minion.card.is_facedown():
            name = 'facedown'
            #status = 'facedown'

        console(y, x, "{0}{1}:{2:^9} {3:^9} {4:^9}".format(spaces, minion.index, name, power_line, status), color)
        #console(y+1, x,"{0:^9}".format(power_line), color)
        #console(y+2, x, "{0:^9}".format(status), color)
        # window.addstr(y + 2, x, "{0}".format(minion.index), color)

    def draw_card(self, card, player, window, y, x):
        color = 0
        if card.can_use(player, player.game):
            status = "*"
            if not self.targets:
                color = 2
        else:
            status = " "
            if not self.targets:
                color = 1
        if self.targets:
            if card is self.selected_target:
                color = 4
            elif card in self.targets:
                color = 3

        name = card.name[:15]

        console(y + 0, x, "{0:>2} mana ({1}) {2:^15}   ".format(card.mana_cost(), status, name), color)
        # console(y + 1, x, "{0:^15}".format(name), color)

    def draw_hero(self, player, window, x, y):
        # color = curses.color_pair(0)
        # if self.targets:
        #     if player.hero is self.selected_target:
        #         color = curses.color_pair(4)
        #     elif player.hero in self.targets:
        #         color = curses.color_pair(3)
        # if player.weapon is not None:
        #     weapon_power = "({0}) ({1})".format(player.weapon.base_attack, player.weapon.durability)
        #     window.addstr(y, x, "{0:^20}".format(player.weapon.card.name))
        #     window.addstr(y + 1, x, "{0:^20}".format(weapon_power))
        #
        # hero_power = "({0}) ({1}+{4}) -- {2}/{3}".format(player.hero.calculate_attack(), player.hero.health,
        #                                                  player.mana, player.max_mana, player.hero.armor)
        # window.addstr(y, x + 20, "{0:^20}".format(CHARACTER_CLASS.to_str(player.hero.character_class)), color)
        # window.addstr(y + 1, x + 20, "{0:^20}".format(hero_power), color)
        #
        # window.addstr(y, x + 40, "{0:^20}".format("Hero Power"))
        # if player.hero.power.can_use():
        #     window.addstr(y + 1, x + 40, "{0:^20}".format("*"))
        pass

    def draw_game(self):
        console(0,0,'UI-draw_game')

        # self.window.clear()
        # self.bottom_minion_window.clear()
        # self.top_minion_window.clear()
        # self.card_window.clear()

        def draw_minions(minions, window, main):
            l_offset = int((80 - 10 * len(minions)) / 2)
            index = 0
            for minion in minions:
                # if main and index == self.selection_index:
                #     window.addstr(2, l_offset + index * 10 - 1, "^")
                self.draw_minion(minion, window, 0, l_offset + index * 10, main)
                index += 1
            # if main and len(minions) == self.selection_index:
            #     window.addstr(2, l_offset + index * 10 - 1, "^")

        def draw_cards(cards, player, window, y):
            l_offset = int((80 - 16 * len(cards)) / 2)
            index = 0
            for card in cards:
                self.draw_card(card, player, window, y, l_offset + index * 16)
                index += 1

        draw_minions(self.top_player.minions, self.top_minion_window, False)
        draw_minions(self.bottom_player.minions, self.bottom_minion_window, True)

        draw_cards(self.bottom_player.hand, self.bottom_player, self.card_window, 0)
        # draw_cards(self.bottom_player.hand[:5], self.bottom_player, self.card_window, 0)
        # draw_cards(self.bottom_player.hand[5:], self.bottom_player, self.card_window, 3)

        # self.draw_hero(self.top_player, self.window, 10, 0)
        # self.draw_hero(self.bottom_player, self.window, 10, 12)
        # self.window.refresh()
        # self.bottom_minion_window.refresh()
        # self.top_minion_window.refresh()
        # self.card_window.refresh()
