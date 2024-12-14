"""
Author: Neal Vander Does
Date: 12/1/2024
Title: SDEV 220 Final Project: Packer Stats
Class: SDEV220-50P-IO-202420-I-82X
Desc: 
"""

"""
Ideas:

Player information comes from clickable button.


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
        self.root.grid_rowconfigure((0, 1, 2), weight=1)

        # Creates sidebar with category buttons and an appearance mode selector
        self.sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Packer Stats", text_color="#FFB612", font=ctk.CTkFont(size=30, weight="bold", underline=True))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Categories:", font=ctk.CTkFont(size=25))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(5, 10))

        self.offense_button = ctk.CTkButton(self.sidebar_frame, text="Offense", fg_color="#203731", font=ctk.CTkFont(size=20), command=self.o_positions)
        self.offense_button.grid(row=2, column=0, padx=20, pady=10)

        self.defense_button = ctk.CTkButton(self.sidebar_frame, text="Defense", fg_color="#203731", font=ctk.CTkFont(size=20), command=self.d_positions)
        self.defense_button.grid(row=3, column=0, padx=20, pady=10)

        self.spt_button = ctk.CTkButton(self.sidebar_frame, text="Special Teams", fg_color="#203731", font=ctk.CTkFont(size=20), command=self.sp_positions)
        self.spt_button.grid(row=4, column=0, padx=20, pady=10)
        
        # Appearance mode selector
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))

        # Segmented Button config
        self.frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frame.grid(row=0, column=1, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure((1, 2, 3), weight=1)

        self.seg_button = ctk.CTkSegmentedButton(self.frame, state="disabled", fg_color= "#FFB612", selected_color="#203731", font=ctk.CTkFont(size=20, weight="bold"))
        self.seg_button.grid(row=0, column=0, padx=(20, 10), pady=(20, 0))
        self.seg_button.configure(values=["Select a category on the left"])

        # Textbox for stat info
        self.textbox = ctk.CTkTextbox(self.root, state="disabled", font=ctk.CTkFont(size=20))  # State breaks the default text
        self.textbox.grid(row=0, rowspan=3, column=1, padx=(20, 15), pady=(75, 15), sticky="nsew")

        # Starts the GUI
        self.root.mainloop()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
    
    # Each function creates buttons in the GUI's segmented button
    def o_positions(self):
        self.seg_button.configure(values=["Quarterback", "Offensive Tackle", "Guard", "Center", "Wide Receiver", "Running Back", "Tight End"], state="normal", command=self.o_seg_value)

    def d_positions(self):
        self.seg_button.configure(values=["Linebacker", "Cornerback", "Defensive Tackle", "Defensive End", "Safety"], state="normal", command=self.d_seg_value)

    def sp_positions(self):
        self.seg_button.configure(values=["Place Kicker", "Punter", "Long Snapper"], state="normal", command=self.sp_seg_value)

    # Each function gets the exact name of the button pressed in the segmented button in order to pull that groups stats 
    def o_seg_value(self, pos_name):
        self.seg_value = pos_name
        offense.o_players(self)
        return self.seg_value
    
    def d_seg_value(self, pos_name):
        self.seg_value = pos_name
        defense.d_players(self)
        return self.seg_value
    
    def sp_seg_value(self, pos_name):
        self.seg_value = pos_name
        sp_teams.sp_players(self)
        return self.seg_value
        
# Stat pulling
class stats(GUI):
    def offense_stats(self):      
        # Filter for each offensive position groups stats (all but one oline stat is 0 so I didn't include them)
        qb_stats = ["Games Plaed", "Completion Percentage", "Completions", "Interceptions", "Passing Touchdowns", "Passing Yards", "Total Sacks", 
                        "Games Played", "Total Touchdowns", "Total Yards", "Yards Per Game", "Adjusted QBR"]
        wr_te_stats = ["Games Played", "Long Reception", "Receiving First Downs", "Receiving Fumbles", "Receptions", "Total Touchdowns", "Receiving Yards", "Yards Per Game"]
        rb_stats = ["Average Gain", "Long Rushing", "Rushing Yards", "Yards Per Game", "Rushing Attempts", "Rushing Fumbles", "Rushing Touchdowns", "Games Played"]
        oline_stats = ["Games Played"]
        
        # Create a dictionary to store stats for each player
        player_stats = {}

        # Creates a link for every individual player in a position group and pulls some stats
        web_format = map(lambda num: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/teams/9/athletes/{num}/statistics", self.players.keys())
        for link in web_format:
            test_stats = requests.get(link)

            if test_stats.status_code == 200: # Checks if the website call went well
                test_stats_data = test_stats.json()["splits"]["categories"]
                if self.seg_value == "Quarterback":
                    filtered_stats = {nstat["displayName"]:nstat["displayValue"] for stat in test_stats_data if stat["name"] 
                                      == "general" or "passing" for nstat in stat["stats"] if nstat["displayName"] in qb_stats}
                elif self.seg_value == "Wide Receiver":
                    filtered_stats = {nstat["displayName"]:nstat["displayValue"] for stat in test_stats_data if stat["name"] 
                                      == "general" or "receiving" for nstat in stat["stats"] if nstat["displayName"] in wr_te_stats}
                elif self.seg_value == "Running Back":
                    filtered_stats = {nstat["displayName"]:nstat["displayValue"] for stat in test_stats_data if stat["name"] 
                                      == "general" or "rushing" for nstat in stat["stats"] if nstat["displayName"] in rb_stats}
                elif self.seg_value == "Tight End":
                    filtered_stats = {nstat["displayName"]:nstat["displayValue"] for stat in test_stats_data if stat["name"]
                                      == "general" or "receiving" for nstat in stat["stats"] if nstat["displayName"] in wr_te_stats}
                else: 
                    self.seg_value == "Offensive Tackle" or "Guard" or "Center"
                    filtered_stats = {nstat["displayName"]:nstat["displayValue"] for stat in test_stats_data if stat["name"]
                                      == "general" for nstat in stat["stats"] if nstat["displayName"] in oline_stats}

            # Adds the pulled stats to the player_stats dictionary with their name and id
            player_name = self.players[link.split("/")[-2]] 
            player_stats[player_name] = filtered_stats
        return player_stats
    
    def defense_stats(self):
        # Filter for each defensive position groups stats
        lb_stats = ["Forced Fumbles", "Fumbles Recovered", "Interceptions", "Passes Defended", "Quarterback Hits", "Sacks", 
                        "Games Played", "Stuffs", "Tackles For Loss", "Yards Per Game", "Total Tackles"]
        cb_sfty_stats = ["Interceptions", "Passes Defended", "Sacks", "Solo Tackles", "Games Played"]
        dt_de_stats = ["Quarterback Hits", "Sacks", "Hurries", "Stuffs", "Tackles For Loss", "Total Tackles", "Forced Fumbles", "Fumbles Recovered", "Games Played"]
        
        # Create a dictionary to store stats for each player
        player_stats = {}

        # Creates a link for every individual player in a position group and pulls some stats
        web_format = map(lambda num: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/teams/9/athletes/{num}/statistics", self.players.keys())
        for link in web_format:
            test_stats = requests.get(link)

            if test_stats.status_code == 200: # Checks if the website call went well
                test_stats_data = test_stats.json()["splits"]["categories"]
                if self.seg_value == "Linebacker":
                    filtered_stats = {nstat["displayName"]:nstat["displayValue"] for stat in test_stats_data if stat["name"] 
                                      == "general" or "defensive" or "defensiveInterceptions" for nstat in stat["stats"] if nstat["displayName"] in lb_stats}
                elif self.seg_value == "Cornerback":
                    filtered_stats = {nstat["displayName"]:nstat["displayValue"] for stat in test_stats_data if stat["name"] 
                                      == "general" or "defensive" or "defensiveInterceptions" for nstat in stat["stats"] if nstat["displayName"] in cb_sfty_stats}
                elif self.seg_value == "Safety":
                    filtered_stats = {nstat["displayName"]:nstat["displayValue"] for stat in test_stats_data if stat["name"] 
                                      == "general" or "defensive" or "defensiveInterceptions" for nstat in stat["stats"] if nstat["displayName"] in cb_sfty_stats}
                else: 
                    self.seg_value == "Defensive Tackle" or "Defensive End"
                    filtered_stats = {nstat["displayName"]:nstat["displayValue"] for stat in test_stats_data if stat["name"] 
                                      == "general" or "defensive" for nstat in stat["stats"] if nstat["displayName"] in dt_de_stats}

            # Adds the pulled stats to the player_stats dictionary with their name and id
            player_name = self.players[link.split("/")[-2]] 
            player_stats[player_name] = filtered_stats
        return player_stats
    
    def sp_stats(self):
        # Filter for each defensive position groups stats
        pkicker_stats = ["Games Played", "Average Kickoff Return Yards", "Average Kickoff Yards", "Extra Point Attempts", "Extra Point Percentage", "Extra Point Blocked", 
                         "Field Goal Attempts", "Field Goal Percentage", "Field Goals Blocked", "Long Field Goal Made"]
        punter_stats = ["Games Played", "Punts", "Average Punt Return Yards", "Gross Average Punt Yards", "Long Punt", "Punt Returns", "Punt Return Yards", "Punts Blocked",
                        "Punts Inside 10", "Punts Inside 20", "Punt Yards", "Touchbacks"]
        lsnapper_stats = ["Games Played"]
        
        
        # Create a dictionary to store stats for each player
        player_stats = {}

        # Creates a link for every individual player in a position group and pulls some stats
        web_format = map(lambda num: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/teams/9/athletes/{num}/statistics", self.players.keys())
        for link in web_format:
            test_stats = requests.get(link)

            if test_stats.status_code == 200: # Checks if the website call went well
                test_stats_data = test_stats.json()["splits"]["categories"]
                if self.seg_value == "Place Kicker":
                    filtered_stats = {nstat["displayName"]:nstat["displayValue"] for stat in test_stats_data if stat["name"] 
                                      == "general" or "kicking" for nstat in stat["stats"] if nstat["displayName"] in pkicker_stats}
                elif self.seg_value == "Punter":
                    filtered_stats = {nstat["displayName"]:nstat["displayValue"] for stat in test_stats_data if stat["name"] 
                                      == "general" or "punting" for nstat in stat["stats"] if nstat["displayName"] in punter_stats}
                else: 
                    self.seg_value == "Long Snapper"
                    filtered_stats = {nstat["displayName"]:nstat["displayValue"] for stat in test_stats_data if stat["name"] 
                                      == "general" for nstat in stat["stats"] if nstat["displayName"] in lsnapper_stats}

            # Adds the pulled stats to the player_stats dictionary with their name and id
            player_name = self.players[link.split("/")[-2]] 
            player_stats[player_name] = filtered_stats
        return player_stats
    
class offense(GUI):
    def o_players(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.players = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1" and name["position"]["name"] == self.seg_value}

        # Gets player stats
        player_stats = stats.offense_stats(self)

        # Displays player stats in the GUI textbox
        for player_name, statistics in player_stats.items():
            self.textbox.insert("end", f"{player_name}:\n")
            for stat_name, stat_value in statistics.items():
                self.textbox.insert("end", f" • {stat_name}: {stat_value}\n")

        self.textbox.configure(state="disabled")
    
class defense(GUI):
    def d_players(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.players = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1" and name["position"]["name"] == self.seg_value}

        # Gets player stats
        player_stats = stats.defense_stats(self)

        # Displays player stats in the GUI textbox
        for player_name, statistics in player_stats.items():
            self.textbox.insert("end", f"{player_name}:\n")
            for stat_name, stat_value in statistics.items():
                self.textbox.insert("end", f" • {stat_name}: {stat_value}\n")

        self.textbox.configure(state="disabled")

class sp_teams(GUI):
    def sp_players(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.players = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1" and name["position"]["displayName"] == self.seg_value}

        # Gets player stats
        player_stats = stats.sp_stats(self)

        # Displays player stats in the GUI textbox
        for player_name, statistics in player_stats.items():
            self.textbox.insert("end", f"{player_name}:\n")
            for stat_name, stat_value in statistics.items():
                self.textbox.insert("end", f" • {stat_name}: {stat_value}\n")

        self.textbox.configure(state="disabled")   

# Calls the website and pulls data for every player on the 53 man roster
players = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/9?enable=roster,projection,stats"

req = requests.get(players)

data = req.json()["team"]["athletes"] # VERY IMPORTANT accesses 'athletes' sub information within team info.

if __name__ == "__main__":
    GUI() # Calls GUI Class