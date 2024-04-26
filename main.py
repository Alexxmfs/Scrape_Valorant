import re
import requests
from fake_useragent import UserAgent
from lxml import html
import pandas as pd
import threading
#from fp.fp import FreeProxy
#import ssl



def pegausertag(rowo):
    try:
        username = rowo.xpath('.//td[2]/div/a[1]/span/span[1]/text()')[0]
        tag = rowo.xpath('.//td[2]/div/a[1]/span/span[2]/text()')[0]
        return (username, tag)
    except IndexError:
        return ('', '')

def pegaperfil(page_num):
    ua = UserAgent()
    usernames_with_tags = []
    proxy = None
    #proxy = FreeProxy(rand=True, timeout=1, https=True).get()
    response = requests.get(f'https://tracker.gg/valorant/leaderboards/ranked/all/default?page={page_num}&region=global&act=22d10d66-4d2a-a340-6c54-408c7bd53807', headers={'User-Agent': ua.random}, proxies=proxy)
    tree = html.fromstring(response.content)

    rows = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[2]/div/div/div[1]/div[2]/table/tbody/tr')
    
    for row in rows:
        (username, tag) = pegausertag(row)
        if username != '' and tag != '':
            usernames_with_tags.append(username + " " + tag)

    return usernames_with_tags

def preprocess_data(data):
    if 'Playtime' in list(data.keys()):
        playtime_str = str(data['Playtime'])
        playtime_str = playtime_str.split()[0]  # Obtém apenas a primeira parte da string
        playtime_str = playtime_str.replace(',', '').replace('h', '').strip()  # Remove vírgulas e "h"
        playtime_numeric = float(playtime_str) # Converte para float e divide por 1000 para ajustar para 3 casas decimais
        playtime_formatted = str(playtime_numeric)  # Formata para exibir três casas decimais
    
    if 'Matches' in list(data.keys()):
        matches_str = str(data['Matches'])
        if ' M' in matches_str:  # Caso a string seja "0.0 M"
            matches_str = matches_str.split(' M')[0]
        matches_str = matches_str.replace(',', '').replace('h', '').strip()  # Remove vírgulas e "h"
        matches_numeric = float(matches_str)  # Converte para float e divide por 1000 para ajustar para 3 casas decimais
        matches_formatted = str(matches_numeric)  # Formata para exibir três casas decimais

    if 'Wins' in list(data.keys()):
        wins_str = str(data['Wins'])
        wins_str = wins_str.split()[0]  # Obtém apenas a primeira parte da string
        wins_str = wins_str.replace(',', '').replace('h', '').strip()  # Remove vírgulas e "h"
        win_numeric = float(wins_str) # Converte para float e divide por 1000 para ajustar para 3 casas decimais
        wins_formatted = str(win_numeric)  # Formata para exibir três casas decimais

    if 'Kills' in list(data.keys()):
        kills_str = str(data['Kills'])
        kills_str = kills_str.split()[0]  # Obtém apenas a primeira parte da string
        kills_str = kills_str.replace(',', '').replace('h', '').strip()  # Remove vírgulas e "h"
        kills_numeric = float(kills_str) / 1000  # Converte para float e divide por 1000 para ajustar para 3 casas decimais
        kills_formatted = '{:.3f}'.format(kills_numeric)  # Formata para exibir três casas decimais

    if 'Deaths' in list(data.keys()):
        deaths = str(data['Deaths'])
        deaths = deaths.split()[0]  # Obtém apenas a primeira parte da string
        deaths = deaths.replace(',', '').replace('h', '').strip()  # Remove vírgulas e "h"
        deaths_numeric = float(deaths) / 1000  # Converte para float e divide por 1000 para ajustar para 3 casas decimais
        deaths_formatted = '{:.3f}'.format(deaths_numeric)  # Formata para exibir três casas decimais

    if 'Assists' in list(data.keys()):
        assists = str(data['Assists'])
        assists = assists.split()[0]  # Obtém apenas a primeira parte da string
        assists = assists.replace(',', '').replace('h', '').strip()  # Remove vírgulas e "h"
        assists_numeric = float(assists) / 1000  # Converte para float e divide por 1000 para ajustar para 3 casas decimais
        assists_formatted = '{:.3f}'.format(assists_numeric)  # Formata para exibir três casas decimais


    
    processed_data = {}
    
    if 'Username' in list(data.keys()):
        processed_data.update({'username': str(data['Username']).lstrip('0').strip() if str(data['Username']).strip().startswith('0') else str(data['Username']).strip()})
    
    if 'Tag' in list(data.keys()):
        processed_data.update({'tag': str(data['Tag']).strip() if str(data['Tag']).strip() else str(data['Tag']).strip()})
    
    if 'Playtime' in list(data.keys()):
        processed_data.update({'playtime': playtime_formatted})
    
    if 'Matches' in list(data.keys()):
        processed_data.update({'matches': matches_formatted})
    
    if 'Rating' in list(data.keys()):
        processed_data.update({'rating': str(data['Rating']).replace(',', '.').lstrip('0').strip() if str(data['Rating']).strip().startswith('0') else str(data['Rating']).replace(',', '.').strip()})
    
    if 'Level' in list(data.keys()):
        processed_data.update({'level': str(data['Level']).lstrip('0').strip() if str(data['Level']).strip().startswith('0') else str(data['Level']).strip()})
    
    if 'Loses' in list(data.keys()):
        processed_data.update({'loses': str(data['Loses']).replace(',', '.').lstrip('0').strip() if str(data['Loses']).strip().startswith('0') else str(data['Loses']).replace(',', '.').strip()})
    
    if 'Damage_round' in list(data.keys()):
        processed_data.update({'damage_round': str(data['Damage_round']).replace(',', '.').lstrip('0').strip() if str(data['Damage_round']).strip().startswith('0') else str(data['Damage_round']).replace(',', '.').strip()})
    
    if 'Headshot' in list(data.keys()):
        processed_data.update({'headshot': str(data['Headshot']).replace(',', '.').lstrip('0').strip() if str(data['Headshot']).strip().startswith('0') else str(data['Headshot']).replace(',', '.').strip()})
    
    if 'Win' in list(data.keys()):
        processed_data.update({'win': str(data['Win']).strip() if str(data['Win']).strip().startswith('0') else str(data['Win']).strip()})
    
    if 'Wins' in list(data.keys()):
        processed_data.update({'wins': wins_formatted})
    
    if 'Kills' in list(data.keys()):
        processed_data.update({'kills': kills_formatted})
    
    if 'Deaths' in list(data.keys()):
        processed_data.update({'deaths': deaths_formatted})
    
    if 'Assists' in list(data.keys()):
        processed_data.update({'assists': assists_formatted})
    
    if 'kad_ratio' in list(data.keys()):
        processed_data.update({"kad_ratio": str(data['kad_ratio'][0]).lstrip('0').strip("[]") if isinstance(data['kad_ratio'], list) else str(data['kad_ratio']).lstrip('0').strip() if str(data['kad_ratio']).strip().startswith('0') else str(data['kad_ratio']).strip()})
    
    if 'kills_round' in list(data.keys()):
        processed_data.update({'kills_round': str(data['kills_round']).lstrip("['").rstrip("']")})
    
    if 'Clutches' in list(data.keys()):
        processed_data.update({'clutches': str(data['Clutches']).lstrip("['").rstrip("']").replace(",", ".")})
    
    if 'Top_agents_1' in list(data.keys()):
        processed_data.update({'top_agents_1': str(data['Top_agents_1']).lstrip("['").rstrip("']")})
    
    if 'top_hours_agent_1' in list(data.keys()):
        processed_data.update({'top_hours_agent_1': str(data['top_hours_agent_1']).replace("['", "").replace("']", "").replace(" hours", "").replace(",", ".").strip() if str(data['top_hours_agent_1']).strip() != 'null' else ''})
    
    if 'top_matches_agent_1' in list(data.keys()):
        processed_data.update({'top_matches_agent_1': str(data['top_matches_agent_1']).replace("['", '').replace("']", '').replace(",", ".").strip() if str(data['top_matches_agent_1']).strip() != 'null' else ''})
    
    if 'top_win_agent_1' in list(data.keys()):
        processed_data.update({'top_win_agent_1': str(data['top_win_agent_1']).replace('[', '').replace(']', '').strip() if str(data['top_win_agent_1']).strip() != 'null' else ''})
    
    if 'top_kd_agent_1' in list(data.keys()):
        processed_data.update({'top_kd_agent_1': str(data['top_kd_agent_1']).replace("['", '').replace("']", '').strip() if str(data['top_kd_agent_1']).strip() != 'null' else ''})
    
    if 'top_weapon_1' in list(data.keys()):
        processed_data.update({'top_weapon_1': str(data['top_weapon_1']).strip() if str(data['top_weapon_1']).strip() != 'None' else '0'})
    
    if 'top_weapon_headshot_1' in list(data.keys()):
        processed_data.update({'top_weapon_headshot_1': str(data['top_weapon_headshot_1']).replace('[', '').replace(']', '').strip() if str(data['top_weapon_headshot_1']).strip() != 'None' else '0'})
    
    if 'top_weapon_2' in list(data.keys()):
        processed_data.update({'top_weapon_2': str(data['top_weapon_2']).strip() if str(data['top_weapon_2']).strip() != 'None' else ''})
    
    if 'top_weapon_headshot_2' in list(data.keys()):
        processed_data.update({'top_weapon_headshot_2': str(data['top_weapon_headshot_2']).replace('[', '').replace(']', '').strip() if str(data['top_weapon_headshot_2']).strip() != 'None' else '0'})
    
    if 'top_maps_1' in list(data.keys()):
        processed_data.update({'top_maps_1': str(data['top_maps_1']).strip() if str(data['top_maps_1']).strip() != 'None' else ''})
    
    if 'top_porcentagem_map_win_1' in list(data.keys()):
        processed_data.update({'top_porcentagem_map_win_1': str(data['top_porcentagem_map_win_1']).replace('[', '').replace(']', '').strip() if str(data['top_porcentagem_map_win_1']).strip() != 'None' else '0'})
    
    print("Processed Data:", processed_data)
    return processed_data        # 'tag': str(data['Tag']).strip(),

def inserir_dados(data):
    print("Inserindo")
    try:
        url = 'http://localhost:8080/jogador/criar-jogador'
        
        # Pré-processamento dos dados
        for index, row in data.iterrows():
            user_data = row.to_dict()
            processed_data = preprocess_data(user_data)
            response = requests.post(url, json=processed_data)
            print(response.text)  
    except Exception as e:
        print("Erro ao inserir os dados:", e, str(data))

def pegaviews(usernames_with_tags, page_num):
    global dthreads
    ua = UserAgent()
    total_data = len(usernames_with_tags)
    data = []

    for current_data, user_with_tag in enumerate(usernames_with_tags, 1):
        for letnum in range(-1, (len(user_with_tag)*(-1)), -1):
            letter = user_with_tag[letnum]
            if letter == '#':
                username = user_with_tag[:letnum].strip()
                tag = user_with_tag[letnum+1:].strip()
                user_data = {
                    'Username': username,
                    'Tag': tag
                }
                data.append(user_data)
        current_index = (current_data - 1) % 100 + 1
        print(f"Dados coletados: {username}#{tag} - Dado {current_index}/{total_data} - Página {page_num}")
    return pd.DataFrame(data)

def raspar_nome(user_with_tag):
    try:
        ua = UserAgent()
        for letnum in range(-1, (len(user_with_tag)*(-1)), -1):
            letter = user_with_tag[letnum]
            if letter == '#':
                username = user_with_tag[:letnum].strip()
                tag = user_with_tag[letnum+1:].strip()
                break

        response = requests.get(f'https://tracker.gg/valorant/profile/riot/{username}%23{tag}/overview?season=all', headers={'User-Agent': ua.random})
        tree = html.fromstring(response.content)

        views = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[1]/div[2]/div[2]/div[1]/span/span/span/text()')
        views_count = views[0] if views else None

        playtime = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/div/div/span[1]/text()')
        playtime_count = playtime[0] if playtime else None
        
        matches = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/div/div/span[2]/text()')
        matches_count = matches[0] if matches else None
        
        rating = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/div/div[1]/span[2]/text()')
        rating_count = rating[0] if rating else None

        level = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/span[2]/text()')
        level_count = level[0] if level else None

        loses = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/div/div[3]/svg/g[2]/text[2]/text()')
        loses_count = loses[0] if loses else None

        damage_round = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/span[2]/span/text()')
        damage_round_count = damage_round[0] if damage_round else None

        headshot = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/span[2]/span/text()')
        headshot_count = headshot[0] if headshot else None

        win = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/span[2]/span/text()')
        win_count = win[0] if win else None

        wins = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[5]/div[1]/div/div[2]/span[2]/span/text()')
        wins_count = wins[0] if wins else None

        kills = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[5]/div[4]/div/div[2]/span[2]/span/text()')
        kills_count = kills[0] if kills else None

        deaths = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[5]/div[5]/div/div[1]/span[2]/span/text()')
        deaths_count = deaths[0] if deaths else None

        assists = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[5]/div[6]/div/div[1]/span[2]/span/text()')
        assists_count = assists[0] if assists else None

        kad_ratio = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[5]/div[8]/div/div[1]/span[2]/span/text()')
        kad_ratio_count = kad_ratio if kad_ratio else None

        kills_round = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[5]/div[9]/div/div[1]/span[2]/span/text()')
        kills_round_count = kills_round if kills_round else None

        clutches = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[1]/div/div[5]/div[10]/div/div[1]/span[2]/span/text()')
        clutches_count = clutches if clutches else None

        top_agents1 = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/text()')
        top_agents1_count = top_agents1 if top_agents1 else None 

        top_hours_agent1 = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/text()')
        top_hours_agent1_count = top_hours_agent1 if top_hours_agent1 else None

        top_matches_agent1 = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/text()')
        top_matches_agent1_count = top_matches_agent1 if top_matches_agent1 else None

        top_win_agent1 = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[3]/div/div/text()')
        top_win_agent1_count = top_win_agent1[0] if top_win_agent1 else None

        top_KD_agent1 = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[4]/div/div/text()')
        top_KD_agent1_count = top_KD_agent1 if top_KD_agent1 else None


        top_weapon1 = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[1]/div[4]/div/div[1]/div[1]/div[1]/text()')
        top_weapon1_count = top_weapon1[0] if top_weapon1 else None

        top_weapon_headshot1 = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[1]/div[4]/div/div[1]/div[2]/div/span[1]/text()')
        top_weapon_headshot1_count = top_weapon_headshot1[0] if top_weapon_headshot1 else None

        top_weapon2 = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[1]/div[4]/div/div[2]/div[1]/div[1]/text()')
        top_weapon2_count = top_weapon2[0] if top_weapon2 else None

        top_weapon_headshot2 = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[1]/div[4]/div/div[2]/div[2]/div/span[1]/text()')
        top_weapon_headshot2_count = top_weapon_headshot2[0] if top_weapon_headshot2 else None

        top_maps_1 = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[1]/div[5]/div/div[2]/div[1]/text()')
        top_maps_1_count = top_maps_1[0] if top_maps_1 else None

        top_porcen_map_win1 = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div[1]/div[5]/div/div[2]/div[2]/div[1]/text()')
        top_porcen_map_win1_count = top_porcen_map_win1[0] if top_porcen_map_win1 else None

        data = []
        user_data = {
            'Username': username,
            'Tag': tag,
            'Views': views_count,
            'Playtime': playtime_count,
            'Matches': matches_count,
            'Rating': rating_count,
            'Level': level_count,
            'Loses': loses_count,
            'Damage_round': damage_round_count,
            'Headshot': headshot_count,
            'Win': win_count,
            'Wins': wins_count,
            'Kills': kills_count,
            'Deaths': deaths_count,
            'Assists': assists_count,
            'kad_ratio': kad_ratio_count,
            'kills_round': kills_round_count,
            'Clutches': clutches_count,
            'Top_agents_1': top_agents1_count,
            'top_hours_agent_1': top_hours_agent1_count,
            'top_matches_agent_1': top_matches_agent1_count,
            'top_win_agent_1': top_win_agent1_count,
            'top_kd_agent_1': top_KD_agent1_count,
            'top_weapon_1': top_weapon1_count,
            'top_weapon_headshot_1': top_weapon_headshot1_count,
            'top_weapon_2': top_weapon2_count,
            'top_weapon_headshot_2': top_weapon_headshot2_count,
            'top_maps_1': top_maps_1_count,
            'top_porcentagem_map_win_1': top_porcen_map_win1_count
        }
        data.append(user_data)
        print(f"Dados coletados: {username}#{tag}")

        inserir_dados(pd.DataFrame([user_data]))
    except Exception as e:
        print("Erro ao raspar os dados:", e)

threads = []
dthreads = []
def main(start_page, end_page):
    global threads
    for page_num in range(start_page, end_page + 1):  
        print('pegaperfil start')
        for attempt in range(10):
            print(f"Tentativa {attempt + 1}")
            usernames_with_tags = pegaperfil(page_num)
            if len(usernames_with_tags) > 0:
                print('Sucesso')
                break
            else:
                print('Falha')
        print('pegaperfil end')
        for i in range(0, len(usernames_with_tags), 100):
            batch_usernames = usernames_with_tags[i:i+100]
            viewsthread = threading.Thread(target=pegaviews, args=(batch_usernames, page_num))
            threads = []
            threads.append(viewsthread)
            for user in batch_usernames:
                print(user)
                usthread = threading.Thread(target=raspar_nome, args=(str(user),))
                threads.append(usthread)
                usthread.start()
            viewsthread.start()
            for thread in threads:
                thread.join()




if __name__ == "__main__":
    start_page = 1
    end_page = 434
    main(start_page, end_page)