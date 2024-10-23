import requests
from datetime import datetime, timezone
import time
import smtplib

MY_LAT = 33.772948  # Your latitude
MY_LONG = -117.859276  # Your longitude
MY_EMAIL = "timmyt345345@gmail.com"
MY_PASSWORD = "qbtnsxioriyqxijz"


def iss_within_range():
    print('checking...')
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    return abs(MY_LONG - iss_longitude) <= 5 and abs(MY_LAT - iss_latitude) <= 5


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now(timezone.utc)
    return sunset < time_now.hour < sunrise


def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs='notxap55@yahoo.com',
            msg=f"Subject:ISS IS OVERHEAD!\n\nLook up!"
        )


while True:
    if iss_within_range() and is_dark():
        send_email()
        time.sleep(21600)
    time.sleep(60)
