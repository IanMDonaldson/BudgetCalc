import sqlite3
from unittest import TestCase

import utils
from Consts import DATABASE
from mock import patch


class MockDB(TestCase):

    @classmethod
    def setUpClass(cls):
        con = sqlite3.connect(DATABASE)
        cur = con.cursor(dictionary=True)

        # drop database if it already exists
        try:
            cur.execute("DROP DATABASE {}".format(MYSQL_DB))
            cur.close()
            print("DB dropped")
        except mysql.connector.Error as err:
            print("{}{}".format(MYSQL_DB, err))

        cur = con.cursor(dictionary=True)
        try:
            cur.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(MYSQL_DB))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        con.database = MYSQL_DB

        query = """CREATE TABLE `test_table` (
                  `id` varchar(30) NOT NULL PRIMARY KEY ,
                  `text` text NOT NULL,
                  `int` int NOT NULL
                )"""
        try:
            cur.execute(query)
            con.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("test_table already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        insert_data_query = """INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                            ('1', 'test_text', 1),
                            ('2', 'test_text_2',2)"""
        try:
            cur.execute(insert_data_query)
            con.commit()
        except mysql.connector.Error as err:
            print("Data insertion to test_table failed \n" + err)
        cur.close()
        con.close()

        testconfig = {
            'host': MYSQL_HOST,
            'user': MYSQL_USER,
            'password': MYSQL_PASSWORD,
            'database': MYSQL_DB
        }
        cls.mock_db_config = patch.dict(utils.config, testconfig)

    @classmethod
    def tearDownClass(cls):
        con = sqlite3.connect(DATABASE)
        cur = con.cursor(dictionary=True)

        # drop test database
        try:
            cur.execute("DROP DATABASE {}".format(MYSQL_DB))
            con.commit()
            cur.close()
        except mysql.connector.Error as err:
            print("Database {} does not exists. Dropping db failed".format(MYSQL_DB))
        con.close()
