import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3 as sq
import schedule 
import time



def parc():
	all_teams = []
	team1 = []
	team2 = []
	all_res = []
	res_team1 = []
	res_team2 = []
	all_beasts = []
	beast_team1 = []
	beast_team2 = []
	stat_all = []
	stat1 = []
	stat11 = []
	stat2 = []
	stat22 = []
	all_rec = []
	rec_n = []
	rec1 = []
	rec2 = []


	url = "https://www.espn.com/nba/scoreboard/_/date/20230215"


	r = requests.get(url).text

	soup = BeautifulSoup(r, 'html5lib')



	teams = soup.find_all('div', class_ = 'ScoreCell__Truncate clr-gray-01 ScoreCell__Truncate--scoreboard flex items-center h7 h5')
	for tms in teams:
		all_teams += [tms.text]
		#print(all_teams)
	for i in range(0, len(all_teams), 2):
		team1 += [all_teams[i]]
		#print(team1)
	for i in range(1, len(all_teams), 2):
		team2 += [all_teams[i]]
		#print(team2)


	rs = soup.find_all('div', class_ = 'ScoreCell__Score h4 clr-gray-01 fw-heavy tar ScoreCell_Score--scoreboard pl2')
	for R in rs:
		all_res += [R.text]
	for i in range(0, len(all_res), 2):
		res_team1 += [all_res[i]]
	for i in range(1, len(all_res), 2):
		res_team2 += [all_res[i]]




	tp = soup.find_all('span', class_ = 'Athlete__PlayerName')
	for t in tp:
		all_beasts += [t.text]
	#print(all_beasts)
	for i in range(0, len(all_beasts), 2):
		beast_team1 += [all_beasts[i]]
	for i in range(1, len(all_beasts), 2):
		beast_team2 += [all_beasts[i]]

	#print(list_beasts)


	tp_s = soup.find_all('div', class_ = 'Athlete__Stats mt2 clr-gray-04 ns9')
	for tp in tp_s:
		stat_all += [tp.text]
	for i in range(0, len(stat_all), 2):
		stat1 += [stat_all[i]] 
	for i in range(1, len(stat_all), 2):
		stat2 += [stat_all[i]] 
	for i in range(len(stat1)):
		el = str(stat1[i])
		if 'PTS' in el or 'REB' in el or 'AST' in el or 'STL' in el or 'BLK' in el:
			el = el.replace('PTS', ' PTS ').replace('REB', ' REB ').replace('STL', ' STL ').replace('BLK',' BLK ').replace('AST', ' AST ')
		stat11.append(el)
	for i in range(len(stat2)):
		el = str(stat2[i])
		if 'PTS' in el or 'REB' in el or 'AST' in el or 'STL' in el or 'BLK' in el:
			el = el.replace('PTS', ' PTS ').replace('REB', ' REB ').replace('STL', ' STL ').replace('BLK',' BLK ').replace('AST', ' AST ')
		stat22.append(el)

	

	rec = soup.find_all('span', class_ = 'ScoreboardScoreCell__Record')
	for r in rec:
		all_rec += [r.text]
	for i in range(0, len(all_rec), 2):
		rec_n += [all_rec[i]]
	for i in range(0, len(rec_n), 2):
		rec1 += [rec_n[i]]
	for i in range(1, len(rec_n), 2):
		rec2 += [rec_n[i]]

	list_all = list(zip(team1,res_team1, res_team2, team2, beast_team1, beast_team2, stat11, stat22, rec1, rec2))
	df = pd.DataFrame(list_all, columns = ['Team1','Score1','Score2', 'Team2', 'Top_Performance1','Top_Performance2', 'Top_Performance_Score1', 'Top_Performance_Score2', 'Record1', 'Record2'])
	#print(df)



	conn = sq.connect('Stat_data_base.db')
	df.to_sql("stats",conn, if_exists='replace', index=False)
	conn.close()

parc()




'''
schedule.every().day.at("9:01").do(parc)
while True:
   schedule.run_pending()
   time.sleep(1)'''
