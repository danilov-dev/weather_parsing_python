import datetime
import json
from typing import Optional

import requests
from bs4 import BeautifulSoup

from app.models.day import Day
from app.models.weather import Weather
from app.utils.date_converter import DateConverter


class Parser:
    def __init__(self, url: str):
        self.url = url
        self._soup = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
        }

    def _get_soup(self):
        if self._soup is None:
            try:
                response = requests.get(self.url, headers=self.headers, timeout=15)
                self._soup = BeautifulSoup(response.content, 'html.parser')
            except requests.exceptions.RequestException as e:
                raise e



    def _get_weather(self, table) -> Optional[Day]:
        if len(table) < 1 or table is None:
            return None

        periods = ['night', 'morning', 'day', 'evening']

        date_text = table.find("div", class_="dates").text
        converted_date = DateConverter.get_date(date_text)

        if converted_date is None:
            return None

        day = Day(converted_date)

        for period in periods:
            period_row = table.find("tr", class_=f"{period}")

            if period_row:
                cells = period_row.find_all("td")
                if len(cells) >= 7:
                    wind_span = period_row.find('span', class_="wwi")
                    wind_direction = wind_span.get('title') if wind_span else None

                    weather = Weather(
                        period=period,
                        temp=cells[1].text.strip(),
                        fells_like=cells[2].text.strip(),
                        probability=cells[3].text.strip(),
                        pressure=cells[4].text.strip(),
                        wind={
                            'direction': wind_direction,
                            'speed': cells[5].text.strip(),
                        },
                        humidity=cells[6].text.strip(),
                    )
                    day.weather.append(weather)

        if not day.weather:
            return None

        return day

    def _parse_weather_table(self) -> dict:
        self._get_soup()
        tables = self._soup.find_all("div", class_="weather-short")
        if len(tables) < 1:
            return {}
        days = {}
        for table in tables:
            day = self._get_weather(table)
            if day:
                days[day.date] = day.to_dict()

        return days

    def parse(self) -> Optional[str]:
        self._get_soup()
        weather_data = self._parse_weather_table()

        if not weather_data:
            print("Не удалось получить данные о погоде")
            return None
        return json.dumps(weather_data, indent=4, ensure_ascii=False)