# imports
from datetime import datetime
import pymysql as MySQLdb
import json

# load config
config = json.load(open('config.json', ))


# you don't need a comment to explain what this does
def debug_log(user, command_run, device_id, command_id, return_code, debug_msg=""):
    # todo remove this once build is release or stable
    print("= User " + user + " has issued the " + command_id + " command")

    try:
        # open the database
        db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
        cursor = db.cursor()
        # Execute the SQL command
        sql = "INSERT INTO LOGS (USER, DATE, COMMAND_RUN, DEVICE_ID, COMMAND_ID, RETURN_CODE, DEBUG_MSG) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        val = (user, datetime.now().__str__().replace(" ", ""), command_run, device_id, command_id, return_code, debug_msg)
        cursor.execute(sql, val)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
        print("Failed to log to database")

# de facto replacement for the same function in the old User.py file
def is_profile_api_key(key):
    try:
        # open the database
        db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
        cursor = db.cursor()
        # see if key exists
        cursor.execute("select * from API_KEYS where API_KEY like '%" + key + "%';")
        # get all records
        records = cursor.fetchall()
        # check
        if records[0][0] == key:
            return records[0][1]
        else:
            return False
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()
    return False
