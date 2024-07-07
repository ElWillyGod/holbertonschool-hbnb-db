#!/usr/bin/sh

# Used when running mysql locally
# Populates database.
# Prints warning that it shouldnt use a password inside a command

password="root"

cat ./1_tables.sql | mysql -uroot --password=$password
cat ./2_connection.sql | mysql -uroot --password=$password
cat ./3_admins.sql | mysql -uroot --password=$password
cat ./4_amenities.sql | mysql -uroot --password=$password
cat ./5_countries.sql | mysql -uroot --password=$password
