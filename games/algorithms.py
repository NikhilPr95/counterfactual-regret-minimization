from functools import reduce

from common.constants import A, B
from common.utils import init_sigma, init_empty_node_maps, init_player_rewards_dict, update_team_rewards
from games.kuhn import KuhnPlayerMoveGameState


class CounterfactualRegretMinimizationBase:
    def __init__(self, root, chance_sampling=False):
        self.root = root
        self.sigma = init_sigma(root)
        self.cumulative_regrets = init_empty_node_maps(root)
        self.cumulative_sigma = init_empty_node_maps(root)
        self.nash_equilibrium = init_empty_node_maps(root)
        self.chance_sampling = chance_sampling
        self.player_rewards = init_player_rewards_dict(root)
        self.root_reward = 0

    def _update_sigma(self, i):
        rgrt_sum = sum(filter(lambda x: x > 0, self.cumulative_regrets[i].values()))
        for a in self.cumulative_regrets[i]:
            self.sigma[i][a] = max(self.cumulative_regrets[i][a], 0.) / rgrt_sum if rgrt_sum > 0 \
                                    else 1. / len(self.cumulative_regrets[i].keys())

    def compute_nash_equilibrium(self):
        self.__compute_ne_rec(self.root)

    def __compute_ne_rec(self, node):
        if node.is_terminal():
            return
        i = node.inf_set()
        if node.is_chance():
            self.nash_equilibrium[i] = {a: node.chance_prob() for a in node.actions}
        else:
            sigma_sum = sum(self.cumulative_sigma[i].values())
            self.nash_equilibrium[i] = {a: self.cumulative_sigma[i][a] / sigma_sum for a in node.actions}
        # go to subtrees
        for k in node.children:
            self.__compute_ne_rec(node.children[k])

    def _cumulate_cfr_regret(self, information_set, action, regret):
        self.cumulative_regrets[information_set][action] += regret

    def _cumulate_sigma(self, information_set, action, prob):
        self.cumulative_sigma[information_set][action] += prob

    def _cumulate_player_value(self, player_index, game_value):
        self.player_rewards[player_index] += game_value

    def _cumulate_root_value(self, game_value):
        self.root_reward += game_value

    def run(self, iterations):
        raise NotImplementedError("Please implement run method")

    def value_of_the_game(self):
        return self.__value_of_the_game_state_recursive(self.root), {k: v/360 for k, v in self.player_rewards.items()}

    def _cfr_utility_recursive(self, state, reach_probs):
        children_states_utilities = {}

        if state.is_terminal():
            # evaluate terminal node according to the game result
            return state.evaluation()

        if state.is_chance():
            if self.chance_sampling:
                # if node is a chance node, lets sample one child node and proceed normally
                return self._cfr_utility_recursive(state.sample_one(), reach_probs)
            else:
                chance_outcomes = {state.play(action) for action in state.actions}
                return state.chance_prob() * sum([self._cfr_utility_recursive(outcome, reach_probs)
                                                  for outcome in chance_outcomes])

        # sum up all utilities for playing actions in our game state
        value = 0.
        for action in state.actions:
            # child_reach_a = reach_a * (self.sigma[state.inf_set()][action] if state.current_player.index == 0 else 1)
            # child_reach_b = reach_b * (self.sigma[state.inf_set()][action] if state.current_player.index == 1 else 1)

            child_reach_probs = [0.] * len(reach_probs)
            for i, reach in enumerate(reach_probs):
                child_reach_probs[i] = reach * (self.sigma[state.inf_set()][action]
                                                if state.current_player.index == i else 1)

            # value as if child state implied by chosen action was a game tree root
            # child_state_utility = self._cfr_utility_recursive(state.play(action), child_reach_a, child_reach_b)
            child_state_utility = self._cfr_utility_recursive(state.play(action), child_reach_probs)

            # value computation for current node
            value += self.sigma[state.inf_set()][action] * child_state_utility
            # values for chosen actions (child nodes) are kept here
            children_states_utilities[action] = child_state_utility

        # we are computing regrets for both players simultaneously, therefore we need to relate reach, reach_opponent
        # to the player acting in current node, for player A, it is different than for player B
        # (cfr_reach, reach) = (reach_b, reach_a) if state.current_player.index == 0 else (reach_a, reach_b)

        reach = reach_probs[state.current_player.index]
        cfr_reach_probs = [reach for i, reach in enumerate(reach_probs) if i != state.current_player.index]

        for action in state.actions:
            # we multiply regret by -1 for player B, this is because value is computed from player A perspective
            # again we need that perspective switch

            # assuming cfr_reach is product of other player probs
            cfr_reach = reduce(lambda x, y: x*y, cfr_reach_probs)
            action_cfr_regret = state.current_player.weight * cfr_reach * (children_states_utilities[action] - value)
            self._cumulate_cfr_regret(state.inf_set(), action, action_cfr_regret)
            self._cumulate_sigma(state.inf_set(), action, reach * self.sigma[state.inf_set()][action])

        if self.chance_sampling:
            # update sigma according to cumulative regrets - we can do it here because we are using chance sampling
            # and so we only visit single game_state from an information set (chance is sampled once)
            self._update_sigma(state.inf_set())

        return value

    def _cfr_utility_recursive_tied_rewards(self, state, reach_probs):
        children_states_utilities = {}

        if state.is_terminal():
            # evaluate terminal node according to the game result
            reward = state.evaluation()
            return reward, {state.current_player.team: reward, state.current_player.get_opponent_team(): None}

        if state.is_chance():
            if self.chance_sampling:
                # if node is a chance node, lets sample one child node and proceed normally
                return self._cfr_utility_recursive_tied_rewards(state.sample_one(), reach_probs)
            else:
                chance_outcomes = {state.play(action) for action in state.actions}
                utility_sum = 0
                for outcome in chance_outcomes:
                    child_utility, team_rewards = self._cfr_utility_recursive_tied_rewards(outcome, reach_probs)
                    if hasattr(state, 'current_player') and team_rewards[state.current_player.team]:
                        print("going in here")
                        utility_sum += team_rewards[state.current_player.team]
                    else:
                        utility_sum += child_utility
                return state.chance_prob() * utility_sum

        # sum up all utilities for playing actions in our game state
        value = 0.
        best_team_rewards = {state.current_player.team: None, state.current_player.get_opponent_team(): None}

        for action in state.actions:
            # child_reach_a = reach_a * (self.sigma[state.inf_set()][action] if state.current_player.index == 0 else 1)
            # child_reach_b = reach_b * (self.sigma[state.inf_set()][action] if state.current_player.index == 1 else 1)

            child_reach_probs = [0.] * len(reach_probs)
            for i, reach in enumerate(reach_probs):
                child_reach_probs[i] = reach * (self.sigma[state.inf_set()][action]
                                                if state.current_player.index == i else 1)

            # value as if child state implied by chosen action was a game tree root
            # child_state_utility = self._cfr_utility_recursive(state.play(action), child_reach_a, child_reach_b)
            child_state_utility, team_rewards = self._cfr_utility_recursive_tied_rewards(state.play(action), child_reach_probs)

            best_team_rewards = update_team_rewards(best_team_rewards, team_rewards)
            # value computation for current node
            # print("tr", team_rewards)
            if team_rewards[state.current_player.team]:
                value += team_rewards[state.current_player.team]
            else:
                value += self.sigma[state.inf_set()][action] * child_state_utility
            # values for chosen actions (child nodes) are kept here
            children_states_utilities[action] = child_state_utility

        # we are computing regrets for both players simultaneously, therefore we need to relate reach, reach_opponent
        # to the player acting in current node, for player A, it is different than for player B
        # (cfr_reach, reach) = (reach_b, reach_a) if state.current_player.index == 0 else (reach_a, reach_b)

        reach = reach_probs[state.current_player.index]
        cfr_reach_probs = [reach for i, reach in enumerate(reach_probs) if i != state.current_player.index]

        for action in state.actions:
            # we multiply regret by -1 for player B, this is because value is computed from player A perspective
            # again we need that perspective switch

            # assuming cfr_reach is product of other player probs
            cfr_reach = reduce(lambda x, y: x*y, cfr_reach_probs)
            action_cfr_regret = state.current_player.weight * cfr_reach * (children_states_utilities[action] - value)
            self._cumulate_cfr_regret(state.inf_set(), action, action_cfr_regret)
            self._cumulate_sigma(state.inf_set(), action, reach * self.sigma[state.inf_set()][action])

        if self.chance_sampling:
            # update sigma according to cumulative regrets - we can do it here because we are using chance sampling
            # and so we only visit single game_state from an information set (chance is sampled once)
            self._update_sigma(state.inf_set())

        return value, best_team_rewards

    def __value_of_the_game_state_recursive(self, node, recurse_index=-1):
        value = 0.
        if node.is_terminal():
            return node.evaluation()
        recurse_index += 1
        for action in node.actions:
            action_value = self.nash_equilibrium[node.inf_set()][action] \
                     * self.__value_of_the_game_state_recursive(node.play(action), recurse_index)
            value += action_value
            if isinstance(node, KuhnPlayerMoveGameState):
                    self._cumulate_player_value(node.current_player.index, action_value)

        return value


class VanillaCFR(CounterfactualRegretMinimizationBase):

    def __init__(self, root):
        super().__init__(root=root, chance_sampling=False)

    def run(self, iterations=1, tied_rewards=False):
        for i in range(0, iterations):
            # if i % 1000 == 0:
                # print("iteration: ", i)
            if tied_rewards:
                self._cfr_utility_recursive_tied_rewards(self.root, [1] * self.root.num_players)
            else:
                self._cfr_utility_recursive(self.root, [1]*self.root.num_players)
            # since we do not update sigmas in each information set while traversing, we need to
            # traverse the tree to perform to update it now
            self.__update_sigma_recursively(self.root)

    def __update_sigma_recursively(self, node):
        # stop traversal at terminal node
        if node.is_terminal():
            return
        # omit chance
        if not node.is_chance():
            self._update_sigma(node.inf_set())
        # go to subtrees
        for k in node.children:
            self.__update_sigma_recursively(node.children[k])


class ChanceSamplingCFR(CounterfactualRegretMinimizationBase):

    def __init__(self, root):
        super().__init__(root=root, chance_sampling=True)

    def run(self, iterations=1, tied_rewards=False):
        for i in range(0, iterations):
            # if i % 1000 == 0:
            #     print("iteration: ", i)
            if tied_rewards:
                self._cfr_utility_recursive_tied_rewards(self.root, [1] * self.root.num_players)
            else:
                self._cfr_utility_recursive(self.root, [1]*self.root.num_players)
