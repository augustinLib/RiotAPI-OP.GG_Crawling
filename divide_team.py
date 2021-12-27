# %%
import pandas as pd
import numpy as np

# %%
match_data = pd.read_csv('/plat_final_added_score.csv')

# %%
match_data.drop('Unnamed: 0', axis=1, inplace=True)
match_data.drop('matchId', axis=1, inplace=True)

# %%
temp_df1 = match_data.copy()
temp_df2 = match_data.copy()

# %%
for playerNumber in range(1, 6):
    temp_df1.drop('t2_p%d_champion_name' % playerNumber, axis=1, inplace=True)
    temp_df1.drop('t2_p%d_summoner_name' % playerNumber, axis=1, inplace=True)
    temp_df1.drop('t2_p%d_teamPosition' % playerNumber, axis=1, inplace=True)
    temp_df1.drop('t2_p%d_kda' % playerNumber, axis=1, inplace=True)
    temp_df1.drop('t2_p%d_winRate' % playerNumber, axis=1, inplace=True)
    temp_df1.drop('t2_p%d_fiveGame_played' % playerNumber, axis=1, inplace=True)
    temp_df1.drop('t2_p%d_psScore' % playerNumber, axis=1, inplace=True)


# %%
for playerNumber in range(1, 6):
    temp_df1.drop('t1_p%d_summoner_name' % playerNumber, axis=1, inplace=True)


for playerNumber in range(1, 6):
    temp_df2.drop('t2_p%d_summoner_name' % playerNumber, axis=1, inplace=True)


# %%
for playerNumber in range(1, 6):
    temp_df2.drop('t1_p%d_champion_name' % playerNumber, axis=1, inplace=True)
    temp_df2.drop('t1_p%d_summoner_name' % playerNumber, axis=1, inplace=True)
    temp_df2.drop('t1_p%d_teamPosition' % playerNumber, axis=1, inplace=True)
    temp_df2.drop('t1_p%d_kda' % playerNumber, axis=1, inplace=True)
    temp_df2.drop('t1_p%d_winRate' % playerNumber, axis=1, inplace=True)
    temp_df2.drop('t1_p%d_fiveGame_played' % playerNumber, axis=1, inplace=True)
    temp_df2.drop('t1_p%d_psScore' % playerNumber, axis=1, inplace=True)

# %%
for i in range(0, len(temp_df2)):
    if temp_df2['t1_win'][i] == 1:
        temp_df2['t1_win'][i] = 0
    else:
        temp_df2['t1_win'][i] = 1

# %%
def find_switch(positionData):
    wrong_position_index_list = []
    for index in range(0, len(positionData)):
        if ((list(temp_df1.iloc[index,5:10]) == ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY']) == False):
            wrong_position_index_list.append(index)

    return wrong_position_index_list


# %%
def drop_switch(originalData, wrong_index):
    for i in wrong_index:
        originalData.drop(i, axis = 0, inplace = True)

# %%
def get_wrong_position_df(originalData, wrong_index):
    wrong_position_df = pd.DataFrame(columns=originalData.columns)
    for index in wrong_index:
        tempList = originalData.iloc[index,:]
        wrong_position_df = wrong_position_df.append(pd.Series(tempList), ignore_index=True)

    return wrong_position_df


# %%
t1_wrong_index = find_switch(temp_df1.iloc[:, 5:10])
t2_wrong_index = find_switch(temp_df2.iloc[:, 5:10])

# %%
a = get_wrong_position_df(temp_df1, t1_wrong_index)
b = get_wrong_position_df(temp_df2, t2_wrong_index)

# %%
drop_switch(temp_df1, t1_wrong_index)
drop_switch(temp_df2, t2_wrong_index)

# %%
position = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY']
position_encoded = [1, 2, 3, 4, 5]

a_encoded = a.replace(position, position_encoded)
b_encoded = b.replace(position, position_encoded)

# %%
def bubble_sort(encoded_postion, teamNumber):
    for q in range(0, len(encoded_postion)):
        array = list(encoded_postion.iloc[q, 5:10])
        n = len(array)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
                    encoded_postion['t%d_p%s_champion_name' % (teamNumber, str(j+1))][q], encoded_postion['t%d_p%s_champion_name' % (teamNumber, str(j+2))][q] = encoded_postion['t%d_p%s_champion_name' % (teamNumber, str(j+2))][q], encoded_postion['t%d_p%s_champion_name' % (teamNumber, str(j+1))][q]
                    encoded_postion['t%d_p%s_kda' % (teamNumber, str(j+1))][q], encoded_postion['t%d_p%s_kda' % (teamNumber, str(j+2))][q] = encoded_postion['t%d_p%s_kda' % (teamNumber, str(j+2))][q], encoded_postion['t%d_p%s_kda' % (teamNumber, str(j+1))][q]
                    encoded_postion['t%d_p%s_teamPosition' % (teamNumber, str(j+1))][q], encoded_postion['t%d_p%s_teamPosition' % (teamNumber, str(j+2))][q] = encoded_postion['t%d_p%s_teamPosition' % (teamNumber, str(j+2))][q], encoded_postion['t%d_p%s_teamPosition' % (teamNumber, str(j+1))][q]
                    encoded_postion['t%d_p%s_winRate' % (teamNumber, str(j+1))][q], encoded_postion['t%d_p%s_winRate' % (teamNumber, str(j+2))][q] = encoded_postion['t%d_p%s_winRate' % (teamNumber, str(j+2))][q], encoded_postion['t%d_p%s_winRate' % (teamNumber, str(j+1))][q]
                    encoded_postion['t%d_p%s_fiveGame_played' % (teamNumber, str(j+1))][q], encoded_postion['t%d_p%s_fiveGame_played' % (teamNumber, str(j+2))][q] = encoded_postion['t%d_p%s_fiveGame_played' % (teamNumber, str(j+2))][q], encoded_postion['t%d_p%s_fiveGame_played' % (teamNumber, str(j+1))][q]
                    encoded_postion['t%d_p%s_psScore' % (teamNumber, str(j+1))][q], encoded_postion['t%d_p%s_psScore' % (teamNumber, str(j+2))][q] = encoded_postion['t%d_p%s_psScore' % (teamNumber, str(j+2))][q], encoded_postion['t%d_p%s_psScore' % (teamNumber, str(j+1))][q]



# %%
bubble_sort(a_encoded, 1)

# %%
bubble_sort(b_encoded, 2)

# %%
t1_p1_champion_name = a_encoded['t1_p1_champion_name']
t1_p2_champion_name = a_encoded['t1_p2_champion_name']
t1_p3_champion_name = a_encoded['t1_p3_champion_name']
t1_p4_champion_name = a_encoded['t1_p4_champion_name']
t1_p5_champion_name = a_encoded['t1_p5_champion_name']

t2_p1_champion_name = b_encoded['t2_p1_champion_name']
t2_p2_champion_name = b_encoded['t2_p2_champion_name']
t2_p3_champion_name = b_encoded['t2_p3_champion_name']
t2_p4_champion_name = b_encoded['t2_p4_champion_name']
t2_p5_champion_name = b_encoded['t2_p5_champion_name']

a_encoded['t2_p1_champion_name'] = t2_p1_champion_name 
a_encoded['t2_p2_champion_name'] = t2_p2_champion_name 
a_encoded['t2_p3_champion_name'] = t2_p3_champion_name 
a_encoded['t2_p4_champion_name'] = t2_p4_champion_name 
a_encoded['t2_p5_champion_name'] = t2_p5_champion_name

b_encoded['t1_p1_champion_name'] = t1_p1_champion_name 
b_encoded['t1_p2_champion_name'] = t1_p2_champion_name 
b_encoded['t1_p3_champion_name'] = t1_p3_champion_name 
b_encoded['t1_p4_champion_name'] = t1_p4_champion_name 
b_encoded['t1_p5_champion_name'] = t1_p5_champion_name 

t1_p1_champion_name = temp_df1['t1_p1_champion_name']
t1_p2_champion_name = temp_df1['t1_p2_champion_name']
t1_p3_champion_name = temp_df1['t1_p3_champion_name']
t1_p4_champion_name = temp_df1['t1_p4_champion_name']
t1_p5_champion_name = temp_df1['t1_p5_champion_name']

t2_p1_champion_name = temp_df2['t2_p1_champion_name']
t2_p2_champion_name = temp_df2['t2_p2_champion_name']
t2_p3_champion_name = temp_df2['t2_p3_champion_name']
t2_p4_champion_name = temp_df2['t2_p4_champion_name']
t2_p5_champion_name = temp_df2['t2_p5_champion_name']

temp_df1['t2_p1_champion_name'] = t2_p1_champion_name 
temp_df1['t2_p2_champion_name'] = t2_p2_champion_name 
temp_df1['t2_p3_champion_name'] = t2_p3_champion_name 
temp_df1['t2_p4_champion_name'] = t2_p4_champion_name 
temp_df1['t2_p5_champion_name'] = t2_p5_champion_name


temp_df2['t1_p1_champion_name'] = t1_p1_champion_name 
temp_df2['t1_p2_champion_name'] = t1_p2_champion_name 
temp_df2['t1_p3_champion_name'] = t1_p3_champion_name 
temp_df2['t1_p4_champion_name'] = t1_p4_champion_name 
temp_df2['t1_p5_champion_name'] = t1_p5_champion_name 

# %%
t1_p1_psScore = a_encoded['t1_p1_psScore']
t1_p2_psScore = a_encoded['t1_p2_psScore']
t1_p3_psScore = a_encoded['t1_p3_psScore']
t1_p4_psScore = a_encoded['t1_p4_psScore']
t1_p5_psScore = a_encoded['t1_p5_psScore']

t2_p1_psScore = b_encoded['t2_p1_psScore']
t2_p2_psScore = b_encoded['t2_p2_psScore']
t2_p3_psScore = b_encoded['t2_p3_psScore']
t2_p4_psScore = b_encoded['t2_p4_psScore']
t2_p5_psScore = b_encoded['t2_p5_psScore']

a_encoded['t2_p1_psScore'] = t2_p1_psScore 
a_encoded['t2_p2_psScore'] = t2_p2_psScore 
a_encoded['t2_p3_psScore'] = t2_p3_psScore 
a_encoded['t2_p4_psScore'] = t2_p4_psScore 
a_encoded['t2_p5_psScore'] = t2_p5_psScore

b_encoded['t1_p1_psScore'] = t1_p1_psScore 
b_encoded['t1_p2_psScore'] = t1_p2_psScore 
b_encoded['t1_p3_psScore'] = t1_p3_psScore 
b_encoded['t1_p4_psScore'] = t1_p4_psScore 
b_encoded['t1_p5_psScore'] = t1_p5_psScore 

t1_p1_psScore = temp_df1['t1_p1_psScore']
t1_p2_psScore = temp_df1['t1_p2_psScore']
t1_p3_psScore = temp_df1['t1_p3_psScore']
t1_p4_psScore = temp_df1['t1_p4_psScore']
t1_p5_psScore = temp_df1['t1_p5_psScore']

t2_p1_psScore = temp_df2['t2_p1_psScore']
t2_p2_psScore = temp_df2['t2_p2_psScore']
t2_p3_psScore = temp_df2['t2_p3_psScore']
t2_p4_psScore = temp_df2['t2_p4_psScore']
t2_p5_psScore = temp_df2['t2_p5_psScore']

temp_df1['t2_p1_psScore'] = t2_p1_psScore 
temp_df1['t2_p2_psScore'] = t2_p2_psScore 
temp_df1['t2_p3_psScore'] = t2_p3_psScore 
temp_df1['t2_p4_psScore'] = t2_p4_psScore 
temp_df1['t2_p5_psScore'] = t2_p5_psScore


temp_df2['t1_p1_psScore'] = t1_p1_psScore 
temp_df2['t1_p2_psScore'] = t1_p2_psScore 
temp_df2['t1_p3_psScore'] = t1_p3_psScore 
temp_df2['t1_p4_psScore'] = t1_p4_psScore 
temp_df2['t1_p5_psScore'] = t1_p5_psScore 

# %%
team1_data = pd.concat([temp_df1, a_encoded])
team2_data = pd.concat([temp_df2, b_encoded])

# %%
def drop_teamPosition(originalData, teamNumber):
    for i in range(1, 6):
        originalData.drop("t%d_p%d_teamPosition" % (teamNumber, i), axis = 1, inplace = True)

# %%
drop_teamPosition(team1_data, 1)

# %%
drop_teamPosition(team2_data, 2)

# %%
temp_column_list = [
    'our_top_champ', 'our_jun_champ', 'our_mid_champ', 'our_bot_champ', 'our_sup_champ', 
    'win', 'our_top_kda', 'our_top_wr', 'our_top_five', 
    'our_jun_kda', 'our_jun_wr', 'our_jun_five',
    'our_mid_kda', 'our_mid_wr', 'our_mid_five',
    'our_bot_kda', 'our_bot_wr', 'our_bot_five', 
    'our_sup_kda', 'our_sup_wr', 'our_sup_five',
    'our_top_psScore', 'our_jun_psScore', 'our_mid_psScore', 'our_bot_psScore', 'our_sup_psScore',
    'opp_top_champ', 'opp_jun_champ', 'opp_mid_champ', 'opp_bot_champ', 'opp_sup_champ',
    'opp_top_psScore', 'opp_jun_psScore', 'opp_mid_psScore', 'opp_bot_psScore', 'opp_sup_psScore',
]


new_column_list = [
    'our_top_champ', 'our_top_kda', 'our_top_wr', 'our_top_five', 'our_top_psScore',
    'our_jun_champ', 'our_jun_kda', 'our_jun_wr', 'our_jun_five', 'our_jun_psScore',
    'our_mid_champ', 'our_mid_kda', 'our_mid_wr', 'our_mid_five', 'our_mid_psScore',
    'our_bot_champ', 'our_bot_kda', 'our_bot_wr', 'our_bot_five', 'our_bot_psScore',
    'our_sup_champ', 'our_sup_kda', 'our_sup_wr', 'our_sup_five', 'our_sup_psScore',
    'opp_top_champ', 'opp_top_psScore', 'opp_jun_champ', 'opp_jun_psScore', 
    'opp_mid_champ', 'opp_mid_psScore', 'opp_bot_champ', 'opp_bot_psScore', 'opp_sup_champ', 'opp_sup_psScore',
    'win'
]

# %%
team1_data.columns = temp_column_list
team2_data.columns = temp_column_list

# %%
final_df = pd.concat([team1_data, team2_data], ignore_index=True)

# %%
final_df.reset_index(inplace=True)
final_df.drop('index', inplace=True, axis=1)

# %%
final_df = final_df[new_column_list]

# %%
final_df

# %%
#final_df.to_csv('plat_final_dataset.csv')
final_df.to_csv('gold_final_dataset.csv')


