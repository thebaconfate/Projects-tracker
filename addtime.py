from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import os


def calctime(date: str, time: str, enddate: str = "", endtime: str = ""):
    prstime = date + " " + time
    starttime = datetime.strptime(prstime, "%d-%m-%Y %H:%M")
    endtime = (
        datetime.now()
        if enddate == "" and endtime == ""
        else datetime.strptime(enddate + " " + endtime, "%d-%m-%Y %H:%M")
    )
    return endtime - starttime


def addtime(time):
    load_dotenv()
    url = os.getenv("URL")
    response = requests.post(
        url + "/login",
        json={
            "email": os.getenv("EMAIL"),
            "password": os.getenv("PASSWORD"),
        },
    )
    print(response.json())
    print(url)
    try:
        response = requests.put(
        url + "/project:1/stage:1/add",
        json={"days": time.days, "seconds": time.seconds},
        )
    except Exception:
        response.url()
    print(response.json())
    fee = requests.get(url + "/project:1/calc")
    print(fee.json())


time = calctime("01-01-2021", "00:00", "01-01-2021", "0:01")
addtime(time)
