import mysql.connector
from mysql.connector import errorcode


Connect = {
    "host": "cis4375.csummbr3vhgu.us-east-2.rds.amazonaws.com",
    "user": "admin",
    "password": "cis4375spring2022",
    "db": "cis4375db",
    "raise_on_warnings": True
}

class DatabaseConnection:
    def __init__(self):
        TABLES = {}
        TABLES['roles'] = (
            "CREATE TABLE `roles` ("
            "  `role_id` int NOT NULL AUTO_INCREMENT,"
            "  `role_name` varchar(10) NOT NULL,"
            "  PRIMARY KEY (`role_id`)"
            ")"
        )
        # UNIQUE KEY `Unique_role_name` (`role_name`)
        TABLES['account_status'] = (
            "CREATE TABLE `account_status` ("
            "  `account_status_id` int NOT NULL AUTO_INCREMENT,"
            "  `acct_status` varchar(10) NOT NULL,"
            "  PRIMARY KEY (`account_status_id`), UNIQUE KEY `Unique_acct_status` (`acct_status`)"
            ")"
        ) 

        TABLES['account'] = (
            "CREATE TABLE `account` ("
            "  `account_id` int NOT NULL AUTO_INCREMENT,"
            "  `username` varchar(50) NOT NULL,"
            "  `password` varchar(255) NOT NULL,"
            "  `secret_question` varchar(255) NOT NULL,"
            "  `secret_answer` varchar(255) NOT NULL,"
            "  `role_id` int NOT NULL,"
            "  `account_status_id` int NOT NULL,"
            "  `active` bit NOT NULL,"
            "  PRIMARY KEY (`account_id`), UNIQUE KEY `Unique_username` (`username`),"
            "  CONSTRAINT `FK_account_role_id` FOREIGN KEY (`role_id`) "
            "     REFERENCES `roles` (`role_id`) ON UPDATE CASCADE,"
            "  CONSTRAINT `FK_account_account_status_id` FOREIGN KEY (`account_status_id`) "
            "     REFERENCES `account_status` (`account_status_id`) ON UPDATE CASCADE"
            ")"
        )

        TABLES['employee_status'] = (
            "CREATE TABLE `employee_status` ("
            "  `employee_status_id` int NOT NULL AUTO_INCREMENT,"
            "  `emp_status` varchar(10) NOT NULL,"
            "  PRIMARY KEY (`employee_status_id`), UNIQUE KEY `Unique_emp_status` (`emp_status`)"
            ")"
        ) 

        TABLES['employee'] = (
            "CREATE TABLE `employee` ("
            "  `employee_id` int NOT NULL AUTO_INCREMENT,"
            "  `first_name` varchar(50) NOT NULL,"
            "  `last_name` varchar(50) NOT NULL,"
            "  `birthday` date NOT NULL,"
            "  `phone` varchar(12) NOT NULL,"
            "  `email` varchar(50),"
            "  `address` varchar(100),"
            "  `employee_status_id` int NOT NULL,"
            "  `account_id` int NOT NULL,"
            "  `active` bit NOT NULL,"
            "  PRIMARY KEY (`employee_id`),"
            "  CONSTRAINT `FK_employee_employee_status_id` FOREIGN KEY (`employee_status_id`) "
            "     REFERENCES `employee_status` (`employee_status_id`) ON UPDATE CASCADE,"
            "  CONSTRAINT `FK_employee_account_id` FOREIGN KEY (`account_id`) "
            "     REFERENCES `account` (`account_id`) ON UPDATE CASCADE"  # considering UPDATE CASCADE
            ")"
        )

        TABLES['roles_data1'] = (
            "INSERT INTO `roles` (`role_name`) SELECT 'Admin' FROM DUAL WHERE NOT EXISTS (SELECT * FROM `roles` WHERE `role_name`='Admin' LIMIT 1);"
        )

        TABLES['roles_data2'] = (
            "INSERT INTO `roles` (`role_name`) SELECT 'User' FROM DUAL WHERE NOT EXISTS (SELECT * FROM `roles` WHERE `role_name`='User' LIMIT 1);"
        )

        TABLES['employee_status_data1'] = (
            "INSERT INTO `employee_status` (`emp_status`) SELECT 'New' FROM DUAL WHERE NOT EXISTS (SELECT * FROM `employee_status` WHERE `emp_status`='New' LIMIT 1);"
        )

        TABLES['employee_status_data2'] = (
            "INSERT INTO `employee_status` (`emp_status`) SELECT 'Current' FROM DUAL WHERE NOT EXISTS (SELECT * FROM `employee_status` WHERE `emp_status`='Current' LIMIT 1);"
        )

        TABLES['employee_status_data3'] = (
            "INSERT INTO `employee_status` (`emp_status`) SELECT 'Pass' FROM DUAL WHERE NOT EXISTS (SELECT * FROM `employee_status` WHERE `emp_status`='Pass' LIMIT 1);"
        )        
            
        cnx = mysql.connector.connect(**Connect)
        cursor = cnx.cursor()
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table and inserting data to {}: ".format(table_name), end='')
                cursor.execute(table_description)
                cnx.commit()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
