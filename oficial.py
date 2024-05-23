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
            'dpR': data['DpR'],
            'kdr': data['KDR'],
            'headshot': data['Headshot%'],
            'win': data['Win%'],
            'wins': data['Wins'],
            'kast': data['KAST'],
            'dddeltaR': data['DDdeltaR'],
            'kills': data['Kills'],
            'deaths': data['Deaths'],
            'assists': data['Assists'],
            'acs': data['ACS'],
            'kadRatio': data['KADRatio'],
            'killsPerRound': data['KillsPerRound'],
            'clutch1v1s': data['Clutch1v1s'],
            'flawlessRounds': data['FlawlessRounds'],
            'currentRating': data['CurrentRating'],
            'peakRating': data['PeakRating'],
            'playtime': data['Playtime'],
            'matches': data['Matches'],
            'level': data['Level'],
            'losses': data['Losses'],
            'topAgent1': data['TopAgent1'],
            'topAgent2': data['TopAgent2'],
            'topAgent3': data['TopAgent3'],
            'topHoursAgent1': data['TopHoursAgent1'],
            'topHoursAgent2': data['TopHoursAgent2'],
            'topHoursAgent3': data['TopHoursAgent3'],
            'topMatchesAgent1': data['TopMatchesAgent1'],
            'topMatchesAgent2': data['TopMatchesAgent2'],
            'topMatchesAgent3': data['TopMatchesAgent3'],
            'topWinAgent1': data['TopWinAgent1'],
            'topWinAgent2': data['TopWinAgent2'],
            'topWinAgent3': data['TopWinAgent3'],
            'topKDAgent1': data['TopKDAgent1'],
            'topKDAgent2': data['TopKDAgent2'],
            'topKDAgent3': data['TopKDAgent3'],
            'topWeapon1': data['TopWeapon1'],
            'topWeaponHeadshot1': data['TopWeaponHeadshot1'],
            'topWeapon2': data['TopWeapon2'],
            'topWeaponHeadshot2': data['TopWeaponHeadshot2'],
            'topWeapon3': data['TopWeapon3'],
            'topWeaponHeadshot3': data['TopWeaponHeadshot3'],
            'topMap1': data['TopMap1'],
            'topMapWinrate1': data['TopMapWinrate1'],
            'topMapWins1': data['TopMapWins1'],
            'topMapLosses1': data['TopMapLosses1'],
            'topMap2': data['TopMap2'],
            'topMapWinrate2': data['TopMapWinrate2'],
            'topMapWins2': data['TopMapWins2'],
            'topMapLosses2': data['TopMapLosses2'],
            'topMap3': data['TopMap3'],
            'topMapWinrate3': data['TopMapWinrate3'],
            'topMapWins3': data['TopMapWins3'],
            'topMapLosses3': data['TopMapLosses3'],
            'topMap4': data['TopMap4'],
            'topMapWinrate4': data['TopMapWinrate4'],
            'topMapWins4': data['TopMapWins4'],
            'topMapLosses4': data['TopMapLosses4'],
            'topMap5': data['TopMap5'],
            'topMapWinrate5': data['TopMapWinrate5'],
            'topMapWins5': data['TopMapWins5'],
            'topMapLosses5': data['TopMapLosses5'],
            'views': data['views']
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
        'TopWeapon2': playerTopWeapons['topWeapon2']['name'],
        'TopWeaponHeadshot2': playerTopWeapons['topWeapon2']['head%'],
        'TopWeapon3': playerTopWeapons['topWeapon3']['name'],
        'TopWeaponHeadshot3': playerTopWeapons['topWeapon3']['head%'],
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
          "\nTop Map 5 Losses: " + playerData['TopMapLosses5'])

    inserir_dados(playerData)
    
    for key, value in playerData.items():
        print(f"{key}: {value}")
    driver.quit()
    return playerData

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