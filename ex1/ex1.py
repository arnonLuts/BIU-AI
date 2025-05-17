import ex1_check
import re

import search
import utils

ids = ["000000000"]

""" Rules """
RED = 1
BLUE = 2
YELLOW = 3
GREEN = 4
COLORS = [RED, BLUE, YELLOW, GREEN]

# For removing repeating cases
succ_set = set()
class ZumaProblem(search.Problem):
    """This class implements a pacman problem"""

    def __init__(self, initial):
        """ Magic numbers for balls:
        1 - red, 2 - blue, 3 - yellow, 4 - green."""

        self.line = initial[0]
        self.ammo = initial[1]
        succ_set.clear()
        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, initial)

    def successor(self, state):
        """ Generates the successor state """
        succ_list = []

        # utils.raiseNotDefined()
        line_arr = list(state[0])
        ammo_arr = list(state[1])
        if not ammo_arr:
            return succ_list

        ammo = ammo_arr.pop(0)
        for i in range(0, len(line_arr) + 1):
            skip = True
            if (i >= 2) and line_arr[i - 1] == line_arr[i - 2]:
                skip = False
            elif (i <= len(line_arr) - 2) and line_arr[i] == line_arr[i + 1]:
                skip = False
            elif ((i >= 1) and (i <= len(line_arr) - 1)) and line_arr[i - 1] == line_arr[i]:
                skip = False
            if skip and (i != 0) and (i < len(line_arr)) and (
                    line_arr[i - 1] != line_arr[i] and line_arr[i] != ammo and line_arr[i - 1] != ammo):
                continue

            tmp_line_arr = line_arr[:]
            tmp_line_arr.insert(i, ammo)
            for c in range(1, len(COLORS) + 1):
                if tuple(tmp_line_arr).count(c) + tuple(ammo_arr).count(c) < 3:
                    continue

            new_state = (tuple(tmp_line_arr), tuple(ammo_arr))
            new_state = rem_bubles(new_state)
            if new_state not in succ_set:
                succ_set.add(new_state)
                succ_list.append((i, new_state))

        succ_list.append((-1, (tuple(line_arr), tuple(ammo_arr))))
        return succ_list

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""
        # utils.raiseNotDefined()
        return not list(state[0])

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state)
        and returns a goal distance estimate"""
        # This heuristic function is a 0,1,2 heuristic which calculates the lowest possible number of
        # balls it would take to clear the line.
        state = node.state
        line, ammo = state
        res_sum = 0
        if not list(line):
            return res_sum
        if not list(ammo):
            return float('inf')
        for i in range(1, len(COLORS) + 1):
            # Find single ball clusters in the line
            regex_single = "(?<!\\b" + str(i) + ", )(" + str(i) + ")(?!, " + str(i) + "\\b)"
            singles = re.findall(regex_single, str(line))
            # Find clusters of two balls in the line
            regex_double = "((" + str(i) + "), )" + str(i)
            doubles = re.findall(regex_double, str(line))
            n_singles = len(singles)
            n_doubles = len(doubles)
            # Because two 2 ball clusters pop when they touch, if there is an uneven number of
            # clusters we need at least one ball to pop them.
            if n_singles < n_doubles:
                rem_doubles = (n_doubles - n_singles) % 2
                # There are still balls of the colour i in the line and in the ammo
                if (i in ammo) and rem_doubles:
                    if res_sum < rem_doubles:
                        res_sum = rem_doubles
                    # Because we now need one more ball but h only returns 0,1,2
                    else:
                        res_sum = rem_doubles + 1
                # no ball in the ammo so we will not be able to pop them.
                elif not (i in ammo) and rem_doubles:
                    return float('inf')
            # Because three 1 ball clusters pop when they touch, and to get n clusters where n>=3 to pop we need
            # at least 2 balls to get the clusters to touch/ pop one of the 1 ball clusters.
            elif n_singles > n_doubles:
                if n_singles - n_doubles < 3:
                    rem_singles = 3 - (n_singles - n_doubles)
                else:
                    rem_singles = 2
                if ammo.count(i) < rem_singles:
                    return float('inf')
                if (i in ammo) and rem_singles and res_sum < rem_singles:
                    res_sum = rem_singles
                # no ball in the ammo so we will not be able to pop them.
                elif not (i in ammo) and rem_singles:
                    return float('inf')

            # If the number of one ball and two ball clusters is equal they
            # can all possibly pop together.

        if len(list(ammo)) < res_sum:
            return float('inf')

        return res_sum


def create_zuma_problem(game):
    print("<<create_zuma_problem")
    """ Create a zuma problem, based on the description.
    game - pair of lists as described in pdf file"""
    return ZumaProblem(game)


def rem_bubles(state):
    row_list = list(state[0])
    for i in range(1, 5):
        group = [i, i, i]
        for j in range(len(row_list) - len(group) + 1):
            if row_list[j: j + len(group)] == group:  # First index that matches with at least 3 bubbles
                while j < len(row_list) and (row_list[j] == i):
                    row_list.pop(j)
                    if not row_list:
                        return (tuple([]), state[1])
                else:
                    break

    state2 = (tuple(row_list), state[1])
    if (state2 != state):
        state = rem_bubles(state2)
    else:
        state = state2

    return state


# game = ()

# create_zuma_problem(game)


if __name__ == '__main__':
    ex1_check.main()
