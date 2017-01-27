from datetime import date
from random  import randint
import os
import sqlite3
import sys


DATABASE = None
CURSOR = None


# Create/Connect to SQLite database
def connect():
	global DATABASE, CURSOR
	try:
		db_dir = '/home/Public/royal-rumble-pool/'
		if not os.path.exists(db_dir):
			os.makedirs(db_dir)
		DATABASE = sqlite3.connect(db_dir + 'RRP-{}.db'.format(date.today().year))
		CURSOR = DATABASE.cursor()
		CURSOR.execute(
			'CREATE TABLE IF NOT EXISTS Entrant ('
			'Name TEXT PRIMARY KEY COLLATE NOCASE,'
			'Number INTEGER NOT NULL,'
			'Comment TEXT,'
			'DateEntered INTEGER DEFAULT 0'
			')'
		)
		DATABASE.commit()
		return True
	except:
		return False


# Check if entrant is unassigned
def entrant_info(entrant_name):
	query = 'SELECT * FROM Entrant WHERE Name=?'
	CURSOR.execute(query, (entrant_name,))
	return CURSOR.fetchone()


# Insert entrant info to database and assign entry number
def insert_entrant(entrant_name, entrant_comment=None):
	entrant_name = trim(entrant_name)
	if entrant_comment:
		entrant_comment = trim(entrant_comment)
	entrant = entrant_info(entrant_name)
	if not entrant:
		entry_number = randint(1, 30)
		query = 'INSERT INTO Entrant (Name, Number, Comment, DateEntered) values (?, ?, ?, DATETIME("now","localtime"))'
		CURSOR.execute(query, (entrant_name, entry_number, entrant_comment))
		DATABASE.commit()
		return '{} has entered the Royal Rumble as #{}!'.format(entrant_name, entry_number)

	return '{} has already been assigned Entry Number #{} on {}!'.format(entrant[0], entrant[1], entrant[3])


# Get all database content
def dump():
	entrant_data = []
	for row in CURSOR.execute('SELECT * FROM Entrant').fetchall():
		entrant = {}
		entrant['name'] = row[0]
		entrant['number'] = row[1]
		entrant['comment'] = row[2]
		entrant['date'] = row[3]
		entrant_data.append(entrant)
	return entrant_data


# Ran through console
if __name__ == '__main__':
	args = sys.argv[1:]
	output = 'Invalid Arguments - Required [entrant_name] [entrant_comment]'
	if args:
		if connect():
			if len(args) == 1 and args[0] == '-d':
				output = dump()
			elif len(args) == 2:
				output = insert_entrant(args[0], args[1])
		else:
			output = 'Database Connection Failed.'
	print(output)
