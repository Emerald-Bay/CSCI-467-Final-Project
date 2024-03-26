import requests
import json

# Faceit API key
API_KEY = '82f9e1c0-b21f-4e85-85a9-d8d51d66fd1c'

# Base URL for Faceit API
BASE_URL = 'https://open.faceit.com/data/v4/'

# Player Stats - Using lifetime if given, otherwise using Dust2 Map stats for all others cuz its the most popular/balanced map
class Player_Stats:

    # Below are all member variables that map to the data needed for the model

    # age
    # country
    # headshot_percentage
    # damage_per_round
    # grenade_damage_per_round
    # maps_played
    # rounds_played
    # kills_per_death
    # kills_per_round
    # assists_per_round
    # deaths_per_round
    # saved_teammates_per_round
    # saved_by_teammates_per_round
    # rounds_with_kills
    # opening_kill_ratio
    # team_win_percent_after_first_kill
    # first_kill_in_won_rounds
    # zero_kill_rounds
    # one_kill_rounds
    # two_kill_rounds
    # three_kill_rounds
    # four_kill_rounds
    # five_kill_rounds
    # rifle_kills
    # sniper_kills
    # smg_kills
    # pistol_kills
    # grenade_kills
    # other_kills

    def __init__(self, response):
        print("As the FACEIT API does not allow for us to collect all of your player stats, we will be asking a series of questions to collect the rest of the data, and approximating the rest using your FACEIT stats on the map Dust2. Please answer to the best of your ability. If you do not know your statistic, make your best approximation, and understand that any inaccurate data collected will throw off the prediction from our model\n")

        print("For the following questions, assume that a match consists of all 31 rounds and if a percentage is requested input your answer as a decimal. (1.0 = 100% and 0 = 0%)\n")

        self.age = int(input("What is your age in years? "))

        self.country = input("What country are you from? ")

        self.headshot_percentage = float(response["lifetime"]["Average Headshots %"]) / 100

        self.damage_per_round = int(input("How much damage do you deal per round on average? (all weapons, guns and grenades included) "))

        self.grenade_damage_per_round = float(input("What percentage of that damage is from grenades? (Input your answer as a decimal, 1.0 = 100% and 0 = 0%) ")) * self.damage_per_round

        self.maps_played = int(response["lifetime"]["Matches"])

        de_dust2 = self.findDust2(response)

        self.rounds_played = int(de_dust2["Rounds"]) * 16

        self.kills_per_death = int(de_dust2["Kills"]) / int(de_dust2["Deaths"])

        self.kills_per_round = int(de_dust2["Kills"]) / self.rounds_played

        self.assists_per_round = int(de_dust2["Assists"]) / self.rounds_played

        self.deaths_per_round = int(de_dust2["Deaths"]) / self.rounds_played

        self.saved_teammates_per_round = float(input("How many of your teammates do you save in a match? ")) / 31

        self.saved_by_teammates_per_round = float(input("How many times are you saved by your teammates in a match? ")) / 31

        self.rounds_with_kills = float(input("What percentage of rounds do you get a kill on an enemy player? "))

        opening_kill_percentage = float(input("What percentage of rounds do you get the opening kill? (The very first kill of the round) "))

        self.opening_kill_ratio = opening_kill_percentage / float(input("What percentage of rounds are you the first member of your team to be killed? "))

        self.team_win_percent_after_first_kill = float(input("What percentage of rounds where you get the opening kill ends with your team winning that round? "))

        self.first_kill_in_won_rounds = opening_kill_percentage * self.team_win_percent_after_first_kill

        self.zero_kill_rounds = float(input("What percentage of rounds do you get zero kills? "))

        self.one_kill_rounds = float(input("What percentage of rounds do you get one kills? "))

        self.two_kill_rounds = float(input("What percentage of rounds do you get two kills? "))

        self.three_kill_rounds = float(de_dust2["Triple Kills"]) * 16 / self.rounds_played

        self.four_kill_rounds = float(de_dust2["Quadro Kills"]) * 16 / self.rounds_played

        self.five_kill_rounds = float(de_dust2["Penta Kills"]) * 16 / self.rounds_played

        print()

        print("Next, we will be asking for kill statistics on a variety of weapons (rifles, snipers, smgs, pistols, grenades, and all others like knife kills, for the next 6 questions the sum of all of your answers must be 1.0\n")

        self.rifle_kills = float(input("What is the percentage of kills you obtain with rifles? "))

        self.sniper_kills = float(input("What is the percentage of kills you obtain with snipers? "))

        self.smg_kills = float(input("What is the percentage of kills you obtain with SMGs? "))

        self.pistol_kills = float(input("What is the percentage of kills you obtain with pistols? "))

        self.grenade_kills = float(input("What is the percentage of kills you obtain with grenades? "))

        self.other_kills = float(input("What is the percentage of kills you obtain with all other weapons? (knife kills, etc.) "))

        print("Thank you for the information :)\n");

    def findDust2(self, response):
        for i in range(16):
            if (response["segments"][i]["label"] == "de_dust2"):
                return response["segments"][i]["stats"]
        
        print("Unable to find Dust2 in your maps list, unexpected error, exitting program")
        exit(0)

    def printData(self):
        print(f"age = {self.age}")
        print(f"country = {self.country}")
        print(f"headshot_percentage = {self.headshot_percentage}")
        print(f"damage_per_round = {self.damage_per_round}")
        print(f"grenade_damage_per_round = {self.grenade_damage_per_round}")
        print(f"maps_played = {self.maps_played}")
        print(f"rounds_played = {self.rounds_played}")
        print(f"kills_per_death = {self.kills_per_death}")
        print(f"kills_per_round = {self.kills_per_round}")
        print(f"assists_per_round = {self.assists_per_round}")
        print(f"deaths_per_round = {self.deaths_per_round}")
        print(f"saved_teammates_per_round = {self.saved_teammates_per_round}")
        print(f"saved_by_teammates_per_round = {self.saved_by_teammates_per_round}")
        print(f"rounds_with_kills = {self.rounds_with_kills}")
        print(f"opening_kill_ratio = {self.opening_kill_ratio}")
        print(f"team_win_percent_after_first_kill = {self.team_win_percent_after_first_kill}")
        print(f"first_kill_in_won_rounds = {self.first_kill_in_won_rounds}")
        print(f"zero_kill_rounds = {self.zero_kill_rounds}")
        print(f"one_kill_rounds = {self.one_kill_rounds}")
        print(f"two_kill_rounds = {self.two_kill_rounds}")
        print(f"three_kill_rounds = {self.three_kill_rounds}")
        print(f"four_kill_rounds = {self.four_kill_rounds}")
        print(f"five_kill_rounds = {self.five_kill_rounds}")
        print(f"rifle_kills = {self.rifle_kills}")
        print(f"sniper_kills = {self.sniper_kills}")
        print(f"smg_kills = {self.smg_kills}")
        print(f"pistol_kills = {self.pistol_kills}")
        print(f"grenade_kills = {self.grenade_kills}")
        print(f"other_kills = {self.other_kills}")

# Function to get player_id
def get_player_id(nickname):
    url = BASE_URL + f'players?nickname={nickname}&game=csgo&game_player_id={nickname}'
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    response = requests.get(url, headers  =headers)

    if (response.status_code == 200):
        return response.json()["player_id"]
    else:
        print(f"Failed to retrieve player_id from nickname: {response.status_code}")
        return None

def get_player_stats(player_id):
    url = BASE_URL + f'players/{player_id}/stats/csgo'
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    # print(url)

    response = requests.get(url, headers = headers)

    if (response.status_code == 200):
        return response.json()
    else:
        print(f'Failed to retrieve player stats from player_id: {response.status_code}')
        return None

# Example player ID
player_nickname = 'petr1k'

# Get player_id
player_id = get_player_id(player_nickname)

if player_id:
    print(player_id)
else:
    print("Failed to retrieve player statistics.")
    exit(0)

# Get player stats
player_stats = get_player_stats(player_id)

if (player_stats):
    print("Player Stats Obtained :)\n")
    # print(player_stats)
else:
    print("Failed to retrieve player statistics.")
    exit(0)

# Consolidate API data into Player_Stats Class
csgo_model_stats = Player_Stats(player_stats)

# Print data to the console for testing
csgo_model_stats.printData()

