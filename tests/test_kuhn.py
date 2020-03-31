from games.kuhn import KuhnRootChanceGameState
from common.constants import *
import pytest


def __recursive_tree_assert(root, logical_expression):
    assert logical_expression(root)
    for k in root.children:
        __recursive_tree_assert(root.children[k], logical_expression)


def test_kuhn_tree_actions_number_equal_to_children():
    root = KuhnRootChanceGameState(2, CARDS_DEALINGS)
    __recursive_tree_assert(root, lambda node: len(node.children) == len(node.actions))


def test_kuhn_to_move_chance_at_root():
    root = KuhnRootChanceGameState(2, CARDS_DEALINGS)
    assert root.to_move == CHANCE


def test_kuhn_to_move_changes_correctly_for_children():
    logical_expression = lambda node: all([node.current_player == node.children[k].current_player.get_next_player()
                                           for k in node.children])
    root = KuhnRootChanceGameState(2, CARDS_DEALINGS)
    for k in root.children:
        child = root.children[k]
        __recursive_tree_assert(child, logical_expression)


def test_player_a_acts_first():
    root = KuhnRootChanceGameState(2, CARDS_DEALINGS)
    for k in root.children:
        child = root.children[k]
        # assert child.to_move == A
        assert child.current_player.index == 0


def test_if_only_root_is_chance():
    logical_expression = lambda node: not node.is_chance()
    root = KuhnRootChanceGameState(2, CARDS_DEALINGS)
    assert root.is_chance()
    for k in root.children:
        child = root.children[k]
        __recursive_tree_assert(child, logical_expression)


def test_if_possible_to_play_unavailable_action():
    root = KuhnRootChanceGameState(2, CARDS_DEALINGS)
    with pytest.raises(KeyError):
        root.play(CALL)
    with pytest.raises(KeyError):
        root.play(BET).play(BET)
    with pytest.raises(KeyError):
        root.play(CHECK).play(CALL)


def test_inf_sets():
    root = KuhnRootChanceGameState(2, CARDS_DEALINGS)
    assert root.inf_set() == "."

    assert root.play(K0Q0).inf_set() == ".K0."
    assert root.play(K0Q0).play(BET).inf_set() == ".Q0.BET"
    assert root.play(K0Q0).play(BET).play(FOLD).inf_set() == ".K0.BET.FOLD"

    assert root.inf_set() == "."

    assert root.play(Q0J0).inf_set() == ".Q0."
    assert root.play(Q0J0).play(BET).inf_set() == ".J0.BET"
    assert root.play(Q0J0).play(BET).play(FOLD).inf_set() == ".Q0.BET.FOLD"
    assert root.play(Q0J0).play(BET).play(CALL).inf_set() == ".Q0.BET.CALL"

    assert root.inf_set() == "."

    assert root.play(J0K0).inf_set() == ".J0."
    assert root.play(J0K0).play(CHECK).inf_set() == ".K0.CHECK"
    assert root.play(J0K0).play(CHECK).play(CHECK).inf_set() == ".J0.CHECK.CHECK"
    assert root.play(J0K0).play(CHECK).play(BET).inf_set() == ".J0.CHECK.BET"
    assert root.play(J0K0).play(CHECK).play(BET).play(CALL).inf_set() == ".K0.CHECK.BET.CALL"
    assert root.play(J0K0).play(CHECK).play(BET).play(FOLD).inf_set() == ".K0.CHECK.BET.FOLD"


def test_termination():
    root = KuhnRootChanceGameState(2, CARDS_DEALINGS)

    assert not root.is_terminal()
    assert not root.play(K0Q0).play(BET).is_terminal()
    assert not root.play(J0Q0).play(CHECK).play(BET).is_terminal()
    assert not root.play(Q0J0).play(CHECK).is_terminal()

    assert root.play(K0Q0).play(BET).play(FOLD).is_terminal()
    assert root.play(J0Q0).play(CHECK).play(CHECK).is_terminal()
    assert root.play(J0K0).play(BET).play(CALL).is_terminal()
    assert root.play(Q0J0).play(CHECK).play(BET).play(FOLD).is_terminal()
    assert root.play(Q0J0).play(CHECK).play(BET).play(CALL).is_terminal()


def test_evaluation():
    root = KuhnRootChanceGameState(2, CARDS_DEALINGS)

    KQ_node = root.children[K0Q0]

    assert KQ_node.play(BET).play(FOLD).evaluation() == 1
    assert KQ_node.play(BET).play(CALL).evaluation() == 2
    assert KQ_node.play(CHECK).play(BET).play(FOLD).evaluation() == -1
    assert KQ_node.play(CHECK).play(CHECK).evaluation() == 1

    QJ_node = root.children[Q0J0]

    assert QJ_node.play(BET).play(FOLD).evaluation() == 1
    assert QJ_node.play(BET).play(CALL).evaluation() == 2
    assert QJ_node.play(CHECK).play(BET).play(FOLD).evaluation() == -1
    assert QJ_node.play(CHECK).play(CHECK).evaluation() == 1

    KJ_node = root.children[K0J0]

    assert KJ_node.play(BET).play(FOLD).evaluation() == 1
    assert KJ_node.play(BET).play(CALL).evaluation() == 2
    assert KJ_node.play(CHECK).play(BET).play(FOLD).evaluation() == -1
    assert KJ_node.play(CHECK).play(CHECK).evaluation() == 1

    QK_node = root.children[Q0K0]

    assert QK_node.play(BET).play(FOLD).evaluation() == 1
    assert QK_node.play(BET).play(CALL).evaluation() == -2
    assert QK_node.play(CHECK).play(BET).play(FOLD).evaluation() == -1
    assert QK_node.play(CHECK).play(CHECK).evaluation() == -1

    JQ_node = root.children[J0Q0]

    assert JQ_node.play(BET).play(FOLD).evaluation() == 1
    assert JQ_node.play(BET).play(CALL).evaluation() == -2
    assert JQ_node.play(CHECK).play(BET).play(FOLD).evaluation() == -1
    assert JQ_node.play(CHECK).play(CHECK).evaluation() == -1

    JK_node = root.children[J0K0]

    assert JK_node.play(BET).play(FOLD).evaluation() == 1
    assert JK_node.play(BET).play(CALL).evaluation() == -2
    assert JK_node.play(CHECK).play(BET).play(FOLD).evaluation() == -1
    assert JK_node.play(CHECK).play(CHECK).evaluation() == -1
