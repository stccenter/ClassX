#!/bin/bash
echo "Initializing label_db tables and data..."
mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" label_db < /data/label_db.sql
echo "label_db initialization completed."
