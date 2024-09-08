class MoreAwardWithStatusClicker:
    def __init__(self, status_name, prize_pool):
        self.status_name = status_name
        self.prize_pool = prize_pool

    async def add_prize_pool(self):
        if self.status_name == "Guardian":
            self.prize_pool += (1 + 1.5) * self.prize_pool
        elif self.status_name == "Crusader":
            self.prize_pool += (1 + 2) * self.prize_pool
        elif self.status_name == "Archon":
            self.prize_pool += (1 + 3) * self.prize_pool
        elif self.status_name == "Legend":
            self.prize_pool += (1 + 4) * self.prize_pool
        elif self.status_name == "Ancient 💪":
            self.prize_pool += (1 + 5) * self.prize_pool
        elif self.status_name == "Divine ☠️":
            self.prize_pool += (1 + 7) * self.prize_pool
        elif self.status_name == "Titan 🔥":
            self.prize_pool += (1 + 14) * self.prize_pool
        else:
            self.prize_pool += 0

        return self.prize_pool
