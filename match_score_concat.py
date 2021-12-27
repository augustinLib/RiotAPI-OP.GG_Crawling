# %%
import pandas as pd
import numpy as np

# %%
match_data = pd.read_csv('/gold_merge_fianl.csv')
match_data.columns

# %%
match_data.drop('Unnamed: 0', inplace=True, axis=1)
#match_data.drop('Unnamed: 0.1', inplace=True, axis=1)
#match_data.drop('Unnamed: 0.1.1', inplace=True, axis=1)

# %%
top = pd.read_csv('/브실골 탑.csv', encoding='cp949')
jug = pd.read_csv('/브실골 정글.csv', encoding='cp949')
mid = pd.read_csv('/브실골 미드.csv', encoding='cp949')
adc = pd.read_csv('/브실골 원딜.csv', encoding='cp949')
sup = pd.read_csv('/브실골 서폿.csv', encoding='cp949')

# %%
top.drop('Unnamed: 0', inplace=True, axis=1)
jug.drop('Unnamed: 0', inplace=True, axis=1)
mid.drop('Unnamed: 0', inplace=True, axis=1)
adc.drop('Unnamed: 0', inplace=True, axis=1)
sup.drop('Unnamed: 0', inplace=True, axis=1)

# %%
top.reset_index(inplace=True)
jug.reset_index(inplace=True)
mid.reset_index(inplace=True)
adc.reset_index(inplace=True)
sup.reset_index(inplace=True)

# %%
top.drop('index', inplace=True, axis=1)
jug.drop('index', inplace=True, axis=1)
mid.drop('index', inplace=True, axis=1)
adc.drop('index', inplace=True, axis=1)
sup.drop('index', inplace=True, axis=1)

# %%
def add_match_score(matchData):
    tx_px_psScore = np.zeros(len(match_data))


    scoreData = pd.DataFrame({
    't1_p1_psScore' : tx_px_psScore, 't1_p2_psScore' : tx_px_psScore, 't1_p3_psScore' : tx_px_psScore, 't1_p4_psScore' : tx_px_psScore, 
    't1_p5_psScore' : tx_px_psScore, 't2_p1_psScore' : tx_px_psScore, 't2_p2_psScore' : tx_px_psScore, 't2_p3_psScore' : tx_px_psScore, 
    't2_p4_psScore' : tx_px_psScore, 't2_p5_psScore' : tx_px_psScore 
    })
 



    for i in range(0, len(matchData)):
        for teamNumber in range(1, 3):
            for playerNumber in range(1, 6):
                if (matchData['t%d_p%d_teamPosition' %(teamNumber, playerNumber)][i] == 'TOP'):
                    for j in range(0,len(top)):
                        if(matchData['t%d_p%d_champion_name' %(teamNumber, playerNumber)][i] == top['champion'][j]):
                            scoreData['t%d_p%d_psScore' %(teamNumber, playerNumber)][i] = top['op_score'][j]
                            

                elif (matchData['t%d_p%d_teamPosition' %(teamNumber, playerNumber)][i] == 'JUNGLE'):
                    for j in range(0,len(jug)):
                        if(matchData['t%d_p%d_champion_name' %(teamNumber, playerNumber)][i] == jug['champion'][j]):
                            scoreData['t%d_p%d_psScore' %(teamNumber, playerNumber)][i] = jug['op_score'][j]
                            


                elif (matchData['t%d_p%d_teamPosition' %(teamNumber, playerNumber)][i] == 'MIDDLE'):
                    for j in range(0,len(mid)):
                        if(matchData['t%d_p%d_champion_name' %(teamNumber, playerNumber)][i] == mid['champion'][j]):
                            scoreData['t%d_p%d_psScore' %(teamNumber, playerNumber)][i] = mid['op_score'][j]
                            


                elif (matchData['t%d_p%d_teamPosition' %(teamNumber, playerNumber)][i] == 'BOTTOM'):
                    for j in range(0,len(adc)):
                        if(matchData['t%d_p%d_champion_name' %(teamNumber, playerNumber)][i] == adc['champion'][j]):
                            scoreData['t%d_p%d_psScore' %(teamNumber, playerNumber)][i] = adc['op_score'][j]
                            


                elif (matchData['t%d_p%d_teamPosition' %(teamNumber, playerNumber)][i] == 'UTILITY'):
                    for j in range(0,len(sup)):
                        if(matchData['t%d_p%d_champion_name' %(teamNumber, playerNumber)][i] == sup['champion'][j]):
                            scoreData['t%d_p%d_psScore' %(teamNumber, playerNumber)][i] = sup['op_score'][j]
                            

                else:
                    print("wrong input")
                    print()
                    return

    
    return scoreData



                        

# %%
plat_score_data = add_match_score(match_data)
plat_score_data

# %%
match_data

# %%
plat_score_data.to_csv('plat_score_data.csv')

# %%
for teamNumber in range(1, 3):
    for playerNumber in range(1, 6):
        match_data['t%d_p%d_psScore' %(teamNumber, playerNumber)] = plat_score_data['t%d_p%d_psScore' %(teamNumber, playerNumber)]

# %%
match_data

# %%
match_data.to_csv('gold_final_added_score.csv')


