### cs32_fp/team.py

class Team:
    def __init__(self, name, players=None):
        self.name = name
        self.players = players if players is not None else []
        self.score = 0

    def add_player(self, player_name):
        self.players.append(player_name)

    def add_points(self, points):
        self.score += points

    def subtract_points(self, points):
        self.score = max(0, self.score - points)

    def __str__(self):
        return f"Team {self.name} | Score: {self.score} | Players: {', '.join(self.players)}"
