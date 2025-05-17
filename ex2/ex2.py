import re

import zuma
import copy

id = ["000000000"]


class Controller:
    """This class is a controller for a Zuma game."""

    def __init__(self, game: zuma.Game):
        """Initialize controller for given game model.
        This method MUST terminate within the specified timeout.
        """
        self.steps_left = 0
        self.original_game = game
        # self.copy_game = copy.deepcopy(game)
        self.model = self.original_game.get_model()
        self._chosen_action_prob = self.model['chosen_action_prob']
        self._next_color_dist = self.model['next_color_dist']
        self._color_pop_prob = self.model['color_pop_prob']
        self._color_pop_reward = self.model['color_pop_reward']
        self._color_not_finished_punishment = self.model['color_not_finished_punishment']
        self._finished_reward = self.model['finished_reward']
        self._seed = self.model['seed']
        self.epsilon = 0.0195
        # self.higher_lower_epsilon = 0.00755
        # self.best_epsilon = 0.0195
        # self.epsilon = 0.003
        # self.epsilon = 0.0031
        self.depth = 1
        self.num_colors = len(self._chosen_action_prob)
        self.cache_mean_action = {}
        self.cache_popped = {}
        self.cache_line_action = {}

    def get_state_key(self, line, current_ball=None, action=None, prob=None):
        return tuple(line), current_ball, action, prob

    def clear_caches(self):
        self.cache_mean_action.clear()
        self.cache_popped.clear()
        self.cache_line_action.clear()

    def choose_next_action(self):
        """Choose next action for Zuma given the current state of the game.
        """

        self.clear_caches()
        line, current_ball, steps, max_steps = self.original_game.get_current_state()

        action = -1
        self.steps_left = max_steps - steps
        if self.steps_left < 3 and current_ball not in line:
            return action
        if self.steps_left < 5 and len(line) < 20:
            self.depth = 2

        if self.depth < self.steps_left:
            t = self.depth
        else:
            t = self.steps_left

        best = self.mean_action(action, current_ball, line, t=t)

        for a in range(0, len(line) + 1):
            curr_reward = self.mean_action(a, current_ball, line, t=t)

            if curr_reward > best:
                action = a
                best = curr_reward

        return action

    def mean_action(self, chosen_action, current_ball, line, prob=1, t=1):

        cache_key = self.get_state_key(line, current_ball, chosen_action, prob)
        if cache_key in self.cache_mean_action:
            return self.cache_mean_action[cache_key]

        # Probability we hit where we aimed
        p_chosen_action = self._chosen_action_prob[current_ball]
        # Or missed
        p_other = (1 - p_chosen_action) / (len(line) + 1)

        line_copy = line.copy()

        if chosen_action != -1:
            line_copy.insert(chosen_action, current_ball)

        E = p_chosen_action * (
            self.popped(line_copy, chosen_action, current_ball, t, prob=prob * p_chosen_action, reward=0))
        if prob * p_other >= self.epsilon:
            for i in range(-1, len(line) + 1):
                if i != chosen_action:
                    line_copy = line.copy()
                    if i != -1:
                        line_copy.insert(i, current_ball)
                    E += p_other * (
                        self.popped(line_copy, chosen_action, current_ball, t, prob=prob * p_other, reward=0))

        self.cache_mean_action[cache_key] = E

        return E

    def popped(self, line_copy, chosen_action, current_ball, t, prob=1, reward=0):

        cache_key = self.get_state_key(line_copy, current_ball, chosen_action, prob)
        if cache_key in self.cache_popped:
            return self.cache_popped[cache_key]

        new_line, new_reward, p_pop, addition = self.R(line_copy, chosen_action)
        if not p_pop:
            result = reward + self.line_action(line_copy, prob, t)
            self.cache_popped[cache_key] = result
            return result

        popped = p_pop * self.popped(new_line, addition, current_ball, t, prob=prob * p_pop,
                                     reward=new_reward + reward)
        not_popped = (1 - p_pop) * (reward + self.line_action(line_copy, prob * (1 - p_pop), t))

        result = popped + not_popped
        self.cache_popped[cache_key] = result
        return result

    def line_action(self, line, prob, t=1):
        cache_key = self.get_state_key(line, prob=prob)
        if cache_key in self.cache_line_action:
            return self.cache_line_action[cache_key]

        if not t:
            if self.steps_left <= 50:
                result = self.reward(line) if self.steps_left - self.depth <= 0 else 0
            else:
                result = self.reward(line) if self.steps_left - self.depth <= 0 else self.h(line)
            self.cache_line_action[cache_key] = result
            return result

        best = 0

        for color, p_color in self._next_color_dist.items():
            best_in_color = 0
            action = -1
            if p_color * prob > self.epsilon:
                best_in_color = self.mean_action(action, color, line, prob=prob * p_color, t=t - 1)

                for a in range(0, len(line) + 1):
                    curr_reward_in_color = self.mean_action(a, color, line, prob=prob * p_color, t=t - 1)

                    best_in_color = max(best_in_color, curr_reward_in_color)
            best += best_in_color * p_color

        self.cache_line_action[cache_key] = best
        return best

    def R(self, line, addition, reward=0):
        burstable = re.finditer(r'1{3,}|2{3,}|3{3,}|4{3,}', ''.join([str(i) for i in line]))
        new_reward = reward
        new_line = line.copy()
        p_pop = 0
        for group in burstable:
            if addition in range(group.span()[0], group.span()[1]):
                p_pop = self._color_pop_prob[line[group.start()]]
                new_reward += (self._color_pop_reward['3_pop'][line[group.start()]] +
                               (group.span()[1] - group.span()[0] - 3) *
                               self._color_pop_reward['extra_pop'][line[group.start()]])
                new_line = line[:group.span()[0]] + line[group.span()[1]:]
                addition = group.span()[0]
                break
        return new_line, new_reward, p_pop, addition

    def h(self, line):
        res_sum = 0
        if not list(line):
            return 0
        for color, p_color in self._next_color_dist.items():
            regex_triple = "((" + str(color) + "), )((" + str(color) + ")(, )?)+"
            doubles = re.findall(regex_triple, str(line))
            res_sum += (len(doubles) * self._color_pop_reward['3_pop'][color]) * p_color
        return res_sum

    def reward(self, line):
        reward = 0
        if len(line) == 0:
            reward += self._finished_reward

        else:
            for k, v in self._color_not_finished_punishment.items():
                num_of_ball = line.count(k)
                reward -= num_of_ball * v

        return reward
