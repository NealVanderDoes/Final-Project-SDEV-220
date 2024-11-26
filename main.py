"""
Author: Neal Vander Does
Date: 11/22/2024
Title: SDEV 220 Final Project: 
Class: SDEV220-50P-IO-202420-I-82X
Desc: 
"""

"""
Ideas: Have Coaches, Offense, Defense, SP_Teams all be searchable with an Entry & search Button. 
Keywords will call the classes and display the results.

Player information comes from clickable button with their picture on it.
"""

# Imports
import customtkinter as ctk
import requests



# Classes
class GUI:
    def __init__(self):
        # Constructor creates GUI
        self.root = ctk.CTk()
        self.root.geometry("1280x720")


        self.root.mainloop()



class Green_Bay_Packers(GUI):
    pass
class coaches(Green_Bay_Packers):
    pass
class offense(Green_Bay_Packers):
    pass
class defense(Green_Bay_Packers):
    pass
class sp_teams(Green_Bay_Packers):
    pass


# Data Fetching Sites
Ja_Stats = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/teams/9/athletes/3895429/statistics?lang=en&region=us"
players = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/9?enable=roster,projection,stats"

# Accesses ESPN API website for individual stats & team information.
r = requests.get(Ja_Stats)

r2 = requests.get(players)
print(r2.status_code)

data = r2.json()["team"]["athletes"] # VERY IMPORTANT accesses 'athletes' sub information within team info.

# Dictionary comprehension detailing id and fullName for players IF they're on 52 man roster.
athletes = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1"}
print(athletes)




with open("json_data.json", "wt") as data_file: 
    # Probably temporary, wanted to make sure ALL the data was pulled correctly.
    for line in r2.text:
        data_file.write(line)



# GUI() # Disabled while figuring out API pulling for stats.