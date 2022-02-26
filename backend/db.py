import mysql.connector
from mysql.connector import errorcode

Connect = {
    "host": "cis4375.csummbr3vhgu.us-east-2.rds.amazonaws.com",
    "user": "admin",
    "password": "cis4375spring2022",
    "db": "cis4375db",
    'raise_on_warnings': True}

TABLES = {}
TABLES['roles'] = (
    "CREATE TABLE `roles` ("
    "  `role_id` int NOT NULL AUTO_INCREMENT,"
    "  `role_name` date NOT NULL,"
    "  PRIMARY KEY (`role_id`)"
    ")")
    # ") ENGINE=InnoDB")

TABLES['account'] = (
    "CREATE TABLE `account` ("
    "  `account_id` int NOT NULL AUTO_INCREMENT,"
    "  `username` varchar(50) NOT NULL,"
    "  `password` varchar(255) NOT NULL,"
    "  `role_id` int NOT NULL,"
    "  `active` bit NOT NULL,"
    "  PRIMARY KEY (`account_id`), UNIQUE KEY `username` (`username`),"
    "  CONSTRAINT `FK_account_role_id` FOREIGN KEY (`role_id`) "
    "     REFERENCES `roles` (`role_id`) ON UPDATE CASCADE"
    ")")
    # ") ENGINE=InnoDB")

cnx = mysql.connector.connect(**Connect)
cursor = cnx.cursor()

def create_database(cursor):
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

create_database(cursor)

# References
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
# https://www.mysqltutorial.org/mysql-create-database/
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
# https://www.mysqltutorial.org/mysql-create-table/