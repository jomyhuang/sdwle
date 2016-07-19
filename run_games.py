import json
import random
from SDWLE.agents.basic_agents import RandomAgent
from SDWLE.cards.heroes import hero_for_class
from SDWLE.constants import CHARACTER_CLASS
from SDWLE.engine import Game, Deck, card_lookup
from SDWLE.cards import *
import timeit


def load_deck(filename):
    cards = []
    character_class = CHARACTER_CLASS.MAGE

    with open(filename, "r") as deck_file:
        contents = deck_file.read()
        items = contents.splitlines()
        for line in items[0:]:
            parts = line.split(" ", 1)
            count = int(parts[0])
            for i in range(0, count):
                card = card_lookup(parts[1])
                if card.character_class != CHARACTER_CLASS.ALL:
                    character_class = card.character_class
                cards.append(card)

    if len(cards) > 30:
        pass

    return Deck(cards, hero_for_class(character_class))

TEST_TIMES = 10000

def do_stuff():
    _count = 0
    game_A_win = 0
    game_B_win = 0
    game_draw =0
    game_error = 0
    game_first_win = 0
    game_second_win = 0
    deck1_name = 'test1-A.hsdeck'
    deck2_name = 'test1.hsdeck'

    def play_game():
        nonlocal _count
        nonlocal game_A_win, game_B_win, game_draw, game_error
        nonlocal game_first_win, game_second_win
        nonlocal deck1_name, deck2_name
        _count += 1
        #TODO copy game func bug!
        # new_game = game.copy()
        deck1 = load_deck(deck1_name)
        deck2 = load_deck(deck2_name)
        game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])

        try:
            # new_game.start()
            game.start()
        except Exception as e:
            game_error += 1
            # print(json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__(), indent=1))
            # print(new_game._all_cards_played)
            raise e

        if game.winner is not None:
            player_id = game.winner.player_id
            if player_id is 0:
                game_A_win += 1
            elif player_id is 1:
                game_B_win += 1

            if game.winner is game.players[0]:
                game_first_win += 1
            else:
                game_second_win += 1
        else:
            game_draw +=1

        # del new_game
        del game
        del deck1, deck2

        if _count % TEST_TIMES == 0:
            print("---- game #{} ----".format(_count))

    random.seed()

    # deck1 = load_deck("test1.hsdeck")
    # deck2 = load_deck("test1.hsdeck")
    # game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])

    # game.start()
    print(timeit.timeit(play_game, 'gc.enable()', number=TEST_TIMES))

    #deck A/B 胜率
    print('deckA: {} / deckB: {}'.format(deck1_name,deck2_name))
    print('A win: {} ({:2.2%})'.format(game_A_win, (game_A_win / TEST_TIMES)))
    print('B win: {} ({:2.2%})'.format(game_B_win, (game_B_win / TEST_TIMES)))
    print('draw : {} ({:2.2%})'.format(game_draw, (game_draw / TEST_TIMES)))
    print('error: {}'.format(game_error))

    # 计算先后手胜率

    print('first hand win : {} ({:2.2%})'.format(game_first_win, (game_first_win / (TEST_TIMES-game_draw))))
    print('second hand win: {} ({:2.2%})'.format(game_second_win, (game_second_win / (TEST_TIMES-game_draw))))

if __name__ == "__main__":
    do_stuff()
