from models.player import load_players
from models.round import Round
from models.match import MatchData


def load_tournaments():
    players = load_players()

    m1 = MatchData(players[0].name, players[1].name)
    m1.j1_win()

    m2 = MatchData(players[2].name, players[3].name)
    m2.draw()

    round1 = Round("Round 1")
    round1.add_match(m1.to_tuple())
    round1.add_match(m2.to_tuple())
    round1.matchDone()

    print(round1)
