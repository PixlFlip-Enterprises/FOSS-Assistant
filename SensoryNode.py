"""
SensoryNode.py Version 0.1.
Author: PixlFlip
Date: Jan 26, 2022

First Version! Featuring absolutely nothing
noteworthy or interesting. In fact why am
I taking the time to write this???
"""
# import Adafruit_DHT
# sensor = Adafruit_DHT.DHT22
# pin = 4
# while True:
#      humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
#      print("Temperature")
#      print(temperature)
#      print("Humidity")
#      print(humidity)


"""Everything in this file is based on timing or preforming an action after or on a specific date/time"""
import pandas as pd
import numpy
from pytrends.request import TrendReq
pytrend = TrendReq()
# Get Google Hot Trends data
df = pytrend.trending_searches(pn='united_states')
# df = pytrend.today_searches(pn='US')
df.head()
