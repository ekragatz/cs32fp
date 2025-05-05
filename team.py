### cs32_fp/team.py

class Team:
    # sets up a new team object with a name, optional list of players, and a starting score of 0
    def __init__(self, name, players=None):
        self.name = name
        self.players = players if players is not None else []
        self.score = 0

    # adds a player's name to the team's player list
    def add_player(self, player_name):
        self.players.append(player_name)

    # increases the team score by the number of points given
    def add_points(self, points):
        self.score += points

    # subracts points from the team score but never lets it get below 0
    def subtract_points(self, points):
        self.score = max(0, self.score - points)

    def __str__(self):
        return f"Team {self.name} | Score: {self.score} | Players: {', '.join(self.players)}"
