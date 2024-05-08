class MoreAwardWithStatusClicker:
    def __init__(self, status_name, prize_pool):
        self.status_name = status_name
        self.prize_pool = prize_pool

    async def add_prize_pool(self):
        if self.status_name == "Guardian":
            self.prize_pool += 1.5
        elif self.status_name == "Crusader":
            self.prize_pool += 2
        elif self.status_name == "Archon":
            self.prize_pool += 3
        elif self.status_name == "Legend":
            self.prize_pool += 4
        elif self.status_name == "Ancient 💪":
            self.prize_pool += 5
        elif self.status_name == "Divine ☠️":
            self.prize_pool += 7
        elif self.status_name == "Titan 🔥":
            self.prize_pool += 14
        else:
            self.prize_pool += 0

        return self.prize_pool
