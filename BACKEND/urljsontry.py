import urllib.request, json 
import matplotlib.pyplot as plt
import numpy as np
xpoints=[]
ypoints=[]
with urllib.request.urlopen("http://54.188.231.51:5000/Stock_Price_Time_Series_Weekly/?ticker=ABB.BSE&start_date=2020-10-01&end_date=2022-10-01") as url:
    data = json.load(url)
    #print(data)
    #print(data[0]['adjustedclose'])
    for i in data:
        xpoints.append(i['tradedate']) 
        ypoints.append(i['adjustedclose']) 
xpts=xpoints[::-1]
ypts=ypoints[::-1]
plt.plot(xpts, ypts)
plt.title("WEEKLY TIME SERIES")
plt.xlabel("Date")
plt.ylabel("Closing Price")
plt.tick_params(axis='x', which='major', labelsize=0.01)
plt.show()

