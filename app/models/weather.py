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

    def to_dict(self) -> dict:
        return {
            'temp': self.temp,
            'fells_like': self.fells_like,
            'probability': self.probability,
            'pressure': self.pressure,
            'wind': self.wind,
            'humidity': self.humidity
        }
