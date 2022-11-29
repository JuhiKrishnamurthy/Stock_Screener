import sys
from functionalities2 import*
ch=0
while(ch!=11):

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
	#print("11.Get similar stocks")
	print("11.exit")
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
	elif ch==9:
	  	alert()
	elif ch==10:
	 	forecast()
	# elif ch==11:
	# 	#similar stock