import random

class rps_bot:
    def __init__(self):
        self.regret_sum = [0.0, 0.0, 0.0]
        self.strategy_sum = [0.0, 0.0, 0.0]

    def get_strategy(self):
        """
        Return current mixed strategy based on regret-matching.
        """
        positive = [r if r > 0 else 0 for r in self.regret_sum]
        total = sum(positive)
        if total > 0:
            return [p / total for p in positive]
        # if no positive regret, play uniformly
        return [1/3, 1/3, 1/3]

    def make_move(self, game_state=None):
        """
        Decide next move and update regrets from the previous round.

        game_state.logs: list of (your_move, outcome)
        game_state.round: current round index (0-based)

        Returns:
            int: 0=rock, 1=paper, 2=scissors
        """
        # Regret update if not the first round
        if game_state and game_state.round > 0:
            last_move, outcome = game_state.logs[-1]
            # infer opponent's move
            if outcome == "win":
                opp_move = (last_move + 2) % 3
            elif outcome == "loss":
                opp_move = (last_move + 1) % 3
            else:  # tie
                opp_move = last_move
            # compute counterfactual utilities
            utilities = []
            for a in range(3):
                if a == opp_move:
                    utilities.append(0)
                elif (a + 1) % 3 == opp_move:
                    utilities.append(1)
                else:
                    utilities.append(-1)
            actual_util = utilities[last_move]
            # update regret sums
            for i in range(3):
                self.regret_sum[i] += utilities[i] - actual_util

        # get mixed strategy via regret-matching
        strategy = self.get_strategy()
        # accumulate strategy for average strategy calculation
        for i in range(3):
            self.strategy_sum[i] += strategy[i]

        # sample action from strategy
        r = random.random()
        cum = 0.0
        for i, p in enumerate(strategy):
            cum += p
            if r < cum:
                return i
        return 2  # fallback to scissors

    def get_average_strategy(self):
        """
        Returns the average strategy over all iterations so far.
        """
        total = sum(self.strategy_sum)
        if total > 0:
            return [s / total for s in self.strategy_sum]
        return [1/3, 1/3, 1/3]

