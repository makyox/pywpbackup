# python-wordpress-backup
 Backup wordpress site and database. Zip entire folder and gzip sql database. Fully automatic.
 
# Core functions
- Zip entire folder with wordpress
- Gzip database
- Parsing wp-config.php - no need to enter database credentials
- Creates directory with current backup

 # Usage

usage: pyb.py [-h] [-n] d

d - Base directory
-h, --help  show this help message and exit
-n, --nodb  Ignore wp-config file

# Example

pyb.py wordpress --nodb

Result: backup only wordpress directory

pyb.py wordpress 

Result: fully backup wordpress and database