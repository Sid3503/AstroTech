import requests
from bs4 import BeautifulSoup

def get_zodiac_sign(birthday):
    day, month = map(int, birthday.split('-'))

    period_ranges = [
        ((21, 3), (19, 4), "aries", 1),
        ((20, 4), (20, 5), "taurus", 2),
        ((21, 5), (21, 6), "gemini", 3),
        ((22, 6), (22, 7), "cancer", 4),
        ((23, 7), (22, 8), "leo", 5),
        ((23, 8), (22, 9), "virgo", 6),
        ((23, 9), (23, 10), "libra", 7),
        ((24, 10), (21, 11), "scorpio", 8),
        ((22, 11), (21, 12), "sagittarius", 9),
        ((22, 12), (19, 1), "capricorn", 10),
        ((20, 1), (18, 2), "aquarius", 11),
        ((19, 2), (20, 3), "pisces", 12)
    ]

    for start, end, period_name, numeric_value in period_ranges:
        start_day, start_month = start
        end_day, end_month = end

        if (start_month < month < end_month) or \
           (start_month == month and day >= start_day) or \
           (end_month == month and day <= end_day):
            return period_name, numeric_value

    return "unknown", -1

def get_horoscope(zodiac_sign_num: int, day: str = "today") -> str:
    url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{day}.aspx?sign={zodiac_sign_num}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        horoscope_div = soup.find("div", class_="main-horoscope")
        if horoscope_div and horoscope_div.p:
            return horoscope_div.p.text.strip()
        else:
            return "Horoscope not found. Please check your input."

    except requests.exceptions.RequestException as e:
        return f"Error fetching horoscope: {e}"
