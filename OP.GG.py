
# %%
import time
from tqdm import tqdm
import pandas as pd
from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# %%
# headless selenium
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')

# %%
request_header = {
    
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8"

    #Input your header
}

# %%
def refresh(userName):
    userName2 = "+".join(userName.split())
    # 유저별 검색 결과 url
    url = f"https://www.op.gg/summoner/champions/userName={userName2}"
    driver = webdriver.Chrome("/chromedriver", options=options)
    driver.get(url)
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="SummonerRefreshButton"]').click()
    driver.quit()
    return

# %%
def my_champion(userName):
    # 빈 데이터 프레임
    data = pd.DataFrame()
    
    # 띄어쓰기 있는 유저이면 +로 구분
    userName2 = "+".join(userName.split())

    # 유저별 검색 결과 url
    url = f"https://www.op.gg/summoner/champions/userName={userName2}"
    
    response = requests.get(url, headers=request_header)
    

    # url 정보 저장
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html')


    else : 
        print(response.status_code)

    # 플레이한 챔피언 데이터 테이블
    champ_info = soup.find("div", attrs= {"class":"Content tabItems"})
    champ_info2 = champ_info.find("div", attrs= {"class":"tabItem season-18"})
    champ_info3 = champ_info2.find("tbody", attrs= {"class":"Body"})
    champ_info4 = champ_info3.find_all("tr")
    
    # 각 태그 지정해서 원하는 정보 추출
    for i in range(len(champ_info4)):
        lst = []
        # 챔피언 이름
        lst.append(champ_info4[i].find("td", attrs= {"class":"ChampionName Cell"}).get_text().strip())

        # 승/패 (단, 한번도 이기거나 진적이 없으면 해당 class가 없음)
        if champ_info4[i].find("div", attrs= {"class":"Text Left"}) == None:
            lst.append(0)
        else:
            lst.append(champ_info4[i].find("div", attrs= {"class":"Text Left"}).get_text().strip()[:-1])

        if champ_info4[i].find("div", attrs= {"class":"Text Right"}) == None:
            lst.append(0)
        else:
            lst.append(champ_info4[i].find("div", attrs= {"class":"Text Right"}).get_text().strip()[:-1])

        # K/D/A
        KDA = champ_info4[i].find("div", attrs= {"class":"KDA"}).get_text().strip().split()
        lst.append(KDA[0])
        lst.append(KDA[2])
        lst.append(KDA[4])
        
        # 기타 정보
        else_info = champ_info4[i].find_all("td", attrs={"class":"Value Cell"})
        for i in else_info:
            info = i.get_text().strip().split()
            if len(info) == 0:
                lst.append(0)
            else:
                lst.append(info[0])
        
        # 데이터 프레임
        champ_df = pd.DataFrame(lst)
        data = pd.concat([data, champ_df], axis=1)
    
    # 데이터 프레임 형태, 타입 설정
    data = data.T
    data.index = range(data.shape[0])
    data.columns = [
        "champion", "win", "lose", "kill", "death", "assist", 
        "gold", "cs", "max_kill", "max_death", "avg_damage", "avg_damaged", "double", "triple", "quadra", "penta"
    ]
    
    data["win"] = data["win"].astype(int)
    data["lose"] = data["lose"].astype(int)
    data["kill"] = data["kill"].astype(float)
    data["death"] = data["death"].astype(float)
    data["death"] = data.death.replace(0,1)
    data["assist"] = data["assist"].astype(float)
    data["gold"] = data["gold"].apply(lambda x: int(x.replace(",","")))
    data["cs"] = data["cs"].astype(float)
    data["max_kill"] = data["max_kill"].astype(int)
    data["max_death"] = data["max_death"].astype(int)
    data["avg_damage"] = data["avg_damage"].apply(lambda x: int(x.replace(",","")))
    data["avg_damaged"] = data["avg_damaged"].apply(lambda x: int(x.replace(",","")))
    data["double"] = data["double"].astype(int)
    data["triple"] = data["triple"].astype(int)
    data["quadra"] = data["quadra"].astype(int)
    data["penta"] = data["penta"].astype(int)
    



    return data

# %%
matchData = pd.read_csv('/bsg_final_korean_df.csv') #LOL API로 수집한 matchdata
matchData.drop('Unnamed: 0', inplace=True, axis=1)

# %%
#맥용
import pickle

gold = pd.read_csv("/gold.csv", encoding = "cp949")
gold.drop('Unnamed: 0', inplace=True, axis=1)
plat = pd.read_csv("/gold.csv", encoding = "cp949")
plat.drop('Unnamed: 0', inplace=True, axis=1)

name_gold = []

for i in range(1,3):
    for j in range(1,6):
        name_gold.append(gold["t"+str(i)+"_p"+str(j)+"_summoner_name"].tolist())


name_plat = []

for i in range(1,3):
    for j in range(1,6):
        name_plat.append(plat["t"+str(i)+"_p"+str(j)+"_summoner_name"].tolist())


name_gold = sum(name_gold, [])
name_plat = sum(name_plat, [])

name_gold = list(set(name_gold))
name_plat = list(set(name_plat))

# %%
def add_summoner_info(userName):
    result = my_champion(userName)
    final_result = pd.DataFrame()
    final_result['champion'] = result['champion']
    final_result['kda'] = (result['kill'] + result['assist']) / result['death']
    final_result['winRate'] = (result['win'] / (result['win'] + result['lose'])) * 100
    final_result['fiveGame_played'] = 0
    for q in range(0, len(result['win'])):
        if((result['win'][q] + result['lose'][q]) >= 5):
            final_result['fiveGame_played'][q] = 1
    return final_result


# %%
a = name_gold[:3000]
b = name_gold[3000:6000]
c = name_gold[6000:9000]
d = name_gold[9000:12000]
e = name_gold[12000:15000]
f = name_gold[15000:]

# %%
name_list2 = a

for i in tqdm(range(0, len(name_list2))):
    try:
        refresh(name_list2[i])

    except:
        continue

# %%
name_list = f
temp_data_list = []

for i in tqdm(range(0, len(name_list))):
    try:
        temp = add_summoner_info(name_list[i])
        temp['summoner_name'] = name_list[i]
        temp_data_list.append(temp)
    except:
        continue

result = pd.concat(temp_data_list)
result.reset_index(inplace=True)
result.drop('index', inplace=True, axis=1)

result

# %%
gold_6 = result


# %%
gold_6

# %%
gold_6.to_csv('gold_6.csv')

# %%
gold_1

# %%
gold_final = pd.concat([gold_1, gold_2, gold_3, gold_4, gold_5, gold_6])

# %%
gold_final

# %%
gold_final.reset_index(inplace=True)
gold_final.drop('index', inplace=True, axis=1)
gold_final

# %%
gold_final.to_csv('gold_final.csv')


