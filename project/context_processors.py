import requests
from datetime import datetime

def weather_context(request):
    api_key = '01da91d1819f2d67733e0d2c76216220'
    city = 'Warsaw'
    weather = {
        'temperature': 'N/A',
        'description': 'N/A',
        'city': 'N/A'
    }
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=pl&appid={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'city': data['name']
            }
    except requests.RequestException as e:
        print(f"Błąd podczas pobierania danych o pogodzie: {e}")
    
    return {'weather': weather}


def holiday_context(request):
    api_key = '2bad7814-d5e2-41a0-ad82-9803edabac80'
    country_code = 'PL'  # Country code for Poland
    year = 2023  # Specify the year for which you want to fetch holiday data
    current_month = datetime.now().month
    current_day = datetime.now().day
    url = f"https://holidayapi.com/v1/holidays?pretty&key={api_key}&language=pl&country={country_code}&year={year}"
    holidays = []

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            all_holidays = data.get('holidays', [])

            for holiday_info in all_holidays:
                holiday_date = holiday_info['date']
                holiday_month = int(holiday_date.split('-')[1])
                holiday_day = int(holiday_date.split('-')[2])
                
                if holiday_month == current_month and holiday_day == current_day:
                    holidays.append({'date': holiday_date, 'name': holiday_info['name']})
    
    except requests.RequestException as e:
        print(f"Błąd podczas pobierania danych o świętach: {e}")

    return {'holidays': holidays}
