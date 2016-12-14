"""
The Game module for Samurai coding 2016
"""

from __future__ import division
from __future__ import print_function
import copy
W, H = 15, 15


class P(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return P(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __str__(self):
        return 'P(%s, %s)' % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __copy__(self):
        return P(self.x, self.y)

    def rotate(self, d):
        x, y = self.x, self.y
        return (self, P(y, -x), P(-x, -y), P(-y, x))[d]

    def is_inside(self):
        return self.x >= 0 and self.x < W and self.y >= 0 and self.y < H


class Samurai(object):
    def __init__(self, p, done, hidden, treatment):
        self.p = p
        self.done = done
        self.hidden = hidden
        self.treatment = treatment

    def __str__(self):
        return ('Samurai(%s, %s, %s, %s)' %
                (self.p, self.done, self.hidden, self.treatment))

    def __deepcopy__(self, _):
        return Samurai(copy.copy(self.p), self.done, self.hidden,
                       self.treatment)

HOMES = [P(0, 0), P(0, 7), P(7, 0), P(14, 14), P(14, 7), P(7, 14)]
WEAPONS = [[P(0, 1), P(0, 2), P(0, 3), P(0, 4)],
           [P(1, 0), P(2, 0), P(0, 1), P(1, 1), P(0, 2)],
           [P(-1, -1), P(1, -1), P(-1, 0), P(0, 1), P(-1, 1), P(0, 1), P(1, 1)]]

def is_home(p):
    return p in HOMES


class State(object):
    def __init__(self, my_team, turn, samurais, maps):
        self.my_team = my_team
        self.turn = turn
        self.samurais = samurais
        self.maps = maps

    def __deepcopy__(self, memo):
        return State(self.my_team, self.turn,
                     copy.deepcopy(self.samurais, memo),
                     copy.deepcopy(self.maps, memo))

    def home_of(self, si):
        return HOMES[si % 3 + 3 * ((si // 3) ^ self.my_team)]

    @staticmethod
    def read_turn(my_team):
        turn = int(input())
        samurais = []
        for _ in range(6):
            x, y, done, hidden, treatment = [int(x) for x in input().split()]
            samurais.append(Samurai(P(x, y), done, hidden, treatment))
        maps = []
        for _ in range(H):
            maps.append([int(x) for x in input().split()])
        return State(my_team, turn, samurais, maps)

    def apply_cmd(self, si, cmd):
        samurais, maps = self.samurais, self.maps
        if cmd <= 4:
            sp = samurais[si].p
            for dp in WEAPONS[si]:
                p1 = sp + dp.rotate(cmd - 1)
                if not(p1.is_inside()) or is_home(p1):
                    continue
                for j in range(3, 6, 1):
                    if p1 == samurais[j].p:
                        p2 = self.home_of(j)
                        samurais[j] = (p2[0], p2[1], samurais[j].done, 0, 18)
                maps[p1.y][p1.x] = si
        elif cmd <= 8:
            samurais[si].p += P(0, 1).rotate(cmd - 5)
        else:
            samurais[si].hidden ^= 1

    def apply_cmds(self, cmds):
        ret = copy.deepcopy(self)
        p = cmds[0]
        for c in cmds[1:]:
            ret.apply_cmd(p, c)
        return ret

    def is_my_area(self, p1):
        return self.maps[p1.y][p1.x] in {0, 1, 2}

    def samurai_positions(self):
        return [s.p for s in self.samurais if s.hidden == 0]

    def can_move(self, si, c):
        samurai = self.samurais[si]
        p = samurai.p
        p1 = p + P(0, 1).rotate(c - 5)
        if not p1.is_inside():
            return False
        if is_home(p1) and p1 != self.home_of(si):
            return False
        if samurai.hidden:
            return self.is_my_area(p1)
        return p1 not in self.samurai_positions()

    def can_show_hide(self, si):
        samurai = self.samurais[si]
        p = samurai.p
        if samurai.hidden:
            return p not in self.samurai_positions()
        return self.is_my_area(p)

    def make_moves_player(self, moves, si, cmds, cost):
        moves.append(cmds + [0])
        if cost <= 0:
            return
        samurais = self.samurais
        cs = []
        if cost >= 4 and not samurais[si].hidden:
            cs.extend(c for c in range(1, 5, 1))
        if cost >= 2:
            for c in range(5, 9, 1):
                if self.can_move(si, c):
                    cs.append(c)
        if self.can_show_hide(si):
            cs.append(9)
        for c in cs:
            new_state = copy.deepcopy(self)
            new_state.apply_cmd(si, c)
            new_state.make_moves_player(moves, si, cmds + [c], cost - 4)

    def make_moves(self):
        samurais = self.samurais
        moves = []
        for si in range(3):
            done, treatment = samurais[si].done, samurais[si].treatment
            if done != 0:
                continue
            if treatment > 0:
                moves.append([si])
                continue
            self.make_moves_player(moves, si, [si], 7)
        return moves
