from app.models.weather import Weather

class Day:
    """
    Класс представления дня
    """
    def __init__(self, date: str):
        self.date = date
        self.weather: list[Weather] = []

    def to_dict(self) -> dict:
        result = {}
        for weather in self.weather:
            result[weather.period] = weather.to_dict()
        return result