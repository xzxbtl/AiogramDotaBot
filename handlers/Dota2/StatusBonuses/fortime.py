
from aiogramproject.handlers.Dota2.StatusBonuses.forclicker import MoreAwardWithStatusClicker
from datetime import datetime, timedelta


class PassiveAwardWithStatus(MoreAwardWithStatusClicker):
    last_execution = {}

    async def reward_for_time(self, user_id):
        current_time = datetime.now()

        if user_id in self.last_execution:
            last_executed_time = self.last_execution[user_id]
            time_diff = current_time - last_executed_time

            if time_diff < timedelta(hours=1):
                return None

        self.last_execution[user_id] = current_time

        if self.status_name == "Guardian":
            self.prize_pool += 0
        elif self.status_name == "Crusader":
            self.prize_pool += 100
        elif self.status_name == "Archon":
            self.prize_pool += 200
        elif self.status_name == "Legend":
            self.prize_pool += 300
        elif self.status_name == "Ancient 💪":
            self.prize_pool += 400
        elif self.status_name == "Divine ☠️":
            self.prize_pool += 550
        elif self.status_name == "Titan 🔥":
            self.prize_pool += 850
        else:
            self.prize_pool += 0

        return self.prize_pool
