import pandas
from fake_useragent import UserAgent
import requests
import os
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
import time
from chromedriver_py import binary_path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json

ua = UserAgent().random
url = 'https://tracker.gg/valorant/leaderboards/ranked/all/default?page=2®ion=global&act=22d10d66-4d2a-a340-6c54-408c7bd53807'

scriptdir = os.path.dirname(__file__)

def inserir_dados(data):
    print("Inserindo dados para o jogador:", data['Username'], "#", data['Tag'])
    try:
        url = 'http://localhost:8080/jogador/criar-jogador'
        
        jogador_request_data = {
            'username': data['Username'],
            'tag': data['Tag'],
            'url': data['Url'],
            'dpR': numeroString(data['DpR']),
            'kdr': numeroString(data['KDR']),
            'headshot': numeroString(data['Headshot%']),
            'win': numeroString(data['Win%']),
            'wins': numeroString(data['Wins']),
            'kast': numeroString(data['KAST']),
            'dddeltaR': numeroString(data['DDdeltaR']),
            'kills': numeroString(data['Kills']),
            'deaths': numeroString(data['Deaths']),
            'assists': numeroString(data['Assists']),
            'acs': numeroString(data['ACS']),
            'kadRatio': numeroString(data['KADRatio']),
            'killsPerRound': numeroString(data['KillsPerRound']),
            'clutch1v1s': numeroString(data['Clutch1v1s']),
            'flawlessRounds': numeroString(data['FlawlessRounds']),
            'currentRating': numeroString(data['CurrentRating']),
            'peakRating': numeroString(data['PeakRating']),
            'playtime': numeroString(data['Playtime']),
            'matches': numeroString(data['Matches']),
            'level': numeroString(data['Level']),
            'losses': numeroString(data['Losses']),
            'topAgent1': data['TopAgent1'],
            'topAgent2': data['TopAgent2'],
            'topAgent3': data['TopAgent3'],
            'topHoursAgent1': numeroString(data['TopHoursAgent1']),
            'topHoursAgent2': numeroString(data['TopHoursAgent2']),
            'topHoursAgent3': numeroString(data['TopHoursAgent3']),
            'topMatchesAgent1': numeroString(data['TopMatchesAgent1']),
            'topMatchesAgent2': numeroString(data['TopMatchesAgent2']),
            'topMatchesAgent3': numeroString(data['TopMatchesAgent3']),
            'topWinAgent1': numeroString(data['TopWinAgent1']),
            'topWinAgent2': numeroString(data['TopWinAgent2']),
            'topWinAgent3': numeroString(data['TopWinAgent3']),
            'topKDAgent1': numeroString(data['TopKDAgent1']),
            'topKDAgent2': numeroString(data['TopKDAgent2']),
            'topKDAgent3': numeroString(data['TopKDAgent3']),
            'topWeapon1': data['TopWeapon1'],
            'topWeaponHeadshot1': numeroString(data['TopWeaponHeadshot1']),
            'topWeaponBodyshot1': numeroString(data['TopWeaponBodyshot1']),
            'topWeaponLegshot1': numeroString(data['TopWeaponLegshot1']),
            'topWeaponKills1': numeroString(data['TopWeaponKills1']),
            'topWeapon2': data['TopWeapon2'],
            'topWeaponHeadshot2': numeroString(data['TopWeaponHeadshot2']),
            'topWeaponBodyshot2': numeroString(data['TopWeaponBodyshot2']),
            'topWeaponLegshot2': numeroString(data['TopWeaponLegshot2']),
            'topWeaponKills2': numeroString(data['TopWeaponKills2']),
            'topWeapon3': data['TopWeapon3'],
            'topWeaponHeadshot3': numeroString(data['TopWeaponHeadshot3']),
            'topWeaponBodyshot3': numeroString(data['TopWeaponBodyshot3']),
            'topWeaponLegshot3': numeroString(data['TopWeaponLegshot3']),
            'topWeaponKills3': numeroString(data['TopWeaponKills3']),
            'topMap1': data['TopMap1'],
            'topMapWinrate1': numeroString(data['TopMapWinrate1']),
            'topMapWins1': numeroString(data['TopMapWins1']),
            'topMapLosses1': numeroString(data['TopMapLosses1']),
            'topMap2': data['TopMap2'],
            'topMapWinrate2': numeroString(data['TopMapWinrate2']),
            'topMapWins2': numeroString(data['TopMapWins2']),
            'topMapLosses2': numeroString(data['TopMapLosses2']),
            'topMap3': data['TopMap3'],
            'topMapWinrate3': numeroString(data['TopMapWinrate3']),
            'topMapWins3': numeroString(data['TopMapWins3']),
            'topMapLosses3': numeroString(data['TopMapLosses3']),
            'topMap4': data['TopMap4'],
            'topMapWinrate4': numeroString(data['TopMapWinrate4']),
            'topMapWins4': numeroString(data['TopMapWins4']),
            'topMapLosses4': numeroString(data['TopMapLosses4']),
            'topMap5': data['TopMap5'],
            'topMapWinrate5': numeroString(data['TopMapWinrate5']),
            'topMapWins5': numeroString(data['TopMapWins5']),
            'topMapLosses5': numeroString(data['TopMapLosses5']),
            'topMap6': data['TopMap6'],
            'topMapWinrate6': numeroString(data['TopMapWinrate6']),
            'topMapWins6': numeroString(data['TopMapWins6']),
            'topMapLosses6': numeroString(data['TopMapLosses6']),
            'topMap7': data['TopMap7'],
            'topMapWinrate7': numeroString(data['TopMapWinrate7']),
            'topMapWins7': numeroString(data['TopMapWins7']),
            'topMapLosses7': numeroString(data['TopMapLosses7']),
            'topMap8': data['TopMap8'],
            'topMapWinrate8': numeroString(data['TopMapWinrate8']),
            'topMapWins8': numeroString(data['TopMapWins8']),
            'topMapLosses8': numeroString(data['TopMapLosses8']),
            'topMap9': data['TopMap9'],
            'topMapWinrate9': numeroString(data['TopMapWinrate9']),
            'topMapWins9': numeroString(data['TopMapWins9']),
            'topMapLosses9': numeroString(data['TopMapLosses9']),
            'topMap10': data['TopMap10'],
            'topMapWinrate10': numeroString(data['TopMapWinrate10']),
            'topMapWins10': numeroString(data['TopMapWins10']),
            'topMapLosses10': numeroString(data['TopMapLosses10']),
            'views': numeroString(data['views'])
        }

        response = requests.post(url, json=jogador_request_data)
        
        if response.status_code == 200:
            print("Dados inseridos com sucesso:", response.json())
        else:
            print("Erro ao inserir dados. Status code:", response.status_code, response.text)
    except Exception as e:
        pass
        print("Erro ao inserir os dados:", e)

def scrapePlayer(user, tag):
    svc = ChromeService(executable_path=binary_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=svc, options=options)
    ua = UserAgent().random
    nuser = str(user.strip()).replace(' ', '%20')
    ntag = str(tag.strip()).replace('#', '')
    uurl = f'https://tracker.gg/valorant/profile/riot/{nuser}%23{ntag}/overview?season=all'
    url = str(uurl)
    driver.get(url=url)
    time.sleep(10)
    src = driver.page_source
    with open(os.path.join(scriptdir, 'oi.txt'), 'w', encoding='utf-8') as f:
        f.write(src)
    soup = bs(src, 'html.parser')
    gstats = soup.find('div', {'class':'giant-stats'})
    gstats = gstats.find_all('div', recursive=False)
    gstat = []
    for div in gstats:
        nums = div.find('div', {'class':'numbers'})
        val = nums.find('span', {'class':'value'}).text
        gstat.append(val)
    playerDpR = gstat[0]
    playerKDR = gstat[1]
    playerHeadRate = gstat[2]
    playerWinRate = gstat[3]

    mstats = soup.find('div', {'class':'main'})
    mstats = mstats.find_all('div', recursive=False)
    mstat = []
    for div in mstats:
        nums = div.find('div', {'class':'numbers'})
        val = nums.find('span', {'class':'value'}).text
        mstat.append(val)
    playerWins = mstat[0].replace(',', '.')
    playerKAST = mstat[1]
    playerDDdeltaR = mstat[2]
    playerKills = mstat[3].replace(',', '.')
    playerDeaths = mstat[4].replace(',', '.')
    playerAssists = mstat[5].replace(',', '.')
    playerACS = mstat[6]
    playerKADRatio = mstat[7]
    playerKillsPerRound = mstat[8]
    playerClutch1v1 = mstat[9].replace(',', '.')
    playerFlawless = mstat[10].replace(',', '.')
    
    ratings = soup.find('div', {'class':['rating-summary', 'trn-card', 'trn-card--bordered', 'has-primary', 'area-rating']})
    ratings = ratings.find_all('div', recursive=False)
    rating = []
    for div in ratings:
        val = div.find('span', {'class':'mmr'}).text
        rating.append(val)
    playerCurrentRating = rating[0]
    playerPeakRating = rating[1].replace(',', '.')
    
    topweapons = soup.find('div', {'class': 'top-weapons__content'})
    topweapons = topweapons.find_all('div', recursive=False)
    playerTopWeapons = {}
    playerTopWeaponsList = []
    for i, weapon in enumerate(topweapons):
        weaponname = weapon.find('div', {'class':'weapon__name'}).text
        weaponacc = weapon.find('div', {'class':'weapon__accuracy'})
        weaponacc = weaponacc.find_all('span', {'class':'stat'})
        weaponacc = [acc.text for acc in weaponacc]
        weaponkills = weapon.find('span', {'class':'value'}).text.replace(',', '.')
        playerweapondict = {
            'name': weaponname,
            'head%': weaponacc[0],
            'body%': weaponacc[1],
            'leg%': weaponacc[2],
            'kills': weaponkills
        }
        weaponkey = f"topWeapon{i+1}"
        playerTopWeapons.update({weaponkey: playerweapondict})
        playerTopWeaponsList.append(playerweapondict)
    
    topmaps = soup.find('div', {'class':'top-maps__maps'})
    topmaps = topmaps.find_all('div', {'class':'top-maps__maps-map'})
    playerTopMaps = {}
    playerTopMapsList = []
    for i, map in enumerate(topmaps):
        mapname = map.find('div', {'class':'name'}).text
        mapinfo = map.find('div', {'class':'info'})
        mapwinrate = mapinfo.find('div', {'class':'value'}).text
        mapwinlose = str(mapinfo.find('div', {'class':'label'}).text)
        mapwin = mapwinlose.split('W - ')[0]
        maplose = mapwinlose.split('W - ')[1].split('L')[0]
        mapdict = {
            'name': mapname,
            'winrate': mapwinrate,
            'wins': mapwin,
            'loses': maplose
        }
        mapkey = f"topMap{i+1}"
        playerTopMaps.update({mapkey: mapdict})
        playerTopMapsList.append(mapdict)
        
    topagents = soup.find('div', {'class':'area-top-agents'})
    topagents = topagents.find('div', {'class':'st-content__category'})
    topagents = topagents.find_all('div', {'class':'st-content__item'})
    playerTopAgents = {}
    playerTopAgentsList = []
    for i, agent in enumerate(topagents):
        agentitems = agent.find_all('div', {'class':'st__item'})
        agentvalues = []
        for j, agentitem in enumerate(agentitems):
            iteminfo = agentitem.find('div', {'class':'info'})
            if j == 0:
                agentname = iteminfo.find('div', {'class':'value'}).text
                agenthrs = iteminfo.find('div', {'class':'label'}).text
            elif j == len(agentitems) - 1:
                agenttopmapdiv = iteminfo.find('div', recursive=False)
                agenttopmap = agenttopmapdiv.find('div', recursive=False).text
                agenttopmapwinrate = agenttopmapdiv.find('span').text
            else:
                itemvalue = iteminfo.find('div', {'class':'value'}).text
                agentvalues.append(itemvalue)
        agentmatches = agentvalues[0]
        agentwinrate = agentvalues[1]
        agentkd = agentvalues[2]
        agentadr = agentvalues[3]
        agentacs = agentvalues[4]
        agentdddelta = agentvalues[5]
        agentdict = {
            'name': agentname,
            'hours': str(agenthrs).replace(' hours', ''),
            'matches': agentmatches.replace(',', '.'),
            'winrate': agentwinrate,
            'kd': agentkd,
            'adr': agentadr,
            'acs': agentacs,
            'dddelta': agentdddelta,
            'topmapname': str(agenttopmap).replace(str(agenttopmapwinrate), '').strip(),
            'topmapwinrate': agenttopmapwinrate
        }
        agentkey = f"topAgent{i+1}"
        playerTopAgents.update({agentkey: agentdict})
        playerTopAgentsList.append(agentdict)
    
    ttstats = soup.find('div', {'class': 'title-stats'})
    playerPlaytime = str(ttstats.find('span', {'class':'playtime'}).text).replace(' Playtime', '').strip().replace('h', '')
    playerMatches = str(ttstats.find('span', {'class':'matches'}).text).replace(' Matches', '').strip().replace(',', '.')

    highlightedstats = soup.find('div', {'class': 'trn-profile-highlighted-content__stats'})
    lvstat = highlightedstats.find_all('div', {'class':'stat'})[1]
    playerLevel = lvstat.find('span', {'class':'stat__value'}).text

    lossstat = highlightedstats.find('div', {'class':'trn-profile-highlighted-content__ratio'})
    lossgs = lossstat.find_all('g')[1]
    playerLosses = lossgs.find_all('text')[1].text
    
    views = soup.find('span', {'class':'ph-details__subtitle-wrapper'})
    view = views.find_all('span')[0]
    view = views.find_all('span')[0].text

    playerData = {
        'Username': user,
        'Tag': tag,
        'Url': url,
        'DpR': playerDpR,
        'KDR': playerKDR,
        'Headshot%': playerHeadRate,
        'Win%': playerWinRate,
        'Wins': playerWins,
        'KAST': playerKAST,
        'DDdeltaR': playerDDdeltaR,
        'Kills': playerKills,
        'Deaths': playerDeaths,
        'Assists': playerAssists,
        'ACS': playerACS,
        'KADRatio': playerKADRatio,
        'KillsPerRound': playerKillsPerRound,
        'Clutch1v1s': playerClutch1v1,
        'FlawlessRounds': playerFlawless,
        'CurrentRating': playerCurrentRating,
        'PeakRating': playerPeakRating,
        'TopWeaponsDict': playerTopWeapons,
        'TopWeaponsList': playerTopWeaponsList,
        'TopMapsDict': playerTopMaps,
        'TopMapsList': playerTopMapsList,
        'TopAgentsDict': playerTopAgents,
        'TopAgentsList': playerTopAgentsList,
        'Playtime': playerPlaytime,
        'Matches': playerMatches,
        'Level': playerLevel,
        'Losses': playerLosses,
        'TopAgent1': playerTopAgents['topAgent1']['name'],
        'TopAgent2': playerTopAgents['topAgent2']['name'],
        'TopAgent3': playerTopAgents['topAgent3']['name'],
        'TopHoursAgent1': playerTopAgents['topAgent1']['hours'],
        'TopHoursAgent2': playerTopAgents['topAgent2']['hours'],
        'TopHoursAgent3': playerTopAgents['topAgent3']['hours'],
        'TopMatchesAgent1': playerTopAgents['topAgent1']['matches'],
        'TopMatchesAgent2': playerTopAgents['topAgent2']['matches'],
        'TopMatchesAgent3': playerTopAgents['topAgent3']['matches'],
        'TopWinAgent1': playerTopAgents['topAgent1']['winrate'],
        'TopWinAgent2': playerTopAgents['topAgent2']['winrate'],
        'TopWinAgent3': playerTopAgents['topAgent3']['winrate'],
        'TopKDAgent1': playerTopAgents['topAgent1']['kd'],
        'TopKDAgent2': playerTopAgents['topAgent2']['kd'],
        'TopKDAgent3': playerTopAgents['topAgent3']['kd'],
        'TopWeapon1': playerTopWeapons['topWeapon1']['name'],
        'TopWeaponHeadshot1': playerTopWeapons['topWeapon1']['head%'],
        'TopWeaponBodyshot1': playerTopWeapons['topWeapon1']['body%'],
        'TopWeaponLegshot1': playerTopWeapons['topWeapon1']['leg%'],
        'TopWeaponKills1': playerTopWeapons['topWeapon1']['kills'],
        'TopWeapon2': playerTopWeapons['topWeapon2']['name'],
        'TopWeaponHeadshot2': playerTopWeapons['topWeapon2']['head%'],
        'TopWeaponBodyshot2': playerTopWeapons['topWeapon2']['body%'],
        'TopWeaponLegshot2': playerTopWeapons['topWeapon2']['leg%'],
        'TopWeaponKills2': playerTopWeapons['topWeapon2']['kills'],
        'TopWeapon3': playerTopWeapons['topWeapon3']['name'],
        'TopWeaponHeadshot3': playerTopWeapons['topWeapon3']['head%'],
        'TopWeaponBodyshot3': playerTopWeapons['topWeapon3']['body%'],
        'TopWeaponLegshot3': playerTopWeapons['topWeapon3']['leg%'],
        'TopWeaponKills3': playerTopWeapons['topWeapon3']['kills'],
        'TopMap1': playerTopMaps["topMap1"]["name"],
        'TopMapWinrate1': playerTopMaps["topMap1"]["winrate"],
        'TopMapWins1': playerTopMaps["topMap1"]["wins"],
        'TopMapLosses1': playerTopMaps["topMap1"]["loses"],
        'TopMap2': playerTopMaps["topMap2"]["name"],
        'TopMapWinrate2': playerTopMaps["topMap2"]["winrate"],
        'TopMapWins2': playerTopMaps["topMap2"]["wins"],
        'TopMapLosses2': playerTopMaps["topMap2"]["loses"],
        'TopMap3': playerTopMaps["topMap3"]["name"],
        'TopMapWinrate3': playerTopMaps["topMap3"]["winrate"],
        'TopMapWins3': playerTopMaps["topMap3"]["wins"],
        'TopMapLosses3': playerTopMaps["topMap3"]["loses"],
        'TopMap4': playerTopMaps["topMap4"]["name"],
        'TopMapWinrate4': playerTopMaps["topMap4"]["winrate"],
        'TopMapWins4': playerTopMaps["topMap4"]["wins"],
        'TopMapLosses4': playerTopMaps["topMap4"]["loses"],
        'TopMap5': playerTopMaps["topMap5"]["name"],
        'TopMapWinrate5': playerTopMaps["topMap5"]["winrate"],
        'TopMapWins5': playerTopMaps["topMap5"]["wins"],
        'TopMapLosses5': playerTopMaps["topMap5"]["loses"],
        'TopMap6': playerTopMaps["topMap6"]["name"],
        'TopMapWinrate6': playerTopMaps["topMap6"]["winrate"],
        'TopMapWins6': playerTopMaps["topMap6"]["wins"],
        'TopMapLosses6': playerTopMaps["topMap6"]["loses"],
        'TopMap7': playerTopMaps["topMap7"]["name"],
        'TopMapWinrate7': playerTopMaps["topMap7"]["winrate"],
        'TopMapWins7': playerTopMaps["topMap7"]["wins"],
        'TopMapLosses7': playerTopMaps["topMap7"]["loses"],
        'TopMap8': playerTopMaps["topMap8"]["name"],
        'TopMapWinrate8': playerTopMaps["topMap8"]["winrate"],
        'TopMapWins8': playerTopMaps["topMap8"]["wins"],
        'TopMapLosses8': playerTopMaps["topMap8"]["loses"],
        'TopMap9': playerTopMaps["topMap9"]["name"],
        'TopMapWinrate9': playerTopMaps["topMap9"]["winrate"],
        'TopMapWins9': playerTopMaps["topMap9"]["wins"],
        'TopMapLosses9': playerTopMaps["topMap9"]["loses"],
        'TopMap10': playerTopMaps["topMap10"]["name"],
        'TopMapWinrate10': playerTopMaps["topMap10"]["winrate"],
        'TopMapWins10': playerTopMaps["topMap10"]["wins"],
        'TopMapLosses10': playerTopMaps["topMap10"]["loses"],
        'views': view
    }
        

    print("Username: " + user + " #" + tag + "\n" + "Damage Round: " + playerDpR + "\n" + "K/D Ratio: " + playerKDR + "\n" + "Headshot: " + playerHeadRate + "\n" + "Win: " + playerWinRate + "\n" + "Wins: " + playerWins + "\n" + "KAST: " + playerKAST + "\n" + "DDA/Round: " + playerDDdeltaR + "\n" + "Kills: " + playerKills + "\n" + "Deaths: " +  playerDeaths + "\n" + "Assits: " + playerAssists + "\n" + "ACS: " + playerACS + "\n" + "KADRatio: " + playerKADRatio + "\n" + "Kills/Round: " + playerKillsPerRound + "\n" + "Clutches 1v1: " + playerClutch1v1 + "\n" + "Flawless: " + playerFlawless + "\n" + "Current Rating: " + playerCurrentRating + "\n" + "Peak Rating: " + playerPeakRating + "\n" + "Top Weapons: " + str(playerTopWeapons) + "\n" + "Top Maps: " + str(playerTopMaps) + "\n" + "Top Agents: " + str(playerTopAgents) + "\n" + "Playtime: " + playerPlaytime + "\n" + "Matches: " + playerMatches + "\n" + "Level: " + playerLevel + "\n" + "Losses: " + playerLosses + "\n" + "URL: " + url + "\n" + "Views: " + view + 
          "\nTop Map 1: " + playerData['TopMap1'] +
          "\nTop Map 1 Winrate: " + playerData['TopMapWinrate1'] +
          "\nTop Map 1 Wins: " + playerData['TopMapWins1'] +
          "\nTop Map 1 Losses: " + playerData['TopMapLosses1'] +
          "\nTop Map 2: " + playerData['TopMap2'] +
          "\nTop Map 2 Winrate: " + playerData['TopMapWinrate2'] +
          "\nTop Map 2 Wins: " + playerData['TopMapWins2'] +
          "\nTop Map 2 Losses: " + playerData['TopMapLosses2'] +
          "\nTop Map 3: " + playerData['TopMap3'] +
          "\nTop Map 3 Winrate: " + playerData['TopMapWinrate3'] +
          "\nTop Map 3 Wins: " + playerData['TopMapWins3'] +
          "\nTop Map 3 Losses: " + playerData['TopMapLosses3'] + 
          "\nTop Map 4: " + playerData['TopMap4'] +
          "\nTop Map 4 Winrate: " + playerData['TopMapWinrate4'] +
          "\nTop Map 4 Wins: " + playerData['TopMapWins4'] +
          "\nTop Map 4 Losses: " + playerData['TopMapLosses4'] +
          "\nTop Map 5: " + playerData['TopMap5'] +
          "\nTop Map 5 Winrate: " + playerData['TopMapWinrate5'] +
          "\nTop Map 5 Wins: " + playerData['TopMapWins5'] +
          "\nTop Map 5 Losses: " + playerData['TopMapLosses5'] +
          "\nTop Map 6: " + playerData['TopMap6'] +
          "\nTop Map 6 Winrate: " + playerData['TopMapWinrate6'] +
          "\nTop Map 6 Wins: " + playerData['TopMapWins6'] +
          "\nTop Map 6 Losses: " + playerData['TopMapLosses6'] +
          "\nTop Map 7: " + playerData['TopMap7'] +
          "\nTop Map 7 Winrate: " + playerData['TopMapWinrate7'] +
          "\nTop Map 7 Wins: " + playerData['TopMapWins7'] +
            "\nTop Map 7 Losses: " + playerData['TopMapLosses7'] +
            "\nTop Map 8: " + playerData['TopMap8'] +
            "\nTop Map 8 Winrate: " + playerData['TopMapWinrate8'] +
            "\nTop Map 8 Wins: " + playerData['TopMapWins8'] +
            "\nTop Map 8 Losses: " + playerData['TopMapLosses8'] +
            "\nTop Map 9: " + playerData['TopMap9'] +
            "\nTop Map 9 Winrate: " + playerData['TopMapWinrate9'] +
            "\nTop Map 9 Wins: " + playerData['TopMapWins9'] +
            "\nTop Map 9 Losses: " + playerData['TopMapLosses9'] +
            "\nTop Map 10: " + playerData['TopMap10'] +
            "\nTop Map 10 Winrate: " + playerData['TopMapWinrate10'] +
            "\nTop Map 10 Wins: " + playerData['TopMapWins10'] +
            "\nTop Map 10 Losses: " + playerData['TopMapLosses10']
          )

    inserir_dados(playerData)
    
    for key, value in playerData.items():
        print(f"{key}: {value}")
    driver.quit()
    return playerData

def numeroString(num):
    newstr = ""
    num = str(num)
    lennum = len(num)
    for i, letra in enumerate(num):
        if letra == '.' and lennum - (i+1) < 3:
            newstr += '.'
        elif letra.isdigit():
            newstr += letra
        else: pass
    newfloat = float(newstr)
    return newfloat

txtlst = os.listdir(os.path.join(scriptdir, 'Pages'))
for pg in txtlst:
    with open(os.path.join(scriptdir, 'Pages', pg), 'r', encoding='utf-8') as f:
        namelines = f.readlines()
    for line in namelines:
        username = line.split('USER: ')[1].split(';;;TAG: ')[0]
        tag = line.split(';;;TAG: ')[1].strip().replace('#', '')
        print(f"Scraping {username}#{tag}")
        try:
            testDict = scrapePlayer(username, tag)
            with open(os.path.join(scriptdir, 'Scrapes', f'{testDict["Username"].strip()}-{testDict["Tag"].strip()}.json'), 'w', encoding='utf-8') as f:
                f.write(json.dumps(testDict, indent=4))
        except AttributeError: 
            print(f'Pulando {username} {tag}')
            pass