from common.constants import CARDS_DEALINGS, NUM_PLAYERS
from games.algorithms import ChanceSamplingCFR, VanillaCFR
from games.kuhn import KuhnRootChanceGameState


root = KuhnRootChanceGameState(NUM_PLAYERS, CARDS_DEALINGS)
print("\nChance Sampling CFR without tied-rewards")
chance_sampling_cfr = ChanceSamplingCFR(root)
chance_sampling_cfr.run(iterations=1000, tied_rewards=False)
chance_sampling_cfr.compute_nash_equilibrium()
# read Nash-Equilibrum via chance_sampling_cfr.nash_equilibrium member
# try chance_sampling_cfr.value_of_the_game() function to get value of the game (-1/18)
results = chance_sampling_cfr.value_of_the_game()
print("results:: Game value: {}".format(results[0]))
print("Player rewards:: ", "".join(["{}: {} ".format(k, v) for k, v in results[1].items()]))
print("Team 1 reward: {} Team 2 reward: {}".format((results[1][0] + results[1][2])/2, (results[1][1] + results[1][3])/2))
print("Avg Team reward: {}".format(sum(results[1].values())/4))

root = KuhnRootChanceGameState(NUM_PLAYERS, CARDS_DEALINGS)
print("\nChance Sampling CFR with tied-rewards")
chance_sampling_cfr = ChanceSamplingCFR(root)
chance_sampling_cfr.run(iterations=1000, tied_rewards=True)
chance_sampling_cfr.compute_nash_equilibrium()
# read Nash-Equilibrum via chance_sampling_cfr.nash_equilibrium member
# try chance_sampling_cfr.value_of_the_game() function to get value of the game (-1/18)
results = chance_sampling_cfr.value_of_the_game()
print("results:: Game value: {}".format(results[0]))
print("Player rewards:: ", "".join(["{}: {} ".format(k, v) for k, v in results[1].items()]))
print("Team 1 reward: {} Team 2 reward: {}".format((results[1][0] + results[1][2])/2, (results[1][1] + results[1][3])/2))
print("Avg Team reward: {}".format(sum(results[1].values())/4))

# vanilla cfr
root = KuhnRootChanceGameState(NUM_PLAYERS, CARDS_DEALINGS)
print("\nVanilla CFR without tied rewards")
vanilla_cfr = VanillaCFR(root)
vanilla_cfr.run(iterations=1000, tied_rewards=False)
vanilla_cfr.compute_nash_equilibrium()

results = vanilla_cfr.value_of_the_game()
print("results:: Game value: {}".format(results[0]))
print("Player rewards:: ", "".join(["{}: {} ".format(k, v) for k, v in results[1].items()]))
print("Team 1 reward: {} Team 2 reward: {}".format((results[1][0] + results[1][2])/2, (results[1][1] + results[1][3])/2))
print("Avg Team reward: {}".format(sum(results[1].values())/4))

# vanilla cfr
root = KuhnRootChanceGameState(NUM_PLAYERS, CARDS_DEALINGS)
print("\nVanilla CFR with tied rewards")
vanilla_cfr = VanillaCFR(root)
vanilla_cfr.run(iterations=1000, tied_rewards=True)
vanilla_cfr.compute_nash_equilibrium()

results = vanilla_cfr.value_of_the_game()
print("results:: Game value: {}".format(results[0]))
print("Player rewards:: ", "".join(["{}: {} ".format(k, v) for k, v in results[1].items()]))
print("Team 1 reward: {} Team 2 reward: {}".format((results[1][0] + results[1][2])/2, (results[1][1] + results[1][3])/2))
print("Avg Team reward: {}".format(sum(results[1].values())/4))
