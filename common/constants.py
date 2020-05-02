import itertools
from enum import Enum


# KQ = "KQ"; KJ = "KJ"; QK = "QK"; QJ = "QJ"; JK = "JK"; JQ = "JQ"
# CARDS_DEALINGS = [KQ, KJ, QK, QJ, JK, JQ]

K0Q0 = ("K0", "Q0")
K0J0 = ("K0", "J0")
Q0K0 = ("Q0", "K0")
Q0J0 = ("Q0", "J0")
J0K0 = ("J0", "K0")
J0Q0 = ("J0", "Q0")

# CARDS = ["K0", "Q0", "J0"]
# NUM_PLAYERS = 2

CARDS = ["K0", "Q0", "J0", "K1", "Q1", "J1"]
NUM_PLAYERS = 4

CARDS_DEALINGS = list(itertools.permutations(CARDS, NUM_PLAYERS))


CHANCE = "CHANCE"

CHECK = "CHECK"
CALL = "CALL"
FOLD = "FOLD"
BET = "BET"


RESULTS_MAP = {}

# RESULTS_MAP[QK] = -1
# RESULTS_MAP[JK] = -1
# RESULTS_MAP[JQ] = -1
# RESULTS_MAP[KQ] = 1
# RESULTS_MAP[KJ] = 1
# RESULTS_MAP[QJ] = 1


scores = {"J": 0, "Q": 1, "K": 2}

# RESULTS_MAP[("Q", "K")] = -1
# RESULTS_MAP[("J", "K")] = -1
# RESULTS_MAP[("J", "Q")] = -1
# RESULTS_MAP[("K", "Q")] = 1
# RESULTS_MAP[("K", "J")] = 1
# RESULTS_MAP[("Q", "J")] = 1

A = 1
B = -A
