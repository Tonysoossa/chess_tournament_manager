from dataclasses import dataclass


@dataclass
class MatchData:
    j1_id: str  # national_id du joueur 1
    j2_id: str  # national_id du joueur 2
    j1_name: str  # nom du joueur 1 (pour affichage)
    j2_name: str  # nom du joueur 2 (pour affichage)
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
        return (
            [self.j1_id, self.j1_name, self.score_1],
            [self.j2_id, self.j2_name, self.score_2],
        )
