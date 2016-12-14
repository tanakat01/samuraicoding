# -*- coding: utf-8 -*-
"""
Random Player for Samurai Coding 2016.

Example:
    To run this program as follows:

        $ python random_player.py
"""

import sys
import random
import game


def main():
    """
    Main routine of random player
    """
    my_team = int(input())
    print(0)
    while True:
        state = game.State.read_turn(my_team)
#        print(state, file=sys.stderr)
        moves = state.make_moves()
#        print('moves = %s' % moves, file=sys.stderr)
        move = moves[random.randrange(len(moves))]
        print(' '.join(str(x) for x in move))


if __name__ == '__main__':
    main()
