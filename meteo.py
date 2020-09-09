import csv
import sqlite3

db = sqlite3.connect('twisto_tweets.db')

#db.execute('''DROP TABLE IF EXISTS tweets;''')
db.execute('''CREATE TABLE IF NOT EXISTS weather (
	id INTEGER PRIMARY KEY,
	date TIMESTAMP NOT NULL,
	tavg FLOAT,
	tmin FLOAT,
	tmax FLOAT,
	prcp FLOAT,
	snow INTEGER,
	wdir INTEGER,
	wspd FLOAT,
	wpgt FLOAT,
	pres FLOAT,
	tsun INTEGER
);''')

with open('07027.csv', 'r', newline='', encoding='utf8') as f:
	fields = ['date', 'tavg', 'tmin', 'tmax', 'prcp',
           'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun']
	reader = csv.reader(f, delimiter=',')

	for row in reader:
		query = '''insert into weather (date, tavg, tmin, tmax, prcp, snow, wdir, wspd, wpgt, pres, tsun)'''
		query += ''' values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
		db.execute(query, row)
	db.commit()
db.close()
