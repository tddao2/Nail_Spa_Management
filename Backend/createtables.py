import mysql.connector
from mysql.connector import errorcode
from Backend.connection import Connect

class CreateTables:
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
            "  `secret_question` varchar(100) NOT NULL,"
            "  `secret_answer` varchar(255) NOT NULL,"
            "  `role_id` int NOT NULL,"
            "  `account_status_id` int NOT NULL,"
            "  `active` BIT NOT NULL DEFAULT 1,"
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
            "  `phone` varchar(16) NOT NULL,"
            "  `email` varchar(100),"
            "  `address` varchar(100),"
            "  `employee_status_id` int NOT NULL,"
            "  `account_id` int NOT NULL,"
            "  `active` BIT NOT NULL DEFAULT 1,"
            "  PRIMARY KEY (`employee_id`),"
            "  CONSTRAINT `FK_employee_employee_status_id` FOREIGN KEY (`employee_status_id`) "
            "     REFERENCES `employee_status` (`employee_status_id`) ON UPDATE CASCADE,"
            "  CONSTRAINT `FK_employee_account_id` FOREIGN KEY (`account_id`) "
            "     REFERENCES `account` (`account_id`) ON UPDATE CASCADE ON DELETE CASCADE"  # considering UPDATE CASCADE
            ")"
        )

        TABLES['feedback'] = (
            "CREATE TABLE `feedback` ("
            "  `feedback_id` int NOT NULL AUTO_INCREMENT,"
            "  `employee_id` int NOT NULL,"
            "  `performance_score` int NOT NULL,"
            "  `description` varchar(500),"
            "  `dateFB` datetime DEFAULT CURRENT_TIMESTAMP,"
            "  `active` BIT NOT NULL DEFAULT 1,"
            "  PRIMARY KEY (`feedback_id`),"
            "  CONSTRAINT `FK_feedback_employee_id` FOREIGN KEY (`employee_id`) "
            "     REFERENCES `employee` (`employee_id`)"
            ")"
        )

        TABLES['service_type'] = (
            "CREATE TABLE `service_type` ("
            "  `service_type_code` char(10) NOT NULL,"
            "  `service_type_desc` varchar(100) NOT NULL,"
            "  PRIMARY KEY (`service_type_code`), UNIQUE KEY `Unique_service_type_desc` (`service_type_desc`)"
            ")"
        )

        TABLES['service'] = (
            "CREATE TABLE `service` ("
            "  `service_id` int NOT NULL AUTO_INCREMENT,"
            "  `service_name` varchar(50) NOT NULL,"
            "  `price` DECIMAL(5,2) NOT NULL,"
            "  `service_type_code` char(10) NOT NULL,"
            "  PRIMARY KEY (`service_id`), UNIQUE KEY `Unique_service_name` (`service_name`),"
            "  CONSTRAINT `FK_service_service_type_code` FOREIGN KEY (`service_type_code`) "
            "     REFERENCES `service_type` (`service_type_code`) ON UPDATE CASCADE"
            ")"
        )

        TABLES['customer'] = (
            "CREATE TABLE `customer` ("
            "  `customer_id` int NOT NULL AUTO_INCREMENT,"
            "  `first_name` varchar(50) NOT NULL,"
            "  `last_name` varchar(50) NOT NULL,"
            "  `phone` varchar(12),"
            "  `email` varchar(100),"
            "  `active` BIT NOT NULL DEFAULT 1,"
            "  PRIMARY KEY (`customer_id`), UNIQUE KEY `Unique_phone` (`phone`)"
            ")"
        )

        TABLES['invoice'] = (
            "CREATE TABLE `invoice` ("
            "  `invoice_id` int NOT NULL AUTO_INCREMENT,"
            "  `employee_id` int NOT NULL,"
            "  `customer_id` int NOT NULL,"
            "  `tip` DECIMAL(5,2) DEFAULT '0.00',"
            "  `discount` int DEFAULT '0',"
            "  `invoice_total` DECIMAL(5,2) NOT NULL,"
            "  `invoice_datetime` datetime DEFAULT CURRENT_TIMESTAMP,"
            "  `active` BIT NOT NULL DEFAULT 1,"
            "  PRIMARY KEY (`invoice_id`),"
            "  CONSTRAINT `FK_invoice_employee_id` FOREIGN KEY (`employee_id`) "
            "     REFERENCES `employee` (`employee_id`) ON UPDATE CASCADE,"
            "  CONSTRAINT `FK_invoice_customer_id` FOREIGN KEY (`customer_id`) "
            "     REFERENCES `customer` (`customer_id`) ON UPDATE CASCADE"
            ")"
        )

        TABLES['invoice_line_item'] = (
            "CREATE TABLE `invoice_line_item` ("
            "  `invoice_line_item_id` int NOT NULL AUTO_INCREMENT,"
            "  `invoice_id` int NOT NULL,"
            "  `service_id` int NOT NULL,"
            "  `active` BIT NOT NULL DEFAULT 1,"
            "  PRIMARY KEY (`invoice_line_item_id`),"
            "  CONSTRAINT `FK_invoice_line_item_invoice_id` FOREIGN KEY (`invoice_id`) "
            "     REFERENCES `invoice` (`invoice_id`) ON UPDATE CASCADE,"
            "  CONSTRAINT `FK_invoice_line_item_service_id` FOREIGN KEY (`service_id`) "
            "     REFERENCES `service` (`service_id`) ON UPDATE CASCADE"
            ")"
        )

        TABLES['appointment'] = (
            "CREATE TABLE `appointment` ("
            "  `appointment_id` int NOT NULL AUTO_INCREMENT,"
            "  `customer_id` int NOT NULL,"
            "  `date_appt` date NOT NULL,"
            "  `time_appt` varchar(10) NOT NULL,"
            "  `appt_desc` varchar(255),"
            "  `active` BIT NOT NULL DEFAULT 1,"
            "  PRIMARY KEY (`appointment_id`),"
            "  CONSTRAINT `FK_appointment_customer_id` FOREIGN KEY (`customer_id`) "
            "     REFERENCES `customer` (`customer_id`) ON UPDATE CASCADE"
            ")"
        )

        TABLES['roles_data1'] = (
            "INSERT INTO `roles` (`role_name`) SELECT 'Admin' FROM DUAL WHERE NOT EXISTS (SELECT * FROM `roles` WHERE `role_name`='Admin' LIMIT 1);"
        )

        TABLES['roles_data2'] = (
            "INSERT INTO `roles` (`role_name`) SELECT 'User' FROM DUAL WHERE NOT EXISTS (SELECT * FROM `roles` WHERE `role_name`='User' LIMIT 1);"
        )

        TABLES['account_status_data1'] = (
            "INSERT INTO `account_status` (`acct_status`) SELECT 'active' FROM DUAL WHERE NOT EXISTS (SELECT * FROM `account_status` WHERE `acct_status`='active' LIMIT 1);"
        )

        TABLES['account_status_data2'] = (
            "INSERT INTO `account_status` (`acct_status`) SELECT 'pending' FROM DUAL WHERE NOT EXISTS (SELECT * FROM `account_status` WHERE `acct_status`='pending' LIMIT 1);"
        )

        TABLES['account_status_data3'] = (
            "INSERT INTO `account_status` (`acct_status`) SELECT 'inactive' FROM DUAL WHERE NOT EXISTS (SELECT * FROM `account_status` WHERE `acct_status`='inactive' LIMIT 1);"
        )

        TABLES['employee_status_data1'] = (
            "INSERT INTO `employee_status` (`emp_status`) SELECT 'New' FROM DUAL WHERE NOT EXISTS (SELECT * FROM `employee_status` WHERE `emp_status`='New' LIMIT 1);"
        )

        TABLES['employee_status_data2'] = (
            "INSERT INTO `employee_status` (`emp_status`) SELECT 'Current' FROM DUAL WHERE NOT EXISTS (SELECT * FROM `employee_status` WHERE `emp_status`='Current' LIMIT 1);"
        )

        TABLES['Default_Admin'] = (
            "INSERT INTO account(username, password, secret_question, secret_answer, role_id, account_status_id) \
            values('admin','$2b$12$xhojbjLhp/HzHDm7YbJVKuFwMSrhWvkMCgEcApyzditKtwcrbLjxy','Your Pet Name','$2b$12$cqf0WNfBSlpP9UkLa5orwOb47RoVYl9rV/eG7HDQb6/aLEPDnlZOW',1,1);"
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
                elif mysql.connector.errors.IntegrityError:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")