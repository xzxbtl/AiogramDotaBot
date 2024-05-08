import requests
import opendota
from aiogramproject.logs import logger
from lists.dotaheroes import result

client = opendota.OpenDota()


# Для стима конвектор в STEAM ID 3
class SteamConvector:
    """Переводит Steam64 в Steam32 и наоборот"""

    def __init__(self, steamid):
        self.steamid = steamid

    @staticmethod
    def steamid_to_steamid32(steamid64_result):
        steamid = steamid64_result.split(":")
        return int(steamid[2]) * 2 + int(steamid[1])

    def steamid64_to_steamid(self):
        steamid64 = bin(int(self.steamid))[2:]
        steamid64 = "0" * (64 - len(steamid64)) + steamid64
        x = int(steamid64[:8], base=2)
        y = int(steamid64[-1], base=2)
        z = int(steamid64[-32: -1], base=2)

        return "STEAM_{}:{}:{}".format(x, y, z)

    def steamid64_to_steamid32(self):
        steamid64_result = self.steamid64_to_steamid()
        return self.steamid_to_steamid32(steamid64_result)


# Информация о пользователе
class TakeInfoUser:
    """Парсинг всей инфы через API"""

    def __init__(self, steamid):
        self.steamid = steamid

    def take_user_winrate(self):
        url = f"https://api.opendota.com/api/players/{self.steamid}/wl"
        response = requests.get(url)
        person, user_id, profile_url = self.TakeInfoUser()

        if response.status_code == 200:
            data = response.json()
            if "win" in data and "lose" in data:
                wins = data["win"]
                lose = data["lose"]
                if wins == 0 and lose == 0:
                    return "Возможно профиль скрыт"
                winrate = round(wins / (wins + lose), 2)
                winrate_account = "{:.0%}".format(winrate)
                message = f"Общая статистика аккаунта {person}: \n Побед : {wins} \n Поражений : {lose} \n Винрейт : " \
                          f"{winrate_account} \n steamid: {user_id} \n\n ссылка на профиль: {profile_url}"
                return message
            else:
                return logger.info("requestsOpenDota.py - Профиль скрыт | Недоступны данные о играх")
        else:
            return logger.error("requestsOpenDota.py - Произошла ошибка при попытке поиске по ID")

    def get_heroes_stats(self):
        heroes = client.get_player_heroes(self.steamid)
        messages = []

        for elem in heroes:
            if elem["games"] > 10:
                for item in result["heroes"]:
                    if item["id"] == elem["hero_id"]:
                        elem["hero_id"] = item["name"]
                        winrate = round(elem['win'] / elem['games'], 2)
                        winrate_percentage = "{:.0%}".format(winrate)
                        message = f"Hero: {elem['hero_id']}\n Matches: {elem['games']} \n Wins: {elem['win']} \n " \
                                  f"Winrate: {winrate_percentage}"
                        messages.append(message)
        return messages[:10]

    def take_last_matches(self):
        url = f"https://api.opendota.com/api/players/{self.steamid}/matches"
        response_matches = requests.get(url)
        if response_matches.status_code == 200:
            data = response_matches.json()
            messages = []
            for elem in data[:10]:
                for item in result["heroes"]:
                    if item["id"] == elem["hero_id"]:
                        elem["hero_id"] = item["name"]
                        match_id = elem["match_id"]
                        time = elem["duration"]
                        converted_time = time // 60
                        kills = elem["kills"]
                        death = elem["deaths"]
                        assists = elem["assists"]
                        mess = f"Матч: {match_id} Длительность : {converted_time} мин \n Герой: {elem['hero_id']} \n " \
                               f"Убийств: {kills} | Смертей {death} | Помощи: {assists}"
                        messages.append(mess)
            return messages
        else:
            return logger.error(
                "requestsOpenDota.py - Произошла ошибка при попытке получить список матчей | Запрос 404")

    def TakeInfoUser(self):
        url_for_profile = f"https://api.opendota.com/api/players/{self.steamid}"
        response = requests.get(url_for_profile)
        data = response.json()
        person = data["profile"]["personaname"]
        steamid = data["profile"]["steamid"]
        profile_url = data["profile"]["profileurl"]
        return person, steamid, profile_url


# test = TakeInfoUser(convector.steamid64_to_steamid32())
# print(test.take_user_winrate())  # Общая статистика

# for mess in test.get_heroes_stats():  # Ласт 10 игр
# print(mess)
