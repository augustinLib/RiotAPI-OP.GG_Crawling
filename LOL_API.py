# %% [markdown]
# # import library + init
# 

# %%
import time
import pandas as pd
import numpy as np
import requests
from urllib import parse
import time
import ssl
print(ssl.OPENSSL_VERSION)
 
api_key = "RGAPI-d8c1705b-ed7f-49b2-8b61-05bce6c2995c" # Input your API key

# %%
request_header = {
    
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-d8c1705b-ed7f-49b2-8b61-05bce6c2995c"

    #input Your header
}

# %%
def get_summonerList_by_tier(tier, division, page): # tier = [IRON, BRONZE, SILVER, GOLD, PLATINUM, DIAMOND, MASTER, GRANDMASTER, CHALLENGER] / division = [I, II, III, IV]
    url = "https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/" + tier + "/" + division + '?page=' + str(page)
    return requests.get(url, headers=request_header).json()
    

# %%
def get_summonerList_by_tier_iter(tier, division, maximumPage): # tier = [IRON, BRONZE, SILVER, GOLD, PLATINUM, DIAMOND, MASTER, GRANDMASTER, CHALLENGER]
                                                                # division = [I, II, III, IV]
    summoner_info = pd.DataFrame()   # maximumPage = 1일경우 205명, 2일 경우 410명... 총 뽑아지는 사람 수 = 205*maximumPage

    for iter in range(1, maximumPage+1): 
        temp = get_summonerList_by_tier(tier, division, iter) # 골드 3 소환사정보 추출
        if temp == []:
            break
        summoner_info = pd.concat([summoner_info, pd.DataFrame(temp)], ignore_index = True)
        time.sleep(1)
    return summoner_info


# %%
challenger_summoner_info = get_summonerList_by_tier_iter("CHALLENGER", "I", 1)
grandmaster_summoner_info = get_summonerList_by_tier_iter("GRANDMASTER", "I", 1)
master_summoner_info = get_summonerList_by_tier_iter("MASTER", "I", 1)  # maximumPage = 1일경우 205명, 2일 경우 410명... 총 뽑아지는 사람 수 = 205*maximumPage
diamond1_summoner_info = get_summonerList_by_tier_iter("DIAMOND", "I", 1)
diamond2_summoner_info = get_summonerList_by_tier_iter("DIAMOND", "II", 1)
diamond3_summoner_info = get_summonerList_by_tier_iter("DIAMOND", "III", 1)
diamond4_summoner_info = get_summonerList_by_tier_iter("DIAMOND", "IV", 2)
platinum1_summoner_info = get_summonerList_by_tier_iter("PLATINUM", "I", 4)
platinum2_summoner_info = get_summonerList_by_tier_iter("PLATINUM", "II", 4)
platinum3_summoner_info = get_summonerList_by_tier_iter("PLATINUM", "III", 7)
platinum4_summoner_info = get_summonerList_by_tier_iter("PLATINUM", "IV", 16)



# %%
def get_name_summonerId(summoner_info):
    name_summonerId = summoner_info[['summonerName', 'summonerId']]
    return name_summonerId

# %%
challenger_name_summonerId = get_name_summonerId(challenger_summoner_info)
grandmaster_name_summonerId = get_name_summonerId(grandmaster_summoner_info)
master_name_summonerId = get_name_summonerId(master_summoner_info)
diamond1_name_summonerId = get_name_summonerId(diamond1_summoner_info)
diamond2_name_summonerId = get_name_summonerId(diamond2_summoner_info)
diamond3_name_summonerId = get_name_summonerId(diamond3_summoner_info)
diamond4_name_summonerId = get_name_summonerId(diamond4_summoner_info)
platinum1_name_summonerId = get_name_summonerId(platinum1_summoner_info)
platinum2_name_summonerId = get_name_summonerId(platinum2_summoner_info)
platinum3_name_summonerId = get_name_summonerId(platinum3_summoner_info)
platinum4_name_summonerId = get_name_summonerId(platinum4_summoner_info)



# %%
def get_summoner_puuid(summonerID):
    temp = summonerID
    temp['puuid'] = ['' for i in range(summonerID.shape[0])]

    for iter in range(len(temp)):
        url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/" + temp.iloc[iter].summonerId
        r = requests.get(url, headers=request_header).json()
        temp.loc[iter]['puuid'] = r['puuid']
        time.sleep(1)

    return temp

# %%
challenger_name_summonerId_puuid = get_summoner_puuid(challenger_name_summonerId.head(3)) # 1
grandmaster_name_summonerId_puuid = get_summoner_puuid(grandmaster_name_summonerId.head(4)) # 2
master_name_summonerId_puuid = get_summoner_puuid(grandmaster_name_summonerId.head(54)) # 27
diamond1_name_summonerId_puuid = get_summoner_puuid(diamond1_name_summonerId.head(50)) # 25
diamond2_name_summonerId_puuid = get_summoner_puuid(diamond2_name_summonerId.head(76)) # 38
diamond3_name_summonerId_puuid = get_summoner_puuid(diamond3_name_summonerId.head(116)) # 58
diamond4_name_summonerId_puuid = get_summoner_puuid(diamond4_name_summonerId.head(368)) # 184
platinum1_name_summonerId_puuid = get_summoner_puuid(platinum1_name_summonerId.head(604)) # 302
platinum2_name_summonerId_puuid = get_summoner_puuid(platinum2_name_summonerId.head(608)) # 304
platinum3_name_summonerId_puuid = get_summoner_puuid(platinum3_name_summonerId.head(1034)) # 517
platinum4_name_summonerId_puuid = get_summoner_puuid(platinum4_name_summonerId.head(3082)) # 1541

# %%
challenger_name_summonerId_puuid = get_summoner_puuid(challenger_name_summonerId.head(3)) # 1
grandmaster_name_summonerId_puuid = get_summoner_puuid(grandmaster_name_summonerId.head(4)) # 2
master_name_summonerId_puuid = get_summoner_puuid(grandmaster_name_summonerId.head(54))

# %%
def match_v5_by_puuid(puuid): #puuid 하나당 10개의 match 추출
    matchId_df = pd.DataFrame()
    for id in puuid:
        url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + id + "/ids?start=0&count=1"
        r = requests.get(url, headers=request_header).json()
        matchId_df = matchId_df.append(r, ignore_index = True)
        time.sleep(1)

    return matchId_df

# %%
challenger_matchId_df = match_v5_by_puuid(challenger_name_summonerId_puuid.puuid) 
grandmaster_matchId_df = match_v5_by_puuid(grandmaster_name_summonerId_puuid.puuid)
master_matchId_df = match_v5_by_puuid(master_name_summonerId_puuid.puuid)
diamond1_matchId_df = match_v5_by_puuid(diamond1_name_summonerId_puuid.puuid)
diamond2_matchId_df = match_v5_by_puuid(diamond2_name_summonerId_puuid.puuid)
diamond3_matchId_df = match_v5_by_puuid(diamond3_name_summonerId_puuid.puuid)
diamond4_matchId_df = match_v5_by_puuid(diamond4_name_summonerId_puuid.puuid)
platinum1_matchId_df = match_v5_by_puuid(platinum1_name_summonerId_puuid.puuid)
platinum2_matchId_df = match_v5_by_puuid(platinum2_name_summonerId_puuid.puuid)
platinum3_matchId_df = match_v5_by_puuid(platinum3_name_summonerId_puuid.puuid)
platinum4_matchId_df = match_v5_by_puuid(platinum4_name_summonerId_puuid.puuid)

# %%
temp_list = [
    challenger_matchId_df, grandmaster_matchId_df, master_matchId_df, 
    diamond1_matchId_df, diamond2_matchId_df, diamond3_matchId_df, diamond4_matchId_df,
    platinum1_matchId_df, platinum2_matchId_df, platinum3_matchId_df, platinum4_matchId_df]

plaover_matchId_df = pd.concat(temp_list, ignore_index=True)
plaover_matchId_df.to_csv('plaover_matchId_df.csv')

# %%
plaover_matchId_df2 = pd.read_csv("/plaover_matchId_df.csv")
plaover_matchId_df2.drop(['Unnamed: 0'], axis = 1, inplace=True)
plaover_matchId_df2.columns = ['matchID']
plaover_matchId_df2.reset_index(drop=True, inplace = True)

# %%
#최종
def match_v5_gameinfo(match_id):
    final_match_df = pd.DataFrame(columns=(
        ["t1_p1_champion_name", "t1_p2_champion_name", "t1_p3_champion_name", 
        "t1_p4_champion_name", "t1_p5_champion_name", "t2_p1_champion_name", 
        "t2_p2_champion_name", "t2_p3_champion_name", "t2_p4_champion_name", 
        "t2_p5_champion_name", "t1_p1_summoner_name", "t1_p2_summoner_name", 
        "t1_p3_summoner_name", "t1_p4_summoner_name", "t1_p5_summoner_name", 
        "t2_p1_summoner_name", "t2_p2_summoner_name", "t2_p3_summoner_name", 
        "t2_p4_summoner_name", "t2_p5_summoner_name", "t1_p1_teamPosition", 
        "t1_p2_teamPosition", "t1_p3_teamPosition", "t1_p4_teamPosition", 
        "t1_p5_teamPosition", "t2_p1_teamPosition", "t2_p2_teamPosition", 
        "t2_p3_teamPosition", "t2_p4_teamPosition", "t2_p5_teamPosition", 
        "matchId" ,"t1_win"]))
    
    for i in match_id['matchID']:  #match_id:
        try:

            url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + i
            r = requests.get(url, headers=request_header).json()
            match_df = pd.DataFrame(r)
        
            if (match_df['info']['gameMode'] == "CLASSIC") and (match_df['info']['mapId'] == 11) and (len(match_df['info']["teams"][0]["bans"]) != 0):
                pt_df = pd.DataFrame(r['info']['participants'])
                temp_df = pt_df.loc[:,['championName' , 'summonerName', 'teamPosition', 'win']]
                temp_list = []
                for j in range(0,3):
                    for k in range(0,10):
                        temp_list.append(temp_df.iloc[k,j])

                temp_list.append(i)

                if (pt_df['win'][0] == True):
                    temp_list.append(1)
                else:
                    temp_list.append(0)
                final_match_df = final_match_df.append(pd.Series(temp_list, index=final_match_df.columns), ignore_index=True)

            time.sleep(1)
        except:
            time.sleep(1)
            continue


    return final_match_df

# %%
plaover_final_df = match_v5_gameinfo(plaover_matchId_df2)
plaover_final_df

# %%
plaover_final_df.to_csv('plaover_final_df.csv')

# %%
matchData = pd.read_csv('plaover_final_df.csv')
matchData.drop('Unnamed: 0', inplace=True, axis=1)

# %%
korean_name = [
    "가렌" , "갈리오", '갱플랭크', '그라가스', '그레이브즈', '그웬', '나르', '나미', '나서스', '노틸러스', '녹턴', '누누와 윌럼프', '니달리',
    '니코', '다리우스', '다이애나', '드레이븐', '라이즈', '라칸', '람머스', '럭스', '럼블', '레넥톤', '레오나', '렉사이', '렐', '렝가', '루시안',
    '룰루', '르블랑', '리 신', '리븐', '리산드라', '릴리아', '마스터 이', '마오카이', '말자하', '말파이트', '모데카이저', '모르가나', '문도 박사',
    '미스 포츈', '바드', '바루스', '바이', '베이가', '베인', '벡스', '벨코즈', '볼리베어', '브라움', '브랜드', '블라디미르', '블리츠크랭크', '비에고',
    '빅토르', '뽀삐', '사미라', '사이온', '사일러스', '샤코', '세나', '세라핀', '세주아니', '세트', '소나', '소라카', '쉔', '쉬바나', '스웨인', '스카너',
    '시비르', '신 짜오', '신드라', '신지드', '쓰레쉬', '아리', '아무무', '아우렐리온 솔', '아이번', '아지르', '아칼리', '아크샨', '아트록스', '아펠리오스',
    '알리스타', '애니', '애니비아', '애쉬', '야스오', '에코', '엘리스', '오공', '오른', '오리아나', '올라프', '요네', '요릭', '우디르', '우르곳', '워윅',
    '유미', '이렐리아', '이블린', '이즈리얼', '일라오이', '자르반 4세', '자야', '자이라', '자크', '잔나', '잭스', '제드', '제라스', '제이스', '조이', '직스',
    '진', '질리언', '징크스', '초가스', '카르마', '카밀', '카사딘', '카서스', '카시오페아', '카이사', '카직스', '카타리나', '칼리스타', '케넨', '케이틀린', '케인',
    '케일', '코그모', '코르키', '퀸', '클레드', '키아나', '킨드레드', '타릭', '탈론', '탈리야', '탐 켄치', '트런들', '트리스타나', '트린다미어', '트위스티드 페이트',
    '트위치', '티모', '파이크', '판테온', '피들스틱', '피오라', '피즈', '하이머딩거', '헤카림' 
]

english_name = [
    "Garen" , "Galio", 'Gangplank', 'Gragas', 'Graves', 'Gwen', 'Gnar', 'Nami', 'Nasus', 'Nautilus', 'Nocturne', 'Nunu', 'Nidalee',
    'Neeko', 'Darius', 'Diana', 'Draven', 'Ryze', 'Rakan', 'Rammus', 'Lux', 'Rumble', 'Renekton', 'Leona', 'RekSai', 'Rell', 'Rengar', 'Lucian',
    'Lulu', 'Leblanc', 'LeeSin', 'Riven', 'Lissandra', 'Lillia', 'MasterYi', 'Maokai', 'Malzahar', 'Malphite', 'Mordekaiser', 'Morgana', 'DrMundo',
    'MissFortune', 'Bard', 'Varus', 'Vi', 'Veigar', 'Vayne', 'Vex', 'Velkoz', 'Volibear', 'Braum', 'Brand', 'Vladimir', 'Blitzcrank', 'Viego',
    'Viktor', 'Poppy', 'Samira', 'Sion', 'Sylas', 'Shaco', 'Senna', 'Seraphine', 'Sejuani', 'Sett', 'Sona', 'Soraka', 'Shen', 'Shyvana', 'Swain', 'Skarner',
    'Sivir', 'XinZhao', 'Syndra', 'Singed', 'Thresh', 'Ahri', 'Amumu', 'AurelionSol', 'Ivern', 'Azir', 'Akali', 'Akshan', 'Aatrox', 'Aphelios',
    'Alistar', 'Annie', 'Anivia', 'Ashe', 'Yasuo', 'Ekko', 'Elise', 'MonkeyKing', 'Ornn', 'Orianna', 'Olaf', 'Yone', 'Yorick', 'Udyr', 'Urgot', 'Warwick',
    'Yuumi', 'Irelia', 'Evelynn', 'Ezreal', 'Illaoi', 'JarvanIV', 'Xayah', 'Zyra', 'Zac', 'Janna', 'Jax', 'Zed', 'Xerath', 'Jayce', 'Zoe', 'Ziggs',
    'Jhin', 'Zilean', 'Jinx', 'Chogath', 'Karma', 'Camille', 'Kassadin', 'Karthus', 'Cassiopeia', 'Kaisa', 'Khazix', 'Katarina', 
    'Kalista', 'Kennen', 'Caitlyn', 'Kayn', 'Kayle', 'KogMaw', 'Corki', 'Quinn', 'Kled', 'Qiyana', 'Kindred', 'Taric', 'Talon', 
    'Taliyah', 'TahmKench', 'Trundle', 'Tristana', 'Tryndamere', 'TwistedFate',
    'Twitch', 'Teemo', 'Pyke', 'Pantheon', 'FiddleSticks', 'Fiora', 'Fizz', 'Heimerdinger', 'Hecarim' 
]

# %%
matchData_temp = matchData.iloc[:, :10]

# %%
for i in range(0, 157):
    matchData_temp.replace(english_name[i], korean_name[i], inplace=True)

# %%
matchData.iloc[:, :10] = matchData_temp
matchData

# %%
matchData.to_csv('plaover_final_korean_df.csv')


