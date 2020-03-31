class Player:
    def __init__(self, index, player_set):
        self.index = index
        if self.index % 2 == 0:
            self.weight = 1
            self.team = 1
        else:
            self.weight = -1
            self.team = 2

        self.player_set = player_set

    def get_next_player(self):
        return self.player_set.get_next_player(self)


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
