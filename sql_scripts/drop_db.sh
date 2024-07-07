#!/usr/bin/sh

# Used when running mysql locally
# Deletes database.
# Prints warning that it shouldnt use a password inside a command

password="root"

echo "DROP DATABASE hbnb;" | mysql -uroot --password=$password
