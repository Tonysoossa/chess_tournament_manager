from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import datetime

Match = Tuple[List[str | float], List[str | float]]


@dataclass
class Round:
    name: str
    matchs: List[Match] = field(default_factory=list)
    start_date: str = field(
        default_factory=lambda: datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    )
    ending_date: str = None
    round_winner: str = ""  # "name (national_id)"

    def add_match(self, match: Match):
        self.matchs.append(match)

    def matchDone(self):
        self.ending_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def set_winner(self, winner: str):
        """Définit le gagnant du round."""
        self.round_winner = winner

    def calculate_winner(self):
        """Calcule le gagnant du round basé sur les scores des matchs."""
        if not self.matchs:
            return

        # Dictionnaire pour accumuler les points de chaque joueur
        player_scores = {}

        for match in self.matchs:
            # Format: ([j1_id, j1_name, j1_score], [j2_id, j2_name, j2_score])
            j1_id, j1_name, j1_score = match[0][0], match[0][1], match[0][2]
            j2_id, j2_name, j2_score = match[1][0], match[1][1], match[1][2]

            if j1_id not in player_scores:
                player_scores[j1_id] = {"name": j1_name, "score": 0.0}
            if j2_id not in player_scores:
                player_scores[j2_id] = {"name": j2_name, "score": 0.0}

            player_scores[j1_id]["score"] += j1_score
            player_scores[j2_id]["score"] += j2_score

        # Trouver le score maximum
        max_score = max(p["score"] for p in player_scores.values())

        # Trouver tous les joueurs avec le score maximum
        winners = [
            f"{p['name']} ({pid})"
            for pid, p in player_scores.items()
            if p["score"] == max_score
        ]

        if len(winners) == 1:
            self.round_winner = winners[0]
        else:
            self.round_winner = " et ".join(winners) + " (ex aequo)"

    def __str__(self):
        resume = f"{self.name} (début: {self.start_date}"
        if self.ending_date:
            resume += f", fin: {self.ending_date}"
        resume += ")\n"
        for m in self.matchs:
            # Format: ([j1_id, j1_name, j1_score], [j2_id, j2_name, j2_score])
            j1_id, j1_name, j1_score = m[0][0], m[0][1], m[0][2]
            j2_id, j2_name, j2_score = m[1][0], m[1][1], m[1][2]
            resume += f"- {j1_name} ({j1_id}) [{j1_score}] vs {j2_name} ({j2_id}) [{j2_score}]\n"
        if self.round_winner:
            resume += f"🏆 Gagnant du round: {self.round_winner}\n"
        return resume
