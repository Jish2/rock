# game_state
# state.logs = (yourmove, outcome = "win"| "loss" | "tie")[]
# state.round = number

# make_move(game_state) -> 0, 1, 2 = rock, paper, scissors

class rps_bot:
    def __init__(self):
      self.s = [0, 0, 0]
      self.o = { "win": 1, "loss": -1, "tie": 0 }

    def best_outcome(self):
        m = max(self.s)
        for i, v in enumerate(self.s):
            if v == m: return i
        return 0

    def make_move(self, game_state=None):
        move, outcome = game_state.logs[-1]
        self.s[move] += self.o[outcome]
        return self.best_outcome()
