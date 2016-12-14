"""
The Game module for Samurai coding 2016
"""

from __future__ import division
from __future__ import print_function
import copy
W, H = 15, 15


def is_inside(p):
    x, y = p
    return x >= 0 and x < W and y >= 0 and y < H


HOMES = [(0, 0), (0, 7), (7, 0), (14, 14), (14, 7), (7, 14)]


def is_home(p):
    return p in HOMES


def home_of(state, si):
    return HOMES[si % 3 + 3 * ((si // 3) ^ state[0])]


def read_turn(my_team):
    turn = int(input())
    samurais = []
    for _ in range(6):
        samurais.append([int(x) for x in input().split()])
    maps = []
    for _ in range(H):
        maps.append([int(x) for x in input().split()])
    return (my_team, turn, samurais, maps)


WEAPONS = [[(0, 1), (0, 2), (0, 3), (0, 4)],
           [(1, 0), (2, 0), (0, 1), (1, 1), (0, 2)],
           [(-1, -1), (1, -1), (-1, 0), (0, 1), (-1, 1), (0, 1), (1, 1)]]
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def add_p(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])


def rotate_dir(p, d):
    x, y = p
    return (p, (y, -x), (-x, -y), (-y, x))[d]


def apply_cmd(state, si, cmd):
    (_, _, samurais, maps) = state
#    print('apply_cmd(state = %s, si = %s, cmd = %s)' % (state, si, cmd))
    if cmd <= 4:
        sp = samurais[si][:2]
        for dp in WEAPONS[si]:
            p1 = add_p(sp, rotate_dir(dp, cmd - 1))
            if not(is_inside(p1)) or is_home(p1):
                continue
            for j in range(3, 6, 1):
                (x, y, done, _, _) = samurais[j]
                if p1 == (x, y):
                    p2 = home_of(state, j)
                    samurais[j] = (p2[0], p2[1], done, 0, 18)
            maps[p1[y]][p1[x]] = si
    elif cmd <= 8:
        samurais[si][0] += DIRS[cmd - 5][0]
        samurais[si][1] += DIRS[cmd - 5][1]
    else:
        samurais[si][3] ^= 1


def apply_cmds(state, cmds):
    ret = copy.deepcopy(state)
    p = cmds[0]
    for c in cmds[1:]:
        apply_cmd(ret, p, c)
    return ret


def is_hidden(samurai, cmds):
    (_, _, _, hidden, _) = samurai
    return (hidden + cmds.count(9)) % 2 == 1


def is_my_area(state, p1):
    (x, y) = p1
#    print("%s %s %s" % (x, y, state))
    return state[3][y][x] in {0, 1, 2}


def samurai_positions(state):
    return [(s[0], s[1]) for s in state[2] if s[3] == 0]


def can_move(state, si, c):
    (x, y, _, hidden, _) = state[2][si]
    p = (x, y)
    p1 = add_p(p, DIRS[c - 5])
#    print('can_move(p = %s, p1 = %s, c = %s)' % (p, p1, c))
    if not is_inside(p1):
        return False
    if is_home(p1) and p1 != home_of(state, si):
        return False
    if hidden:
        return is_my_area(state, p1)
    return p1 not in samurai_positions(state)


def can_show_hide(state, si):
    (x, y, _, hidden, _) = state[2][si]
    p = (x, y)
    if hidden:
        return p not in samurai_positions(state)
    return is_my_area(state, p)


def make_moves_player(moves, state, si, cmds, cost):
#    print('make_moves_player(cmds = %s, state = %s)' % (cmds, state))
    moves.append(cmds + [0])
    if cost <= 0:
        return
    (_, _, samurais, _) = state
    cs = []
    if cost >= 4 and samurais[si][3] == 0:
        cs.extend(c for c in range(1, 5, 1))
    if cost >= 2:
        for c in range(5, 9, 1):
            if can_move(state, si, c):
                cs.append(c)
    if can_show_hide(state, si):
        cs.append(9)
    for c in cs:
        new_state = copy.deepcopy(state)
        apply_cmd(new_state, si, c)
        make_moves_player(moves, new_state, si, cmds + [c], cost - 4)


def make_moves(state):
    (_, _, samurais, _) = state
    moves = []
    for si in range(3):
        (_, _, done, _, treatment) = samurais[si]
        if done != 0:
            continue
        if treatment > 0:
            moves.append([si])
            continue
        make_moves_player(moves, state, si, [si], 7)
    return moves
