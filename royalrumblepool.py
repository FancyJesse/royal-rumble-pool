from datetime import date
from random import choice
import json
import os
import sqlite3
import sys


# Location of database file
DB_DIR = '/home/Public/royal-rumble-pool/'

# List of year's winning entry number
# List of tuples (YEAR, WINNING_ENTRY_NUMBER)
WINNING_ENTRIES = [(2017, 23)]

# Boolean to check if entries are currently being accepted
ACCEPTING_ENTRIES = False

# Database and cursor shared by all function
# Assigned when calling connect()
DATABASE = None
CURSOR = None

# Current year - used to access latest table
CURRENT_YEAR = date.today().year

# Highest entry number available
MAX_ENTRY_NUMBER = 30


# Create/Connect to SQLite database and create table for current year
def connect():
	global DATABASE, CURSOR
	try:
		if not os.path.exists(DB_DIR):
			os.makedirs(DB_DIR)
		DATABASE = sqlite3.connect(DB_DIR + 'RRP.db')
		CURSOR = DATABASE.cursor()
		CURSOR.execute(
			'CREATE TABLE IF NOT EXISTS Entrant_{} ('
			'Name TEXT PRIMARY KEY COLLATE NOCASE,'
			'Number INTEGER NOT NULL,'
			'Comment TEXT,'
			'DateEntered INTEGER DEFAULT 0'
			')'.format(CURRENT_YEAR)
		)
		DATABASE.commit()
		return True
	except:
		return False


# Get all winners based on WINNING_ENTRIES
def winners():
	if WINNING_ENTRIES:
		winner_data = []
		for winning_entry in WINNING_ENTRIES:
			year_winners = []
			if winning_entry[1]:
				query = 'SELECT * FROM Entrant_{} Where Number=? ORDER BY Name'.format(winning_entry[0])				
				for row in CURSOR.execute(query, (winning_entry[1],)).fetchall():
					entrant = {}
					entrant['name'] = row[0]
					entrant['number'] = row[1]
					entrant['comment'] = row[2]
					entrant['date'] = row[3]
					year_winners.append(entrant)
			else:
				entrant = {}
				entrant['name'] = 'Coming Soon'
				entrant['number'] = 'Coming Soon'
				entrant['comment'] = 'Coming Soon'
				entrant['date'] = 'Coming Soon'
				year_winners.append(entrant)
			if not year_winners:
				entrant = {}
				entrant['name'] = 'Winner(s) Not Found'
				entrant['number'] = winning_entry[1]
				entrant['comment'] = 'Winner(s) Not Found'
				entrant['date'] = 'Winner(s) Not Found'
				year_winners.append(entrant)
			winner_data.append({'year':winning_entry[0], 'winners':year_winners})
		return True, winner_data
	return False, 'Winning entry data not found'


# Get a random entry number
# If all entry numbers are given - duplicates accepted
def random_entry_number():
	entry_numbers = list(range(1, MAX_ENTRY_NUMBER + 1))
	query = 'SELECT DISTINCT Number FROM Entrant_{}'.format(CURRENT_YEAR)
	CURSOR.execute(query)
	data = CURSOR.fetchall()
	data = [row[0] for row in data]
	if data and len(data) < MAX_ENTRY_NUMBER:
		entry_numbers = list(set(entry_numbers) - set(data))
	return choice(entry_numbers)


# Check if entrant exists in current table
def entrant_info(entrant_name):
	query = 'SELECT * FROM Entrant_{} WHERE Name=?'.format(CURRENT_YEAR)
	CURSOR.execute(query, (entrant_name,))
	return CURSOR.fetchone()


# Insert entrant info into current table and assign entry number
def insert_entrant(entrant_name, entrant_comment=None):
	if not ACCEPTING_ENTRIES:
		return False, 'Sorry, entries for the {} Royal Rumble are closed. See you next year!'.format(CURRENT_YEAR)
	entrant_name = entrant_name.strip()
	if not (entrant_name and len(entrant_name) > 2):
		return False, 'Invalid Entry Name'
	if entrant_comment:
		entrant_comment = entrant_comment.strip()
	entrant = entrant_info(entrant_name)
	if not entrant:
		entry_number = random_entry_number()
		query = 'INSERT INTO Entrant_{} (Name, Number, Comment, DateEntered) values (?, ?, ?, DATETIME("now","localtime"))'.format(CURRENT_YEAR)
		CURSOR.execute(query, (entrant_name, entry_number, entrant_comment))
		DATABASE.commit()
		return True, '{} has entered the Royal Rumble as #{}!'.format(entrant_name, entry_number)
	return False, '{} has already been assigned Entry Number #{} on {}!'.format(entrant[0], entrant[1], entrant[3])


# Remove entrant from current table
def remove_entrant(entrant_name):
	entrant_name = entrant_name.strip()
	if not entrant_name:
		return False, 'Invalid Entry Name'
	if entrant_info(entrant_name):
		query = 'DELETE FROM Entrant_{} WHERE Name=?'.format(CURRENT_YEAR)
		CURSOR.execute(query, (entrant_name,))
		DATABASE.commit()
		return True, '{} has been removed from the Royal Rumble!'.format(entrant_name)
	return False, '{} is not in the Royal Rumble!'.format(entrant_name)


# Re-roll entrant's entry number in current table
def reroll_entrant(entrant_name):
	entrant_name = entrant_name.strip()
	if not entrant_name:
		return False, 'Invalid Entry Name'
	entrant = entrant_info(entrant_name)
	if entrant_info(entrant_name):
		entry_number = random_entry_number()
		query = 'UPDATE Entrant_{} SET Number=? WHERE Name=?'.format(CURRENT_YEAR)
		CURSOR.execute(query, (entry_number, entrant_name))
		DATABASE.commit()
		return True, "{}'s Entry Number has been altered: '{}' -> '{}'".format(entrant_name, entrant[1], entry_number)
	return False, '{} is not in the Royal Rumble!'.format(entrant_name)


# Change entrant's comment in current table
def update_comment(entrant_name, new_comment):
	entrant_name = entrant_name.strip()
	if not entrant_name:
		return False, 'Invalid Entry Name'
	if new_comment:
		new_comment = new_comment.strip()
	entrant = entrant_info(entrant_name)
	if entrant_info(entrant_name):
		query = 'UPDATE Entrant_{} SET Comment=? WHERE Name=?'.format(CURRENT_YEAR)
		CURSOR.execute(query, (new_comment, entrant_name))
		DATABASE.commit()
		return True, "{}'s Comment has been altered: '{}' -> '{}'".format(entrant_name, entrant[2], new_comment)
	return False, '{} is not in the Royal Rumble!'.format(entrant_name)


# Return all stored content from selected year
def dump(year=CURRENT_YEAR):
	entrant_data = []
	for row in CURSOR.execute('SELECT * FROM Entrant_{} ORDER BY Number, Name'.format(year)).fetchall():
		entrant = {}
		entrant['name'] = row[0]
		entrant['number'] = row[1]
		entrant['comment'] = row[2]
		entrant['date'] = row[3]
		entrant_data.append(entrant)
	return True, entrant_data


# Console command - uses current year and table
if __name__ == '__main__':
	args = sys.argv[1:]
	result = False, 'Invalid Arguments - Required [OPTION] [ARG]*'
	if args:
		if connect():
			if len(args) == 1:
				if args[0] == '-d':
					result = dump()
				elif args[0] == '-winners':
					result = winners()
			elif len(args) == 2:
				if args[0] == '-remove':
					result = remove_entrant(args[1])
				elif args[0] == '-reroll':
					result = reroll_entrant(args[1])
			elif len(args) == 3:
				if args[0] == '-add':
					result = insert_entrant(args[1], args[2])
				elif args[0] == '-comment':
					result = update_comment(args[1], args[2])
		else:
			result = False, 'Database Connection Failed.'
	print(json.dumps({'success':result[0], 'data':result[1]}))
