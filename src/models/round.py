from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import datetime

Match = Tuple[List[str | float], List[str | float]]


@dataclass
class Round:
    name: str
    matchs: List[Match] = field(default_factory=list)
    start_date: datetime = field(default_factory=datetime.now)
    ending_date: datetime = None

    def add_match(self, match: Match):
        self.matchs.append(match)

    def matchDone(self):
        self.ending_date = datetime.now()

    def __str__(self):
        resume = f"{self.name} (début: {self.start_date}"
        if self.ending_date:
            resume += f", fin: {self.ending_date}"
        resume += ")\n"
        for m in self.matchs:
            resume += f"- {m[0][0]} ({m[0][1]}) vs {m[1][0]} ({m[1][1]})\n"
        return resume
