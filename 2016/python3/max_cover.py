import itertools
import copy
import pprint

from game import P
from game import WEAPONS

si = 1
initial_cmds = [[1], [1, 5], [1, 7]]
rate = 4.5000001
#si = 2
#initial_cmds = [[1], [1, 5], [1, 6], [1, 7]]
#rate = 4.66

init_p = P(0, 0)
all_cmds = []
for i in range(4):
    all_cmds.append([i + 1])
    all_cmds.append([i + 5])
    for j in range(4):
        all_cmds.append([i + 1, j + 5])
        all_cmds.append([j + 5, i + 1])
        if i <= j and j - i != 2:
            all_cmds.append([i + 5, j + 5])
            for k in range(j, 4, 1):
                if k - j != 2 and k - i != 2:
                    all_cmds.append([i + 5, j + 5, k + 5])
all_cmds.sort()

initial_state = (init_p, ())


def apply_cmds(state, cmds):
    (p, ocs) = state[0], list(state[1])
    for cmd in cmds:
        if cmd < 5:
            for dp in WEAPONS[si]:
                p1 = p + dp.rotate(cmd - 1)
                if p1 not in ocs:
                    ocs.append(p1)
        else:
            p = p + P(0, 1).rotate(cmd - 5)
    return (p, tuple(sorted(ocs)))


def is_opt(l, state, rate):
    return l * rate <= len(state[1])


def is_long_repeat(cmds):
    last_cmd = cmds[-1]
    for i in range(3, len(cmds) // 3 + 1, 1):
        if cmds[-i - 1] == last_cmd:
            if cmds[-i:] == cmds[-2 * i: -i] and cmds[-i:] == cmds[-3 * i: -2 * i]:
                return True
    return False


#def normalized_moves(cmds):
#    if len(cmds) < 2:
#        return True
#    cmd1, cmd2 = cmds[-1], cmds[-2]
##n    moves1 = list(itertools.takewhile(lambda x: x >= 5, reversed(cmd2)))
#    moves = list(reversed(moves1)) + list(itertools.takewhile(lambda x: x >= 5, cmd1))
#    
#    return sorted(moves) == moves

def show_max_repeat(l, opt_states):
    print('%s %s' % (l, len(opt_states)))
    mv, mc = 0, []
    for s in opt_states:
        p, mp = s
        p2 = p + p
        new_mp = set([p + dp for dp in mp])
        new_mp2 = set([p2 + dp for dp in mp])
        c = len(list(p1 for p1 in mp if p1 in new_mp))
        c2 = len(list(p1 for p1 in mp if p1 not in new_mp and p1 in new_mp2))
        v = float(len(mp) - c - c2) / l
        if v > mv:
            mv, mc = v, opt_states[s]
#            print('len(mp) = %s, c = %s, c2 = %s, mv = %s, mc = %s' % (len(mp), c, c2, mv, mc))
#            print('mp=%s' % (mp, ))
    print('%s %s' % (mv, mc))


opt_states = {initial_state : []}

pp = pprint.PrettyPrinter(depth=6)

for l in range(1, 100, 1):
    new_opt_states = {}
    for st in sorted(opt_states, key = lambda x: opt_states[x]):
        old_cmds = opt_states[st]
        for cmds in (all_cmds if l > 1 else initial_cmds):
            new_st = apply_cmds(st, cmds)
            new_cmds = old_cmds + [cmds]
            if not is_opt(l, new_st, rate) or new_st in new_opt_states:
                continue
            if is_long_repeat(new_cmds):
                print(new_cmds)
            new_opt_states[new_st] = new_cmds
    if len(new_opt_states) == 0:
        for st in opt_states:
            old_cmds = opt_states[st]
            print("%s %s" % (old_cmds, st))
    opt_states = new_opt_states
    show_max_repeat(l, opt_states)
