Royal-Rumble-Pool
========================================================================
[![status](https://img.shields.io/badge/Project%20Status-work--in--progress-green.svg)](#)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=jesus_andrade45%40yahoo%2ecom&lc=US&item_name=GitHub%20Projects&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)

Assigns Royal Rumble entry numbers and displays data on a webpage


Introduction
------------------------------------------------------------------------
The Royal Rumble is a WWE PPV event where participants enter at timed intervals based on their entry number. This project was created to allow users to be assigned an entry number and see if their corresponding entry wins the Royal Rumble. Users are able to register their name, along with a comment, and assigned an entry number at random.

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

To download the LED-Vote project use the following:

git
```
$ git clone https://github.com/FancyJesse/royal-rumble-pool
```


Usage
------------------------------------------------------------------------
To insert user data into the database use the following command:
```
$ cd
$ ./royalrumblepool.py [entry_name] [entry_comment]
```

*Note: You might have to explicitly call python3 to run it*
```
$ python3 ./royalrumblepool.py [entry_name] [entry_comment]
```

*Note: A database file is automatically created when first running the script*


Release History
------------------------------------------------------------------------
* 0.1.0
	* Initial release


License
------------------------------------------------------------------------
See the file "LICENSE" for license information.


Authors
------------------------------------------------------------------------
FancyJesse
