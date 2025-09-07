from dataclasses import dataclass


@dataclass
class MatchData:
    j1: str
    j2: str
    score_1: float = 0.0
    score_2: float = 0.0

    def j1_win(self):
        self.score_1 = 1.0
        self.score_2 = 0.0

    def j2_win(self):
        self.score_1 = 0.0
        self.score_2 = 1.0

    def draw(self):
        self.score_1 = 0.5
        self.score_2 = 0.5

    def to_tuple(self):
        """format tuple ([joueur, score], [joueur, score])"""
        return ([self.j1, self.score_1], [self.j2, self.score_2])
