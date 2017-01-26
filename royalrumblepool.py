from random  import randint
import sqlite3
import sys


DATABASE = None
CURSOR = None


# Create/Connect to SQLite database
def connect():
	global DATABASE, CURSOR
	try:
		DATABASE = sqlite3.connect('RRP-DB.db')
		CURSOR = DATABASE.cursor()
		CURSOR.execute('CREATE TABLE IF NOT EXISTS Entrant ('
						'Name TEXT PRIMARY KEY COLLATE NOCASE,'
						'Number INTEGER NOT NULL,'
						'Note TEXT,'
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
def insert_entrant(entrant_name, entrant_note=None):
	entrant = entrant_info(entrant_name)
	if not entrant:
		entry_number = randint(1, 30)
		query = 'INSERT INTO Entrant (Name, Number, Note, DateEntered) values (?, ?, ?, DATETIME("now","localtime"))'
		CURSOR.execute(query, (entrant_name, randint(1, 30), entrant_note))
		DATABASE.commit()
		return '{} has Entered the Royal Rumble as #{}!'.format(entrant_name, entry_number)

	return '{} has Already Been Assigned Entry Number #{} on {}!'.format(entrant[0], entrant[1], entrant[3])


# Print out database content
def dump():
	for row in CURSOR.execute('SELECT * FROM Entrant').fetchall():
		print(row)


if __name__ == '__main__':
	args = sys.argv[1:]
	if len(args) == 2:
		if connect():
			output = insert_entrant(args[0], args[1])
		else:
			output = 'Unable to Connect to Database.'
	else:
		output = 'Invalid Arguments - Required [entrant_name] [entrant_note]'
	print(output)
