import requests
import pandas as pd
import os
from matplotlib import pyplot as plt
from datetime import datetime, timedelta


#--------------------------------------------------

today = datetime.now()
month_ago = today - timedelta(days=30)

start_date = month_ago.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

latitude = 32.09979
longitude = 74.182501

#--------------------------------------------------

url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": latitude,
	"longitude": longitude,
	"daily": ["temperature_2m_max", "temperature_2m_min"],
	"timezone": "auto",
	"start_date": start_date,
	"end_date": end_date,
}

response = requests.get(url, params=params)
data = response.json()

#--------------------------------------------------

daily_data = data["daily"]
df = pd.DataFrame({
    "Date" : daily_data["time"],
    "Max_Temp" : daily_data["temperature_2m_max"],
    "Min_Temp" : daily_data["temperature_2m_min"]
})

df["Date"] = pd.to_datetime(df["Date"])

#--------------------------------------------------

if not os.path.exists("data"):
    os.makedirs("data", exist_ok=True)

df.to_csv("data/daily-data.csv", index=False)

#--------------------------------------------------

plt.figure(figsize=(10, 6))
plt.plot(df["Date"], df["Max_Temp"], marker = "o", color = 'red', label = "Max Temperature")
plt.plot(df["Date"], df["Min_Temp"], marker = "o", color = 'blue', label = "Min Temperature")

plt.xticks(rotation = 10)
plt.xlabel("Date")
plt.ylabel("Temperature")
plt.title("Gujranwala Weather History")
plt.legend()
plt.tight_layout()

#--------------------------------------------------

plt.savefig("weather-chart.png")
plt.show()