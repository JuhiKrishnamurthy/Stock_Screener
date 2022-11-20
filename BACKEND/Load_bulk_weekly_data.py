import sys
import json
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
	ll_str = ll_str + str(ll[10]) 

	querystr="insert into WEEKLYPRICE values(" + ll_str + ");"
	print(querystr)
	db.exec_write_query(querystr)
	return

def main():
	f1 = open(sys.argv[1])
	db = MFDataDb()
	db.connect()

	for line in f1:
		linelist = [None]*11
		line = line.rstrip('\r\n')
		ts = json.loads(line)
		if not("Meta Data" in ts):
			continue
		MD = ts["Meta Data"]
		ticker = MD["2. Symbol"]
		linelist[0]=ticker
		for k in ts["Weekly Adjusted Time Series"]:
			tradedatestr = k
			linelist[3] = tradedatestr
			info = ts["Weekly Adjusted Time Series"][k]
			linelist[4] = info["1. open"]
			linelist[5] = info["2. high"]
			linelist[6] = info["3. low"]
			linelist[7] = info["4. close"]
			linelist[8] = info["6. volume"]
			linelist[9] = info["5. adjusted close"]
			linelist[10] = info["7. dividend amount"]

			insert_line(db,linelist)

	return 0

if __name__ == "__main__":
	main()














