from app.services.parser import Parser

if __name__ == "__main__":
    base_url = "https://world-weather.ru/pogoda/russia/saint_petersburg/"
    parser = Parser(base_url)
    json_weather_data = parser.parse()
    if json_weather_data is not None:
        try:
            with open('paring_result.json', 'w', encoding='utf-8') as outfile:
                outfile.write(json_weather_data)
        except  Exception as e:
            print(f"Error occurred {e}")
    else:
        print("Не удалось получить данные о погоде")


    print(json_weather_data)
