Royal-Rumble-Pool
========================================================================
[![status](https://img.shields.io/badge/Project%20Status-work--in--progress-green.svg)](#)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=jesus_andrade45%40yahoo%2ecom&lc=US&item_name=GitHub%20Projects&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)

Assigns Royal Rumble entry numbers and displays data on a webpage

####Current webpage: [royalrumblepool.fancyjesse.com](http://royalrumblepool.fancyjesse.com)


Introduction
------------------------------------------------------------------------
The Royal Rumble is a WWE PPV event where participants enter at timed intervals based on their entry number. This project was created to allow users to be assigned an entry number and see if their corresponding entry wins the Royal Rumble. Users are able to register their name, along with a comment, and are then assigned an entry number at random.

The project's main interface is provided through a webpage, where users can enter their name and comment, and be registered into the Royal Rumble pool. User data is stored in an SQLite database via a Python script. Communication to this Python script is provided by the webpage's PHP.

A list of winners will be retained in the webpage -- for bragging rights. Prior to winners being announced, the list of participants will be displayed on the webpage as well.


Prerequisites
------------------------------------------------------------------------
Python3

PHP

HTML webpage


Installation
------------------------------------------------------------------------
Before the installation, be sure to update & upgrade your current packages
```
$ sudo apt-get update && sudo apt-get upgrade
```

Clone the Royal-Rumble-Pool repository use the following:

git
```
$ git clone https://github.com/FancyJesse/royal-rumble-pool
```

Since the Python script creates a database file, a directory has to be set in which to place the newly created file.
By default, the directory path is '/home/Public/royal-rumble-pool/'. This can be changed within the script.

*Note 1: Paths are automatically created when running the Python script"

*Note 2: Be sure to apply the proper permissions to the created files and directory.*


Usage
------------------------------------------------------------------------
Insert user data into the database:
```
$ python3 ./royalrumblepool.py [entry_name] [entry_comment]
```

Dump all user data stored in the database:
```
$ python3 ./royalrumblepool.py -d
```

*Note: All returned data is of type JSON*


Release History
------------------------------------------------------------------------
* 0.2.0
	* Added command line arguement support
	* All functions return JSON (easier communication between PHP and AJAX)
* 0.1.0
	* Initial release


License
------------------------------------------------------------------------
See the file "LICENSE" for license information.


Authors
------------------------------------------------------------------------
FancyJesse
