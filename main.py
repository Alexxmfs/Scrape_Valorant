import re
import requests
from fake_useragent import UserAgent
from lxml import html
import pandas as pd


def pegaperfil(page_num):
    ua = UserAgent()
    usernames_with_tags = []

    response = requests.get(f'https://tracker.gg/valorant/leaderboards/ranked/all/default?page={page_num}&region=global&act=22d10d66-4d2a-a340-6c54-408c7bd53807', headers={'User-Agent': ua.random})
    tree = html.fromstring(response.content)

    rows = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[2]/div/div/div[1]/div[2]/table/tbody/tr')
    
    for row in rows:
        username = row.xpath('.//td[2]/div/a[1]/span/span[1]/text()')[0]
        tag = row.xpath('.//td[2]/div/a[1]/span/span[2]/text()')[0]
        usernames_with_tags.append(username + " " + tag)

    return usernames_with_tags

def preprocess_data(data):
    playtime_str = str(data['Playtime'])
    playtime_str = playtime_str.split()[0]  # Obtém apenas a primeira parte da string
    playtime_str = playtime_str.replace(',', '').replace('h', '').strip()  # Remove vírgulas e "h"
    playtime_numeric = float(playtime_str) / 1000  # Converte para float e divide por 1000 para ajustar para 3 casas decimais
    playtime_formatted = '{:.3f}'.format(playtime_numeric)  # Formata para exibir três casas decimais

    matches_str = str(data['Matches'])
    matches_str = matches_str.split()[0]  # Obtém apenas a primeira parte da string
    matches_str = matches_str.replace(',', '').replace('h', '').strip()  # Remove vírgulas e "h"
    matches_numeric = float(matches_str) / 1000  # Converte para float e divide por 1000 para ajustar para 3 casas decimais
    matches_formatted = '{:.3f}'.format(matches_numeric)  # Formata para exibir três casas decimais

    wins_str = str(data['Wins'])
    wins_str = wins_str.split()[0]  # Obtém apenas a primeira parte da string
    wins_str = wins_str.replace(',', '').replace('h', '').strip()  # Remove vírgulas e "h"
    win_numeric = float(wins_str) / 1000  # Converte para float e divide por 1000 para ajustar para 3 casas decimais
    wins_formatted = '{:.3f}'.format(win_numeric)  # Formata para exibir três casas decimais

    kills_str = str(data['Kills'])
    kills_str = kills_str.split()[0]  # Obtém apenas a primeira parte da string
    kills_str = kills_str.replace(',', '').replace('h', '').strip()  # Remove vírgulas e "h"
    kills_numeric = float(kills_str) / 1000  # Converte para float e divide por 1000 para ajustar para 3 casas decimais
    kills_formatted = '{:.3f}'.format(kills_numeric)  # Formata para exibir três casas decimais

    deaths = str(data['Deaths'])
    deaths = deaths.split()[0]  # Obtém apenas a primeira parte da string
    deaths = deaths.replace(',', '').replace('h', '').strip()  # Remove vírgulas e "h"
    deaths_numeric = float(deaths) / 1000  # Converte para float e divide por 1000 para ajustar para 3 casas decimais
    deaths_formatted = '{:.3f}'.format(deaths_numeric)  # Formata para exibir três casas decimais

    assists = str(data['Assists'])
    assists = assists.split()[0]  # Obtém apenas a primeira parte da string
    assists = assists.replace(',', '').replace('h', '').strip()  # Remove vírgulas e "h"
    assists_numeric = float(assists) / 1000  # Converte para float e divide por 1000 para ajustar para 3 casas decimais
    assists_formatted = '{:.3f}'.format(assists_numeric)  # Formata para exibir três casas decimais


    
    processed_data = {
        'username': str(data['Username']).lstrip('0').strip() if str(data['Username']).strip().startswith('0') else str(data['Username']).strip(),
        'tag': str(data['Tag']).strip() if str(data['Tag']).strip() else str(data['Tag']).strip(),
        'playtime': playtime_formatted,
        "matches": matches_formatted,
        'rating': str(data['Rating']).replace(',', '.').lstrip('0').strip() if str(data['Rating']).strip().startswith('0') else str(data['Rating']).replace(',', '.').strip(),
        'level': str(data['Level']).replace(',', '.').lstrip('0').strip() if str(data['Level']).strip().startswith('0') else str(data['Level']).replace(',', '.').strip(),
        'loses': str(data['Loses']).replace(',', '.').lstrip('0').strip() if str(data['Loses']).strip().startswith('0') else str(data['Loses']).replace(',', '.').strip(),
        'damage_round': str(data['Damage_round']).replace(',', '.').lstrip('0').strip() if str(data['Damage_round']).strip().startswith('0') else str(data['Damage_round']).replace(',', '.').strip(),
        'headshot': str(data['Headshot']).replace(',', '.').lstrip('0').strip() if str(data['Headshot']).strip().startswith('0') else str(data['Headshot']).replace(',', '.').strip(),
        'win': str(data['Win']).strip() if str(data['Win']).strip().startswith('0') else str(data['Win']).strip(),
        "wins": wins_formatted,
        "kills": kills_formatted,
        "deaths": deaths_formatted,
        "assists": assists_formatted,   
        "kad_ratio": str(data['kad_ratio'][0]).lstrip('0').strip("[]") if isinstance(data['kad_ratio'], list) else str(data['kad_ratio']).lstrip('0').strip() if str(data['kad_ratio']).strip().startswith('0') else str(data['kad_ratio']).strip(),
        'kills_round': str(data['kills_round']).lstrip("['").rstrip("']"),
        'clutches': str(data['Clutches']).lstrip("['").rstrip("']").replace(",", "."),
        'top_agents_1': str(data['Top_agents_1']).lstrip("['").rstrip("']"),

        'top_hours_agent_1': str(data['top_hours_agent_1']).replace("['", "").replace("']", "").replace(" hours", "").replace(",", ".").strip() if str(data['top_hours_agent_1']).strip() != 'null' else '',
        'top_matches_agent_1': str(data['top_matches_agent_1']).replace("['", '').replace("']", '').replace(",", ".").strip() if str(data['top_matches_agent_1']).strip() != 'null' else '',
        'top_win_agent_1': str(data['top_win_agent_1']).replace('[', '').replace(']', '').strip() if str(data['top_win_agent_1']).strip() != 'null' else '',
        'top_kd_agent_1': str(data['top_kd_agent_1']).replace("['", '').replace("']", '').strip() if str(data['top_kd_agent_1']).strip() != 'null' else '',

        'top_weapon_1': str(data['top_weapon_1']).strip() if str(data['top_weapon_1']).strip() != 'None' else '0',
        'top_weapon_headshot_1': str(data['top_weapon_headshot_1']).replace('[', '').replace(']', '').strip() if str(data['top_weapon_headshot_1']).strip() != 'None' else '0',
        'top_weapon_2': str(data['top_weapon_2']).strip() if str(data['top_weapon_2']).strip() != 'None' else '',
        'top_weapon_headshot_2': str(data['top_weapon_headshot_2']).replace('[', '').replace(']', '').strip() if str(data['top_weapon_headshot_2']).strip() != 'None' else '0',
        'top_maps_1': str(data['top_maps_1']).strip() if str(data['top_maps_1']).strip() != 'None' else '',
        'top_porcentagem_map_win_1': str(data['top_porcentagem_map_win_1']).replace('[', '').replace(']', '').strip() if str(data['top_porcentagem_map_win_1']).strip() != 'None' else '0',
    }
    print("Processed Data:", processed_data)
    return processed_data        # 'tag': str(data['Tag']).strip(),

def inserir_dados(data):
    try:
        url = 'http://localhost:8080/jogador/criar-jogador'
        
        # Pré-processamento dos dados
        for index, row in data.iterrows():
            user_data = row.to_dict()
            processed_data = preprocess_data(user_data)
            response = requests.post(url, json=processed_data)
            print(response.text)  
    except Exception as e:
        print("Erro ao inserir os dados:", e)

def pegaviews(usernames_with_tags, page_num):
    ua = UserAgent()
    total_data = len(usernames_with_tags)
    data = []

    for current_data, user_with_tag in enumerate(usernames_with_tags, 1):
        match = re.match(r'(.+)\s#(.+)', user_with_tag)
        if match:
            username = match.group(1)
            tag = match.group(2)
        else:
            print(f"Erro ao separar o username e a tag para: {user_with_tag}")
            continue

        response = requests.get(f'https://tracker.gg/valorant/profile/riot/{username}%23{tag}/overview?season=all', headers={'User-Agent': ua.random})
        tree = html.fromstring(response.content)

        views = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[1]/div[2]/div[2]/div[1]/span/span/span/text()')
        views_count = views[0] if views else None

        response = requests.get(f'https://tracker.gg/valorant/profile/riot/{username}%23{tag}/overview?season=all', headers={'User-Agent': ua.random})
        tree = html.fromstring(response.content)

        views = tree.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[1]/div[2]/div[2]/div[1]/span/span/span/text()')
        views_count = views[0] if views else None

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

        current_index = (current_data - 1) % 100 + 1
        print(f"Dados coletados: {username}#{tag} - Dado {current_index}/{total_data} - Página {page_num}")


        inserir_dados(pd.DataFrame([user_data]))

    return pd.DataFrame(data)

def main():
    total_pages = 434  
    for page_num in range(1, total_pages + 1):  
 
        usernames_with_tags = pegaperfil(page_num)
        for i in range(0, len(usernames_with_tags), 100):
            batch_usernames = usernames_with_tags[i:i+100]  
            usuarios_com_visualizacoes = pegaviews(batch_usernames, page_num)

if __name__ == "__main__":
    main()
