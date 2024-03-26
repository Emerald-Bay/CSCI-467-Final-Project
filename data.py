import pandas as pd

#data frame ("path_to_file") 
#skipping header rows !!CHANGE "CSGO_PLAYERS.CSV TO YOUR PATH"
df = pd.read_csv("csgo_players.csv", skiprows=0, header=2)

#remove unneeded col's (stats)
cols_Remove = [0, 1, 2, 5, 6, 7, 8, 21, 22, 23, 25]
df = df.drop(df.columns[cols_Remove], axis=1)

#divide specific stats by rounds for normalization
cols_label_Divide = ["0_kill_rounds", "1_kill_rounds", "2_kill_rounds", "3_kill_rounds", "4_kill_rounds", "5_kill_rounds", "rifle_kills", "sniper_kills", "smg_kills", "pistol_kills", "grenade_kills", "other_kills"]

#Iterate over the columns and perform division
for col in cols_label_Divide:
    df[col] = df[col] / df["rounds_played"]
   
print(df.iloc[0])