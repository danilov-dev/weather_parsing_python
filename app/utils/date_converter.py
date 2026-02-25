import datetime
from typing import Optional


class DateConverter:

    @staticmethod
    def get_date(date_text: str) -> Optional[str]:
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
            return None

        date = full_date[1].split(' ')
        if len(date[0]) < 2:
            day = '0'+date[0]
        else:
            day = date[0]
        month = date[1].strip().lower()[:-1]

        return '.'.join([day, months[month], str(datetime.date.today().year)])