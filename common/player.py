from enum import Enum


class Team(Enum):
    team_one = 0
    team_two = 1


class Player:
    def __init__(self, index, player_set):
        self.index = index
        if self.index % 2 == 0:
            self.weight = 1
            self.team = Team.team_one
        else:
            self.weight = -1
            self.team = Team.team_two

        self.player_set = player_set

    def get_next_player(self):
        return self.player_set.get_next_player(self)

    def get_opponent_team(self):
        return Team.team_one if self.team is Team.team_two else Team.team_two


class PlayerSet:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = []
        for i in range(num_players):
            player = Player(i, self)
            self.players.append(player)

    def get_first_player(self):
        return self.players[0]

    def get_next_player(self, player):
        return self.players[(player.index + 1) % self.num_players]
