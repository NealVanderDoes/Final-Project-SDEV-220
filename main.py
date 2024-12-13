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
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

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
        
        self.coaches_button = ctk.CTkButton(self.sidebar_frame, text="Coaching Staff", fg_color="#203731", font=ctk.CTkFont(size=20), command=self.coaches_positions)
        self.coaches_button.grid(row=5, column=0, padx=20, pady=10)
        
        # Appearance mode selector
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        # Segmented Button config
        self.frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frame.grid(row=0, column=1, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure((1, 2, 3), weight=1)

        self.seg_button = ctk.CTkSegmentedButton(self.frame, state="disabled", fg_color= "#FFB612", selected_color="#203731", font=ctk.CTkFont(size=20, weight="bold"))
        self.seg_button.grid(row=0, column=0, padx=(20, 10), pady=(20, 0))
        self.seg_button.configure(values=["Select a category on the left"])

        # Textbox for stat info
        self.textbox = ctk.CTkTextbox(self.root, state="disabled", font=ctk.CTkFont(size=35))  # State breaks the default text
        self.textbox.grid(row=0, rowspan=3, column=1, padx=(20, 15), pady=(75, 15), sticky="nsew")

        # Starts the GUI
        self.root.mainloop()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
    
    def o_positions(self):
        self.seg_button.configure(values=["Quarterback", "Offensive Tackle", "Guard", "Center", "Wide Receiver", "Running Back", "Tight End"], state="normal", command=self.get_seg_value)

    def d_positions(self):
        self.seg_button.set(value="Linebacker")
        self.seg_button.configure(values=["Linebacker", "Cornerback", "Defensive Tackle", "Defensive End", "Safety"], state="normal", command="")

    def sp_positions(self):
        self.seg_button.set(value="Place Kicker")
        self.seg_button.configure(values=["Place Kicker", "Punter", "Long Snapper"], state="normal", command="")

    def coaches_positions(self):
        self.seg_button.set(value="Temp")
        self.seg_button.configure(values=["temporary value"], state="normal", command="")

    def get_seg_value(self, pos_name):
        self.seg_value = pos_name
        offense.o_players(self)
        return self.seg_value
    
    # def update_textbox(self): # Possibly unnecessary
    #     self.textbox.delete("0.0", "end")
    #     self.textbox.insert("0.0", id_name)
    
# Stat pulling
class offense(GUI):
    def o_players(self):

        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        players = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1" and name["position"]["name"] == self.seg_value} # Accesses ID's and Names

        id = [name["id"] for name in data if name["status"]["id"] == "1" and name["position"]["name"] == self.seg_value] # Just accesses ID's so I can create a format to scan many API links
        print(id)

        for id_name in id:
            self.textbox.insert("0.0", f"{id_name}\n")
        self.textbox.configure(state="disabled")
# Maybe use lambda for accessesing API with format?


# class defense(GUI):
#     def d_players_stats(self):

#         players = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1" and name["position"]["name"] in 
#                    ["Linebacker", "Cornerback", "Defensive Tackle", "Defensive End", "Safety"]}
        
#         for value in players.values():
#             print(value)


#         # print([value for value in players.values()]) # Could use list comprehension as well
        
#     def cornerback():
#         pass

# class sp_teams(GUI):
#     def sp_players():
#         players = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1" and name["position"]["name"] in 
#                    ["Place kicker", "Punter", "Long Snapper"]}
        
#         for value in players.values():
#             print(value)

#         # print([value for value in players.values()]) # Could use list comprehension as well

# class coaches(GUI):
#     def coaching_staff():
#         print("Coaching Staff: ")


# # Data Fetching Sites
# Ja_Stats = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/teams/9/athletes/3895429/statistics?lang=en&region=us"
players = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/9?enable=roster,projection,stats"

# # Accesses ESPN API website for individual stats & team information.
# # r = requests.get(Ja_Stats)

r2 = requests.get(players)
print(r2.status_code)

data = r2.json()["team"]["athletes"] # VERY IMPORTANT accesses 'athletes' sub information within team info.

# # # Dictionary comprehension detailing id and fullName for players IF they're on 52 man roster.
# # athletes = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1"}
# # corners = {name["id"]:name["fullName"] for name in data if name["status"]["id"] == "1" and name["position"]["name"] == "Cornerback"} # Example how to access position grups
# # print(corners)
# # print(athletes)

# # positions = {name["position"]["name"] for name in data if name["status"]["id"] == "1"}
# # print(positions)


# # with open("json_data.json", "wt") as data_file: 
# #     # Probably temporary, wanted to make sure ALL the data was pulled correctly.
# #     for line in r2.text:
# #         data_file.write(line)




if __name__ == "__main__":
    GUI() # Calls GUI Class