import json
from data_parser import get_league_data

print('1) EPL (Англия)')
print('2) La Liga (Испания)')
print('3) Bundesliga (Германия)')
print('4) Serie A (Италия)')
print('5) Ligue 1 (Франция)')
print('6) RFPL (Россия)')

league_number = 0
while league_number not  in range(1, 7):
    try:
        league_number = int(input('Введите номер лиги:'))
    except:
        pass
result = get_league_data(league_number-1)
if result['errors']:
    for error_text in result['errors']:
        print(error_text)
else:
    if result['data']['games_data']:
        with open('fixtures.json', 'w') as file:
            json.dump(result['data']['games_data'], file, indent=4)
            print('Сформирован файл с данными матчей fixtures.json')
    if result['data']['league_table']:
        with open('table.json', 'w') as file:
            json.dump(result['data']['league_table'], file, indent=4)
            print('Сформирован файл с данными матчей table.json')