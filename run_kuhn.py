from common.constants import CARDS_DEALINGS, NUM_PLAYERS
from games.algorithms import ChanceSamplingCFR, VanillaCFR
from games.kuhn import KuhnRootChanceGameState


root = KuhnRootChanceGameState(NUM_PLAYERS, CARDS_DEALINGS)
chance_sampling_cfr = ChanceSamplingCFR(root)
chance_sampling_cfr.run(iterations=1000)
chance_sampling_cfr.compute_nash_equilibrium()
# read Nash-Equilibrum via chance_sampling_cfr.nash_equilibrium member
# try chance_sampling_cfr.value_of_the_game() function to get value of the game (-1/18)

# vanilla cfr
vanilla_cfr = VanillaCFR(root)
vanilla_cfr.run(iterations=1000)
vanilla_cfr.compute_nash_equilibrium()

print(vanilla_cfr.value_of_the_game())
print(chance_sampling_cfr.value_of_the_game())
