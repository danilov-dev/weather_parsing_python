from app.services.parser import Parser

if __name__ == "__main__":
    base_url = "https://world-weather.ru/pogoda/russia/saint_petersburg/"
    parser = Parser(base_url)
    json_weather_data = parser.parse()
    print(json_weather_data)
