import pandas as pd
import numpy as np
from unidecode import unidecode

# <ADD ABBR TEAM NAMES>

column_names = ['team_name', 'opp_name', 'team_score', 'opp_score', 'team_roster', 'opp_roster', 'team_hrefs', 'opp_hrefs']
df_lineups = pd.read_csv('all-game-lineups.csv', comment='#', names=column_names)

df_team_names = pd.read_csv('team-names.csv', comment='#', names=['long','short'])

team_abbr = []
opp_abbr = []
err_count = 0

for index, row in df_lineups.iterrows():
    team_index = df_team_names[df_team_names['long']==row['team_name']].index.values[0]
    opp_index = df_team_names[df_team_names['long']==row['opp_name']].index.values[0]

    if(team_index > -1 and opp_index > -1):
        team_abbr.append(df_team_names.short[team_index])
        opp_abbr.append(df_team_names.short[opp_index])
    else:
        err_count += 1
        print(f"Team name not found. Index: {index}")

print(f"ERROR COUNT: {err_count}")


if (err_count == 0 and len(team_abbr) == len(df_lineups.team_name) and len(opp_abbr) == len(df_lineups.opp_name)):
    df_lineups.drop(columns=['team_hrefs', 'opp_hrefs'], inplace=True)
    df_lineups['team_abbr'] = team_abbr
    df_lineups['opp_abbr'] = opp_abbr
    df_lineups.to_csv('temp1.csv', index=False, header=False)

# </ADD ABBR TEAM NAMES>

# <ADD PLAYER OFFENSIVE STATS>

lineup_col_names = ['team_name', 'opp_name', 'team_score', 'opp_score', 'team_roster', 'opp_roster', 'team_abbr', 'opp_abbr']
df_lineups = pd.read_csv('all-game-lineups-abbr.csv', comment='#', names=lineup_col_names)

fielding_col_names = ['Tm','#Fld','RA/G','DefEff','G','GS','CG','Inn','Ch','PO','A','E','DP','Fld%','Rtot','Rtot/yr','Rdrs','Rdrs/yr','Rgood']
df_fielding_stats = pd.read_csv('all-team-fielding.csv', comment='#', names=fielding_col_names)

pitching_col_names = ['Tm','#P','PAge','RA/G','W','L','W-L%','ERA','G','GS','GF','CG','tSho','cSho','SV','IP','H','R','ER','HR','BB','IBB','SO','HBP','BK','WP','BF','ERA+','FIP','WHIP','H9','HR9','BB9','SO9','SO/W','LOB']
df_pitching_stats = pd.read_csv('all-team-pitching.csv', comment='#', names=pitching_col_names)

temp1_col_names = ['team_name','opp_name','team_score','opp_score','team_roster','opp_roster','team_abbr','opp_abbr','t_BA','t_OBP','t_SLG','t_OPS','t_OPSplus','t_GDP','t_HBP','t_SH','t_SF','t_IBB']
df_temp1 = pd.read_csv('temp1.csv', comment='#', names=temp1_col_names)


batting_col_names = ['Rk','Name','Age','Tm','Lg','G','PA','AB','R','H','2B','3B','HR','RBI','SB','CS','BB','SO','BA','OBP','SLG','OPS','OPSplus','TB','GDP','HBP','SH','SF','IBB','Pos Summary']
df_batting_stats = pd.read_csv('all-player-batting.csv', comment='#', names=batting_col_names)

err_count = 0
all_player_BA = []
all_player_OBP = []
all_player_SLG = []
all_player_OPS = []
all_player_OPS_plus = []
all_player_GDP = []
all_player_HBP = []
all_player_SH = []
all_player_SF = []
all_player_IBB = []

blank_players = []

for index, row in df_temp1.iterrows():

    str1 = row['opp_roster'].replace(']','').replace('[','').replace("'",'')
    team_roster = str1.replace('"','').split(",")
    
    player_BA = []
    player_OBP = []
    player_SLG = []
    player_OPS = []
    player_OPS_plus = []
    player_GDP = []
    player_HBP = []
    player_SH = []
    player_SF = []
    player_IBB = []
    for i in range(len(team_roster)):
        player_stat_index = -1
        for stat_index, stat_row in df_batting_stats.iterrows():
            player_name = unidecode(team_roster[i].replace('-',' ').replace('.','').replace("'",''))
            if(player_name[0] == ' '):
                player_name = player_name[1:]
            
            if(player_name in unidecode(stat_row['Name'].replace('-',' ').replace('.','').replace("'",''))):
                player_stat_index = stat_index
                if(player_stat_index > -1):
                    player_BA.append(df_batting_stats.BA[player_stat_index])
                    player_OBP.append(df_batting_stats.OBP[player_stat_index])
                    player_SLG.append(df_batting_stats.SLG[player_stat_index])
                    player_OPS.append(df_batting_stats.OPS[player_stat_index])
                    player_OPS_plus.append(df_batting_stats.OPSplus[player_stat_index])
                    player_GDP.append(df_batting_stats.GDP[player_stat_index])
                    player_HBP.append(df_batting_stats.HBP[player_stat_index])
                    player_SH.append(df_batting_stats.SH[player_stat_index])
                    player_SF.append(df_batting_stats.SF[player_stat_index])
                    player_IBB.append(df_batting_stats.IBB[player_stat_index])
                    break

        if(player_stat_index == -1):
            err_count += 1
            print(f"Player name not found in stats: {player_name}")
            blank_players.append(player_name)
            player_BA.append(0)
            player_OBP.append(0)
            player_SLG.append(0)
            player_OPS.append(0)
            player_OPS_plus.append(0)
            player_GDP.append(0)
            player_HBP.append(0)
            player_SH.append(0)
            player_SF.append(0)
            player_IBB.append(0)

    all_player_BA.append(player_BA)
    all_player_OBP.append(player_OBP)
    all_player_SLG.append(player_SLG)
    all_player_OPS.append(player_OPS)
    all_player_OPS_plus.append(player_OPS_plus)
    all_player_GDP.append(player_GDP)
    all_player_HBP.append(player_HBP)
    all_player_SH.append(player_SH)
    all_player_SF.append(player_SF)
    all_player_IBB.append(player_IBB)
    print(index)

# print(f"all_player_BA: {all_player_BA[:5]}")
print("DONE")

df_temp1['BA'] = all_player_BA
df_temp1['OBP'] = all_player_OBP
df_temp1['OPS'] = all_player_OPS
df_temp1['OPSplus'] = all_player_OPS_plus
df_temp1['GDP'] = all_player_GDP
df_temp1['HBP'] = all_player_HBP
df_temp1['SH'] = all_player_SH
df_temp1['SF'] = all_player_SF
df_temp1['IBB'] = all_player_IBB

df_temp1.to_csv('temp2.csv', index=False, header=False)

# </ADD PLAYER OFFENSIVE STATS>


# <ADD TEAM DEFENSIVE STATS>
temp2_col_names = ['team_name','opp_name','team_score','opp_score','team_roster','opp_roster','team_abbr','opp_abbr','t_BA','t_OBP','t_SLG','t_OPS','t_OPSplus','t_GDP','t_HBP','t_SH','t_SF','o_BA','o_OBP','o_SLG','o_OPS','o_OPSplus','o_GDP','o_HBP','o_SH','o_SF']
df_temp2 = pd.read_csv('temp2.csv', comment='#', names=temp2_col_names)

fielding_col_names = ['Tm','#Fld','RA/G','DefEff','G','GS','CG','Inn','Ch','PO','A','E','DP','Fld%','Rtot','Rtot/yr','Rdrs','Rdrs/yr','Rgood']
df_fielding_stats = pd.read_csv('all-team-fielding.csv', comment='#', names=fielding_col_names)

pitching_col_names = ['Tm','#P','PAge','RA/G','W','L','W-L%','ERA','G','GS','GF','CG','tSho','cSho','SV','IP','H','R','ER','HR','BB','IBB','SO','HBP','BK','WP','BF','ERA+','FIP','WHIP','H9','HR9','BB9','SO9','SO/W','LOB']
df_pitching_stats = pd.read_csv('all-team-pitching.csv', comment='#', names=pitching_col_names)

all_team_RA_per_G = []
all_team_ERA = []
all_opp_RA_per_G = []
all_opp_ERA = []
for index, row in df_temp2.iterrows():
    for pitch_index, pitch_row in df_pitching_stats.iterrows():
        if(row['team_abbr'] == pitch_row['Tm']):
            all_team_RA_per_G.append(pitch_row['RA/G'])
            all_team_ERA.append(pitch_row['ERA'])
        elif(row['opp_abbr'] == pitch_row['Tm']):
            all_opp_RA_per_G.append(pitch_row['RA/G'])
            all_opp_ERA.append(pitch_row['ERA'])
    print(index)

df_temp2['tm_RA/G'] = all_team_RA_per_G
df_temp2['tm_ERA'] = all_team_ERA
df_temp2['opp_RA/G'] = all_opp_RA_per_G
df_temp2['opp_ERA'] = all_opp_ERA

df_temp2.to_csv('temp3.csv', index=False)
# </ADD TEAM DEFENSIVE STATS>

# <SEPARATE TEAMS FROM OPPS>

temp3_col_names = ['team_name','opp_name','team_score','opp_score','team_roster','opp_roster','team_abbr','opp_abbr','t_BA','t_OBP','t_SLG','t_OPS','t_OPSplus','t_GDP','t_HBP','t_SH','t_SF','o_BA','o_OBP','o_SLG','o_OPS','o_OPSplus','o_GDP','o_HBP','o_SH','o_SF','tm_RA/G','tm_ERA','opp_RA/G','opp_ERA']
df_temp3 = pd.read_csv('temp3.csv', comment='#', names=temp3_col_names)

temp4_col_names = ['team_name','score','roster','abbr','t_BA','t_OBP','t_SLG','t_OPS','t_OPSplus','t_GDP','t_HBP','t_SH','t_SF','tm_RA/G','tm_ERA']
df_temp4 = pd.DataFrame(columns=temp4_col_names)

team_names = []
scores = []
rosters = []
abbrs = []
t_BAs = []
t_OBPs = []
t_SLGs = []
t_OPSs = []
t_OPSpluses = []
t_GDPs = []
t_HBPs = []
t_SHs = []
t_SFs = []
tm_RA_per_Gs = []
tm_ERAs = []

for index, row in df_temp3.iterrows():
    team_names.append(row['team_name'])
    scores.append(row['team_score'])
    rosters.append(row['team_roster'])
    abbrs.append(row['team_abbr'])
    t_BAs.append(row['t_BA'])
    t_OBPs.append(row['t_OBP'])
    t_SLGs.append(row['t_SLG'])
    t_OPSs.append(row['t_OPS'])
    t_OPSpluses.append(row['t_OPSplus'])
    t_GDPs.append(row['t_GDP'])
    t_HBPs.append(row['t_HBP'])
    t_SHs.append(row['t_SH'])
    t_SFs.append(row['t_SF'])
    tm_RA_per_Gs.append(row['tm_RA/G'])
    tm_ERAs.append(row['tm_ERA'])

    team_names.append(row['opp_name'])
    scores.append(row['opp_score'])
    rosters.append(row['opp_roster'])
    abbrs.append(row['opp_abbr'])
    t_BAs.append(row['o_BA'])
    t_OBPs.append(row['o_OBP'])
    t_SLGs.append(row['o_SLG'])
    t_OPSs.append(row['o_OPS'])
    t_OPSpluses.append(row['o_OPSplus'])
    t_GDPs.append(row['o_GDP'])
    t_HBPs.append(row['o_HBP'])
    t_SHs.append(row['o_SH'])
    t_SFs.append(row['o_SF'])
    tm_RA_per_Gs.append(row['opp_RA/G'])
    tm_ERAs.append(row['opp_ERA'])

df_temp4['team_name'] = team_names
df_temp4['score'] = scores
df_temp4['roster'] = rosters
df_temp4['abbr'] = abbrs
df_temp4['t_BA'] = t_BAs
df_temp4['t_OBP'] = t_OBPs
df_temp4['t_SLG'] = t_SLGs
df_temp4['t_OPS'] = t_OPSs
df_temp4['t_OPSplus'] = t_OPSpluses
df_temp4['t_GDP'] = t_GDPs
df_temp4['t_HBP'] = t_HBPs
df_temp4['t_SH'] = t_SHs
df_temp4['t_SF'] = t_SFs
df_temp4['tm_RA/G'] = tm_RA_per_Gs
df_temp4['tm_ERA'] = tm_ERAs

print(df_temp4.iloc[:5])

df_temp4.to_csv('temp4.csv', index=False)

# <SEPARATE ALL GAMES INTO 2 COLUMNS>

temp4_col_names = ['team_name','score','roster','abbr','t_BA','t_OBP','t_SLG','t_OPS','t_OPSplus','t_GDP','t_HBP','t_SH','t_SF','tm_RA/G','tm_ERA']
df_temp4 = pd.read_csv('temp4.csv', comment='#', names=temp4_col_names)

all_x = []
all_y = []

for index, row in df_temp4.iterrows():

    temp_x = []

    str1 = row['t_BA'].replace(']','').replace('[','').replace("'",'')
    t_BA = str1.replace('"','').split(",")
    for i in range(len(t_BA)):
        temp_x.append(t_BA[i])

    str1 = row['t_OBP'].replace(']','').replace('[','').replace("'",'')
    t_OBP = str1.replace('"','').split(",")
    for i in range(len(t_OBP)):
        temp_x.append(t_OBP[i])
    
    str1 = row['t_SLG'].replace(']','').replace('[','').replace("'",'')
    t_SLG = str1.replace('"','').split(",")
    for i in range(len(t_SLG)):
        temp_x.append(t_SLG[i])

    str1 = row['t_OPS'].replace(']','').replace('[','').replace("'",'')
    t_OPS = str1.replace('"','').split(",")
    for i in range(len(t_OPS)):
        temp_x.append(t_OPS[i])

    str1 = row['t_OPSplus'].replace(']','').replace('[','').replace("'",'')
    t_OPSplus = str1.replace('"','').split(",")
    for i in range(len(t_OPSplus)):
        temp_x.append(t_OPSplus[i])

    str1 = row['t_GDP'].replace(']','').replace('[','').replace("'",'')
    t_GDP = str1.replace('"','').split(",")   
    for i in range(len(t_GDP)):
        temp_x.append(t_GDP[i])

    str1 = row['t_HBP'].replace(']','').replace('[','').replace("'",'')
    t_HBP = str1.replace('"','').split(",")  
    for i in range(len(t_HBP)):
        temp_x.append(t_HBP[i])
    
    str1 = row['t_SH'].replace(']','').replace('[','').replace("'",'')
    t_SH = str1.replace('"','').split(",")  
    for i in range(len(t_SH)):
        temp_x.append(t_SH[i])

    str1 = row['t_SF'].replace(']','').replace('[','').replace("'",'')
    t_SF = str1.replace('"','').split(",") 
    for i in range(len(t_SF)):
        temp_x.append(t_SF[i])
    
    temp_x.append(row['tm_RA/G'])
    temp_x.append(row['tm_ERA'])

    print(index)
    all_x.append(temp_x)
    all_y.append(row['score'])

df_temp5 = pd.DataFrame(columns=['x','y'])
df_temp5['x'] = all_x
df_temp5['y'] = all_y
df_temp5.to_csv('temp5.csv', index=False)
# <\SEPARATE ALL GAMES INTO 2 COLUMNS>

# <ENSURE ALL DATA IS IN READABLE FORMAT>
df_temp5 = pd.read_csv('temp5.csv', comment='#', names=['x','y'])

x = []
for x_in in df_temp5.x:
    temp_x = []
    str1 = x_in.replace(']','').replace('[','').replace("'",'')
    arr1 = str1.replace('"','').split(",")
    for a in arr1:
        temp_x.append(float(a))
    x.append(temp_x)

y = []
for y_in in df_temp5.y:
    y.append(float(y_in))

print(x[0])
print(x[0][0])
print(type(x[0][0]))

print(y[0])
print(type(y[0]))

df_temp5.x = x
df_temp5.y = y

# <\ENSURE ALL DATA IS IN READABLE FORMAT>