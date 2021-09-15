import pandas as pd

# <REMOVE EMPTY LINES>

# df = pd.read_csv('baseball-lineups.csv', encoding='latin-1')
# df.to_csv('all-game-lineups.csv', index=False)

# </REMOVE EMPTY LINES>


# <REMOVE INDEX COLUMN>

# column_names = ['index', 'team_name', 'opp_name', 'team_score', 'opp_score', 'team_roster', 'opp_roster', 'team_hrefs', 'opp_hrefs']
# df = pd.read_csv('all-game-lineups.csv', comment='#', names=column_names)
# df.drop(columns="index", inplace=True)
# df.to_csv('all-game-lineups.csv', index=False, header=False)

# </REMOVE INDEX COLUMN>


# <CHECK FOR DUPLICATE GAMES>

column_names = ['team_name', 'opp_name', 'team_score', 'opp_score', 'team_roster', 'opp_roster', 'team_hrefs', 'opp_hrefs']
df = pd.read_csv('all-game-lineups.csv', names=column_names)
for index1, row1 in df.iterrows():
    for index2, row2 in df.iterrows():
        if(index1 != index2 and row1['team_name'] == row2['team_name'] and row1['opp_name'] == row2['opp_name']):
            if(row1['team_score'] == row2['team_score'] and row1['opp_score'] == row2['opp_score']):
                if(abs(index1 - index2) < 3):   # Games close to each other with same score are probably duplicates
                    print(f"index1: {index1}")
                    print(f"index2: {index2}")
                    print(f"team: {row1['team_name']}, opp: {row1['opp_name']}")

# </CHECK FOR DUPLICATE GAMES>