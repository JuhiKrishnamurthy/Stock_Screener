import sys
import matplotlib.pyplot as plt
# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from datetime import date
from datetime import timedelta
import numpy as np
from mf_db import *


# creating a Flask app
app = Flask(__name__)

# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/home', methods = ['GET', 'POST'])
def home():
	if(request.method == 'GET'):

		data = "hello world"
		return jsonify({'data': data})


# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):
	return jsonify({'data': num**2})






@app.route('/echorequest/', methods = ['GET'])
def echorequest():
	return jsonify(request.args)








@app.route('/Stock_Price_Time_Series_Weekly/', methods = ['GET'])
def Stock_Price_Time_Series_Weekly():
	pricedict = {}
	#connect to DB, issue the query, get the data, put it into price dict.
	#print(request.args)
	ticker_val = request.args["ticker"]
	start_date_val = request.args["start_date"]
	end_date_val = request.args["end_date"]

	dbconn = MFDataDb() 
	dbconn.connect()

	c = dbconn.exec_read_query(f"SELECT ticker,tradedate,adjustedclose,volume FROM WEEKLYPRICE where ticker = '{ticker_val}' and tradedate between '{start_date_val}' and '{end_date_val}' ;")
	# while True:
	#     row = c.fetchone()
	#     if (row == None):
	#         break
	#     print(row)
	#     print(row['tradedate'].isoformat())
	rows = c.fetchall()
	# for r in rows:
	    # print(r)

	return jsonify(rows)









@app.route('/Stock_Price_Time_Series_Daily/', methods = ['GET'])
def Stock_Price_Time_Series_Daily():
	pricedict = {}
	#connect to DB, issue the query, get the data, put it into price dict.
	#print(request.args)
	ticker_val = request.args["ticker"]
	start_date_val = request.args["start_date"]
	end_date_val = request.args["end_date"]

	dbconn = MFDataDb() 
	dbconn.connect()

	c = dbconn.exec_read_query(f"SELECT ticker,tradedate,volume FROM DAILYPRICE where ticker = '{ticker_val}' and tradedate between '{start_date_val}' and '{end_date_val}' ;")
	# while True:
	#     row = c.fetchone()
	#     if (row == None):
	#         break
	#     print(row)
	#     print(row['tradedate'].isoformat())
	rows = c.fetchall()
	# for r in rows:
	    # print(r)

	return jsonify(rows)









@app.route('/Risk_Value/', methods = ['GET'])
def Risk_Value():
	#connect to DB, issue the query, get the data, put it into price dict.
	#print(request.args)
	ticker_val = request.args["ticker"]
	dbconn = MFDataDb() 
	dbconn.connect()
	#start_date_val = request.args["start_date"]
	#end_date_val = request.args["end_date"]
	end_date_val = dbconn.exec_read_query(f"select DATE_FORMAT(max(tradedate), '%Y %m %e') from WEEKLYPRICE where ticker = '{ticker_val}' ;")
	#print(end_date_val)

	end_date_json=end_date_val.fetchall()
	cur_date_list = end_date_json[0]["DATE_FORMAT(max(tradedate), '%Y %m %e')"].split(" ")
	#print(cur_date_list)
	cur_date = date(int(cur_date_list[0]),int(cur_date_list[1]),int(cur_date_list[2]))
	start_date_val = (cur_date - timedelta(days=70))
	adj_close = dbconn.exec_read_query(f"SELECT adjustedclose FROM WEEKLYPRICE WHERE ticker = '{ticker_val}' and tradedate between '{start_date_val.isoformat()}' and '{cur_date.isoformat()}';")
	#min_adj_close = dbconn.exec_read_query(f"SELECT MIN(adjustedclose) FROM WEEKLYPRICE WHERE ticker = '{ticker_val}' and tradedate between '{start_date_val.isoformat()}' and '{cur_date.isoformat()} ;")
	#return jsonify(max_adj_close.fetchall())
	adj_close=adj_close.fetchall()
	adj_close_arr=[]
	for r in adj_close:
		adj_close_arr.append(float(r["adjustedclose"]))
	std_dev = np.std(adj_close_arr)
	ret_dict = {"ticker_val":ticker_val,"risk_val":std_dev}
	return jsonify(ret_dict)










@app.route('/Get_Alert/', methods = ['GET'])
def Get_Alert():
	ret_dict={}
	ticker_val = request.args["tickers"]
	ticker_vals=ticker_val.split(',')
	dbconn = MFDataDb() 
	dbconn.connect()
	for t in ticker_vals:
		last_date_val = dbconn.exec_read_query(f"select changepercent, ticker, tradedate from DAILYPRICE where tradedate = (select max(tradedate) from DAILYPRICE where ticker ='{t}') and ticker = '{t}'; ")
		ldv = last_date_val.fetchall()
		if abs(float(ldv[0]["changepercent"])) >= 1:
			ret_dict[t]=ldv
	return jsonify(ret_dict)

	# for r in rows:
	    # print(r)

	#return jsonify(rows)








@app.route('/Get_Forecast/', methods = ['GET'])
def Get_Forecast():
	ret_dict={}
	ticker_val = request.args["ticker"]
	dbconn = MFDataDb() 
	dbconn.connect()
	end_date_val = dbconn.exec_read_query(f"select DATE_FORMAT(max(tradedate), '%Y %m %e') from WEEKLYPRICE where ticker = '{ticker_val}' ;")
	end_date_json=end_date_val.fetchall()
	cur_date_list = end_date_json[0]["DATE_FORMAT(max(tradedate), '%Y %m %e')"].split(" ")
	cur_date = date(int(cur_date_list[0]),int(cur_date_list[1]),int(cur_date_list[2]))
	start_date_val = (cur_date - timedelta(days=365))
	adj_close = dbconn.exec_read_query(f"SELECT adjustedclose FROM WEEKLYPRICE WHERE ticker = '{ticker_val}' and tradedate between '{start_date_val.isoformat()}' and '{cur_date.isoformat()}';")
	adj_close=adj_close.fetchall()
	adj_close_arr=[]
	for r in adj_close:
		adj_close_arr.append(float(r["adjustedclose"]))
	x = np.arange(0,len(adj_close_arr),1)
	y = np.array(adj_close_arr)
	preds = np.polyfit(x,y,2)
	forecast_date = cur_date
	fd_pred_arr=[]
	for w in range(12):
		wn=w+len(adj_close_arr)
		forecasted_val=preds[0]*wn*wn + preds[1]*wn + preds[2]
		fd=forecast_date+timedelta(days=7)
		forecast_date=forecast_date+timedelta(days=7)
		ret_dict = {'ticker':ticker_val,'forecast_date':fd.isoformat(),'forecasted_value':forecasted_val}
		fd_pred_arr.append(ret_dict)
	return(jsonify(fd_pred_arr))



def SignUp():
		name = input("Enter Name: ")
		email = input("Enter email: ")
		passw =input("Enter Password: ")
		dbconn = MFDataDb() 
		dbconn.connect()
		dbconn.exec_write_query(f"Insert into USER values('{name}' , '{email}' , '{passw}' ,NULL,NULL,NULL,NULL,NULL) ;")
		print("User signed up successfully")
		return email

def login():
		email = input("Enter email: ")
		passw =input("Enter Password: ")
		dbconn = MFDataDb() 
		dbconn.connect()
		ex=dbconn.exec_read_query(f"SELECT EXISTS(SELECT * FROM USER WHERE email='{email}' and pass='{passw}');")
		if ex:
			print("logged in successfully")
		else:
			print("Either user does not exist or invalid password.")
		return email

def add_to_portfolio():
	email = input("Enter email: ")
	no_of_stock = int(input("Enter number of stocks: "))
	for i in range(no_of_stock):
		stock_name = input("Enter stock name: ")
		dbconn = MFDataDb() 
		dbconn.connect()
		dbconn.exec_write_query(f"Insert into PORTFOLIO values('{email}','{stock_name}');")

def view_portfolio():
	email = input("Enter email: ")
	dbconn = MFDataDb() 
	dbconn.connect()
	stock_list=dbconn.exec_read_query(f"select stock_name from PORTFOLIO where email = '{email}'; ")
	stock_list=stock_list.fetchall()
	print("PORTFOLIO:" )
	for s in stock_list:
		print(s)


def weekly_time_series():
	tic_name=input("Enter ticker name: ")
	stdt=input("Enter start date: ")
	enddt = input("Enter end date: ")
	qrystr = str(f"http://54.188.231.51:5000/Stock_Price_Time_Series_Weekly/?ticker={tic_name}&start_date={stdt}&end_date={enddt}")
	print("kindly paste the following url in browser to get weekly time series: ")
	print(qrystr)

def daily_time_series():
	tic_name=input("Enter ticker name: ")
	stdt=input("Enter start date: ")
	enddt = input("Enter end date: ")
	qrystr = str(f"http://54.188.231.51:5000/Stock_Price_Time_Series_Daily/?ticker={tic_name}&start_date={stdt}&end_date={enddt}")
	print("kindly paste the following url in browser to get daily time series: ")
	print(qrystr)



def risk_val():
	tick_name=input("Enter the ticker name: ")
	qrystr = str(f"http://54.188.231.51:5000/Risk_Value/?ticker={tick_name}")
	print("kindly paste the following url in browser to get risk value: ")
	print(qrystr)

def plot_graph_weekly():
	tick_name=input("Enter ticker name: ")
	dbconn = MFDataDb() 
	dbconn.connect()
	end_date_val = dbconn.exec_read_query(f"select DATE_FORMAT(max(tradedate), '%Y %m %e') from WEEKLYPRICE where ticker = '{tick_name}' ;")
	end_date_json=end_date_val.fetchall()
	cur_date_list = end_date_json[0]["DATE_FORMAT(max(tradedate), '%Y %m %e')"].split(" ")
	cur_date = date(int(cur_date_list[0]),int(cur_date_list[1]),int(cur_date_list[2]))
	start_date_val = (cur_date - timedelta(days=365))
	x = dbconn.exec_read_query(f"SELECT tradedate FROM WEEKLYPRICE where ticker = '{tick_name}' and tradedate between '{start_date_val}' and '{end_date_val}' ;")
	x =x.fetchall()
	y = dbconn.exec_read_query(f"SELECT adjustedclose FROM WEEKLYPRICE where ticker = '{tick_name}' and tradedate between '{start_date_val}' and '{end_date_val}' ;")
	y =y.fetchall()
	for v in x:
		print(v)
	plt.plot(x, y)
	plt.savefig('plot.png')






print("Choose your functionality:")
print("1.Sign up")
print("2.log in")
print("3.Add stock to portfolio")
print("4.View portfolio")
print("5.Get weekly time series")
print("6.Get daily time series")
print("7.Get time series plot")
print("8.Get risk value")
print("9.Get alerts")
print("10.Get forecast")
print("11.Get similar stocks")
print("12.exit")
print("\n")



ch = int(input())
if ch==1:
	SignUp()
elif ch==2:
 	login()
elif ch==3:
 	add_to_portfolio()
elif ch==4:
 	view_portfolio()
elif ch==5:
	weekly_time_series()
elif ch==6:
 	daily_time_series()
elif ch==7:
 	plot_graph_weekly()
elif ch==8:
 	risk_val()
# elif ch==9:
# 	#alert
# elif ch==10:
# 	#forecast
# elif ch==11:
# 	#similar stock
# elif ch==12:
# 	#exit the program



# driver function
if __name__ == '__main__':

	app.run(debug = True, host = "0.0.0.0", port=5000)
	print("\n")
	





	
