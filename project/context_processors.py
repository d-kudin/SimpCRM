# project/context-processors.py

import os
import logging
import requests
from datetime import datetime
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

def weather_context(request):
    api_key = os.getenv("WEATHER_API")
    city = "Warsaw"
    weather = {
        "temperature": "N/A",
        "description": "N/A",
        "city": "N/A"
    }

    if not api_key:
        logger.warning("WEATHER_API key is missing in environment variables.")
        return {"weather": weather}

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=en&appid={api_key}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        weather = {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "city": data["name"]
        }
    except requests.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")

    return {"weather": weather}


def holiday_context(request):
    api_key = os.getenv("HOLIDAY_API")
    country_code = 'PL'  # Country code for Poland
    year = datetime.now().year - 1  # Specify the year for which you want to fetch holiday data
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
        print(f"Error fetching holiday data: {e}")

    return {'holidays': holidays}