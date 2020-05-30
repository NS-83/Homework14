from requests_html import HTMLSession
from bs4 import BeautifulSoup

SITE_URL = 'https://understat.com/'
LEAGUES = ('EPL', 'La_liga', 'Bundesliga', 'Serie_A', 'Ligue_1', 'RFPL')


def get_league_data(league_number):
    result = {'data': {'games_data': [], 'league_table': []}, 'errors': []}
    session = HTMLSession()
    response = session.get(SITE_URL)
    if response.status_code != 200:
        result['errors'].append(f'Не удалось получить данные с сайта: {response.reason}')
        return result
    else:
        soup = BeautifulSoup(response.html.html, 'html.parser')
        links = soup.find_all('a', class_='link')
        league_link = ''
        for link in links:
            if link.text == LEAGUES[league_number]:
                league_link = link.get('href')
        league_data_link = f'{SITE_URL}{league_link}'
        response = session.get(league_data_link)
        response.html.render()
        league_soup = BeautifulSoup(response.html.html, 'html.parser')
        calendar_dates = league_soup.find_all('div', class_='calendar-date-container')
        for calendar_date in calendar_dates:
            games_date = date_format(calendar_date.contents[0].text)
            games = calendar_date.find_all('div', class_='calendar-game')
            for game in games:
                goals_information = game.contents[1].contents[0]
                is_result = game.contents[1].get('data-isresult') == 'true'
                game_data = {
                'game_date': games_date,
                'is_result': is_result,
                'home_team': game.contents[0].text,
                'away_team': game.contents[2].text,
                'home_goals': goals_information.contents[0].text if is_result else 0,
                'away_goals': goals_information.contents[1].text if is_result else 0
                }
                result['data']['games_data'].append(game_data)
        league_table = league_soup.find('table')
        teams_data = league_table.find_all('tr')
        for i in range(1,len(teams_data)):
            team_data = teams_data[i].contents
            team_data_dict = {'team': team_data[1].text,
                              'games': team_data[2].text,
                              'wins': team_data[3].text,
                              'loses': team_data[4].text,
                              'draws': team_data[5].text,
                              'points': team_data[8].text,
                              }
            result['data']['league_table'].append(team_data_dict)
    return result


def date_format(date_string):
    months_dict = {'January': '01',
                   'February': '02',
                   'March': '03',
                   'April': '04',
                   'May': '05',
                   'June': '06',
                   'July': '07',
                   'August': '08',
                   'September': '09',
                   'October': '10',
                   'November': '11',
                   'December': '12',
                   }
    date_string = 'Tuesday, May 26, 2020'
    date_string_parts = date_string.split(',')
    date_string_parts = list(map(lambda x: x.strip(), date_string_parts))
    date_year = date_string_parts[2]
    date_day_parts = date_string_parts[1].split(' ')
    date_month = months_dict[date_day_parts[0]]
    return f'{date_string_parts[2]}.{date_month}.{date_day_parts[1]}'