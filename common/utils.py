from common.constants import scores


def init_sigma(node, output = None):
    output = dict()

    def init_sigma_recursive(node):
        output[node.inf_set()] = {action: 1. / len(node.actions) for action in node.actions}
        for k in node.children:
            init_sigma_recursive(node.children[k])

    init_sigma_recursive(node)
    return output


def init_empty_node_maps(node, output=None):
    output = dict()

    def init_empty_node_maps_recursive(node):
        output[node.inf_set()] = {action: 0. for action in node.actions}
        for k in node.children:
            init_empty_node_maps_recursive(node.children[k])
    init_empty_node_maps_recursive(node)
    return output


def init_player_rewards_dict(root):
    return {index: 0 for index in range(root.num_players)}


def get_value(card):
    return card[0]


def get_result(cards):
    return 1 if scores[get_value(cards[0])] > scores[get_value(cards[1])] else -1


def update_team_rewards(best_team_rewards, team_rewards):
    for team, reward in team_rewards.items():
        if not best_team_rewards[team] or (reward and reward > best_team_rewards[team]):
            best_team_rewards[team] = reward

    return best_team_rewards
