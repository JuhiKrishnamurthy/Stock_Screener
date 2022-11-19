import sys
import json
from datetime import date
from datetime import timedelta
from mf_db import *

def insert_line(db,ll):
	ll_str = '"'+str(ll[0]) + '"' + "," 
	ll_str = ll_str + '"' + '"' +","
	ll_str = ll_str + '"' + '"' +","
	ll_str = ll_str + '"' +str(ll[3]) + '"' +","
	ll_str = ll_str + str(ll[4]) +","
	ll_str = ll_str + str(ll[5]) +","
	ll_str = ll_str + str(ll[6]) +","
	ll_str = ll_str + str(ll[7]) +","
	ll_str = ll_str + str(ll[8]) +","
	ll_str = ll_str + str(ll[9]) +","
	ll_str = ll_str + str(ll[10]) +","
	ll_str = ll_str + str(ll[11]) 

	querystr="insert into DAILYPRICE values(" + ll_str + ");"
	#print(querystr)
	db.exec_write_query(querystr)
	return

def main():
	f1 = open(sys.argv[1])
	db = MFDataDb()
	db.connect()

	for line in f1:
		linelist = [None]*12
		line = line.rstrip('\r\n')
		ts = json.loads(line)
		if not("Meta Data" in ts):
			continue
		MD = ts["Meta Data"]
		ticker = MD["2. Symbol"]
		linelist[0]=ticker
		for k in ts["Time Series (Daily)"]:
			tradedatestr = k
			linelist[3] = tradedatestr
			info = ts["Time Series (Daily)"][k]
			# print(k)
			# print(info)
			linelist[4] = info["1. open"]
			linelist[5] = info["2. high"]
			linelist[6] = info["3. low"]
			linelist[7] = info["4. close"]
			linelist[8] = info["5. volume"]
			#START DATE = 2009-04-06
			sd = date(2000,1,1)
			#format = '%Y/%m/%d'
			#cur_date = datetime.strptime(k, format)
			cur_date_list = k.split("-")
			cur_date = date(int(cur_date_list[0]),int(cur_date_list[1]),int(cur_date_list[2]))
			prev_date= (cur_date - timedelta(days=1))
			while ((prev_date>sd) and not(prev_date.isoformat() in ts["Time Series (Daily)"])):
			 	prev_date = prev_date - timedelta(days=1)
			pd=prev_date.isoformat()
			if prev_date>sd:
				linelist[9] =  float(ts["Time Series (Daily)"][pd]["4. close"])#prev close
				linelist[10] = float(linelist[7])-float(linelist[9]) #price change 
				if abs(float(linelist[9]))>1e-5:
					linelist[11] = (float(linelist[10])/float(linelist[9]))*100 #change percent
			insert_line(db,linelist)


	return 0

if __name__ == "__main__":
	main()














