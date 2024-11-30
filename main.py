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


Make it home & away color scheme with light and dark mode?
"""

# Imports
import customtkinter as ctk
import requests


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

# Classes
class GUI():
    def __init__(self):
      
        # Creates Window
        self.root = ctk.CTk()
        self.root.title("Packer Stats")
        self.root.geometry("1280x720")


        # Configure GUI's grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure((2, 3), weight=0) # Doesn't do anything?
        self.root.grid_rowconfigure((0, 1), weight=1)

        # Creates sidebar with category buttons and an appearance mode menu
        self.sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Packer Stats", text_color="#FFB612", font=ctk.CTkFont(size=30, weight="bold", underline=True))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Categories:", font=ctk.CTkFont(size=25))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(5, 10))

        self.offense_button = ctk.CTkButton(self.sidebar_frame, text="Offense", fg_color="#203731", font=ctk.CTkFont(size=20), command=offense.o_players)
        self.offense_button.grid(row=2, column=0, padx=20, pady=10)

        self.defense_button = ctk.CTkButton(self.sidebar_frame, text="Defense", fg_color="#203731", font=ctk.CTkFont(size=20), command=defense.d_players)
        self.defense_button.grid(row=3, column=0, padx=20, pady=10)

        self.spt_button = ctk.CTkButton(self.sidebar_frame, text="Special Teams", fg_color="#203731", font=ctk.CTkFont(size=20), command=sp_teams.sp_players)
        self.spt_button.grid(row=4, column=0, padx=20, pady=10)
        
        self.coaches_button = ctk.CTkButton(self.sidebar_frame, text="Coaching Staff", fg_color="#203731", font=ctk.CTkFont(size=20), command=coaches.coaching_staff)
        self.coaches_button.grid(row=5, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))


        self.root.mainloop()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
    



class Green_Bay_Packers(GUI):
    pass

class coaches(Green_Bay_Packers):
    def coaching_staff():
        print("Coaching Staff: ")

class offense(Green_Bay_Packers):
    def o_players():
        players = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1" and name["position"]["name"] in 
                   ["Quarterback", "Offensive Tackle", "Guard", "Center", "Wide Receiver", "Running Back", "Tight End"]}
        
        for value in players.values():
            print(value) 

        # print([value for value in players.values()]) # Could use list comprehension as well

class defense(Green_Bay_Packers):
    def d_players():
        players = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1" and name["position"]["name"] in 
                   ["Linebacker", "Cornerback", "Defensive Tackle", "Defensive End", "Safety"]}
        
        for value in players.values():
            print(value)

        # print([value for value in players.values()]) # Could use list comprehension as well
        
    def cornerback():
        pass

class sp_teams(Green_Bay_Packers):
    def sp_players():
        players = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1" and name["position"]["name"] in 
                   ["Place kicker", "Punter", "Long Snapper"]}
        
        for value in players.values():
            print(value)

        # print([value for value in players.values()]) # Could use list comprehension as well



# Data Fetching Sites
Ja_Stats = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/teams/9/athletes/3895429/statistics?lang=en&region=us"
players = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/9?enable=roster,projection,stats"

# Accesses ESPN API website for individual stats & team information.
# r = requests.get(Ja_Stats)

r2 = requests.get(players)
print(r2.status_code)

data = r2.json()["team"]["athletes"] # VERY IMPORTANT accesses 'athletes' sub information within team info.

# Dictionary comprehension detailing id and fullName for players IF they're on 52 man roster.
# athletes = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1"}
# corners = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1" and name["position"]["name"] == "Cornerback"} # Example how to access position grups
# print(corners)
# print(athletes)

# positions = {name["position"]["name"] for name in data if name["status"]["id"] == "1"}
# print(positions)


# with open("json_data.json", "wt") as data_file: 
#     # Probably temporary, wanted to make sure ALL the data was pulled correctly.
#     for line in r2.text:
#         data_file.write(line)




if __name__ == "__main__":
    GUI() 