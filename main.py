import datetime
import json
import requests
from bs4 import BeautifulSoup



class Day:
    """
    Класс представления дня
    """
    def __init__(self, date: str):
        self.date = date
        self.weather: list[Weather] = []

    def to_dict(self):
        result = {}
        for weather in self.weather:
            result[weather.period] = weather.to_dict()
        return result


class Weather:
    """
    Класс представления погоды за один дневной период (ночь, утро, день или вечер)
    """
    def __init__(self, period: str, temp: str, fells_like: str, probability: str, pressure: str, wind: dict[str, str],
                 humidity: str):
        self.period = period
        self.temp = temp
        self.fells_like = fells_like
        self.probability = probability
        self.pressure = pressure
        self.wind = wind
        self.humidity = humidity

    def to_dict(self):
        return {
            'temp': self.temp,
            'fells_like': self.fells_like,
            'probability': self.probability,
            'pressure': self.pressure,
            'wind': self.wind,
            'humidity': self.humidity
        }


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
                print(e)

    def _get_date(self, date_text: str):
        if not date_text:
            return "null"

        months = {
            'январ': '01',
            'феврал': '02',
            'март': '03',
            'апрел': '04',
            'ма': '05',
            'июн': '06',
            'июл': '07',
            'август': '08',
            'сентябр': '09',
            'октябр': '10',
            'ноябр': '11',
            'декабр': '12',
        }
        full_date = date_text.split(', ')
        if len(full_date) != 2:
            return "null"

        date = full_date[1].split(' ')
        if len(date[0]) < 2:
            day = '0'+date[0]
        else:
            day = date[0]
        month = date[1].strip().lower()[:-1]

        return '.'.join([day, months[month], str(datetime.date.today().year)])

    def _get_weather(self, table):
        if len(table) < 1 or table is None:
            return {}

        periods = ['night', 'morning', 'day', 'evening']

        date = table.find("div", class_="dates").text

        day = Day(self._get_date(date))

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
        return day

    def _parse_weather_table(self):
        self._get_soup()
        tables = self._soup.find_all("div", class_="weather-short")
        if len(tables) < 1:
            return {}
        days = {}
        for table in tables:
            day = self._get_weather(table)
            days[day.date] = day.to_dict()

        return days

    def parse(self):
        self._get_soup()
        weather_data = self._parse_weather_table()

        if not weather_data:
            print("Не удалось получить данные о погоде")
            return None
        return json.dumps(weather_data, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    base_url = "https://world-weather.ru/pogoda/russia/saint_petersburg/"
    parser = Parser(base_url)
    json_weather_data = parser.parse()
    print(json_weather_data)
