from flask_restful import Resource, reqparse
from datetime import datetime
import pymysql as MySQLdb
import json
from API_Server.core_utilities import core_functions

# load config
config = json.load(open('config.json',))

########################################################################################################################
#                                                   FINANCE RESOURCE
########################################################################################################################
# finance get args
finance_get_args = reqparse.RequestParser()
finance_get_args.add_argument("id", type=str, help="ID of specific tx to retrieve.", required=False)
finance_get_args.add_argument("device_id", type=str, help="Device created on.", required=True)

# finance put args
finance_put_args = reqparse.RequestParser()
finance_put_args.add_argument("date", type=str, help="Datetime of transaction.", required=True)
finance_put_args.add_argument("title", type=str, help="Title of transaction.", required=True)
finance_put_args.add_argument("memo", type=str, help="Description of transaction.", required=False)
finance_put_args.add_argument("deposit", type=bool, help="True means positive, false means negative.", required=True)
finance_put_args.add_argument("amount", type=float, help="Monetary amount transferred", required=True)

# finance del args
finance_del_args = reqparse.RequestParser()
finance_del_args.add_argument("id", type=str, help="id of tx to be deleted", required=True)


# create finance resource
class Finance(Resource):

    def get(self, profile_id):
        # verify fields
        args = finance_get_args.parse_args()

        if args['id'] is None:
            # return all entries
            try:
                # open the database
                db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
                cursor = db.cursor()
                # Execute the SQL command
                cursor.execute("select * from FINANCE where PROFILE_ID LIKE '" + profile_id + "%';")
                # get all records
                records = cursor.fetchall()
                records = list(reversed(list(records)))
                # log
                core_functions.debug_log(profile_id, "Finance Transactions View", 'server', "000500", "201", "View Finance")
                try:
                    dates = []
                    txs = {"status": "Completed.", 'total_transactions': len(records), 'by_date': dates}
                    # convert to dicts and store with usable data
                    for r in records:
                        dates.append(r[2])
                        txs[r[2]] = [r[3], r[4], r[6], r[7]]
                    return txs, 201
                except:
                    # log
                    core_functions.debug_log(profile_id, "Finance Transactions View", 'server', "000500", "404", "Error View Finance")
                    return {"status": "Failed."}
            except:
                # Rollback in case there is any error
                db.rollback()
            # disconnect from server
            db.close()
        else:
            # one tx get request
            try:
                # open the database
                db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
                cursor = db.cursor()
                # Execute the SQL command
                cursor.execute("select * from FINANCE where PROFILE_ID LIKE '" + profile_id + "' AND ID LIKE " + args['id'] + ";")
                # get all records
                records = cursor.fetchall()
                # first is entry
                try:
                    txs = records[0]
                    # log
                    core_functions.debug_log(user=profile_id, command_run="Finance View Single Tx", device_id="server", command_id="000510", return_code="201")
                    return {"status": "Completed.", "date": txs[2], "title": txs[3], "memo": txs[4], "amount": txs[6]}, 201
                except:
                    # log
                    core_functions.debug_log(user=profile_id, command_run="Finance View Single Tx", device_id='server', command_id="000510", return_code="404", debug_msg="Error while retrieving the tx")
                    return {"status": "Failed. Transaction does not exist"}
            except:
                # Rollback in case there is any error
                db.rollback()
            # disconnect from server
            db.close()
            # return since entry doesn't exist
            core_functions.debug_log(user=profile_id, command_run="Finance View Single Tx", device_id='server', command_id="000510", return_code="404", debug_msg="Error while retrieving the tx")
            return {"status": "Failed. Transaction does not exist"}


    def put(self, profile_id):
        # verify fields
        args = finance_put_args.parse_args()
        # holding variable
        account_balance = 0.00

        # get the previous transaction's account balance
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
            cursor = db.cursor()
            # execute sql
            cursor.execute("select * from FINANCE where PROFILE_ID LIKE '" + profile_id + "%';")
            # get records
            records = cursor.fetchall()
            # get last tx
            account_balance = float(list(records)[len(records)-1][7])
            # update account balance with new transaction's value
            if args['deposit']:
                account_balance = account_balance + args['amount']
            else:
                account_balance = account_balance - args['amount']
            # update db with tx
            sql = "INSERT INTO FINANCE (PROFILE_ID, DATE, TITLE, MEMO, DEPOSIT, AMOUNT, ACCOUNT_BALANCE) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            val = (profile_id, args['date'], args['title'], args['memo'], args['deposit'], args['amount'], account_balance)
            cursor.execute(sql, val)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            return {"status": "Failed. Is the data provided correct?"}
        # disconnect from server
        db.close()
        # note, you can put a comma and then follow it with a status code of your choice. Handy for some stuff
        return {"status": "Completed"}, 201


    def delete(self, profile_id):
        # verify fields
        args = finance_del_args.parse_args()

        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
            cursor = db.cursor()
            # Execute the SQL command
            sql = "DELETE FROM FINANCE WHERE PROFILE_ID = '" + profile_id + "' AND DATE = '" + args['date'] + "%'"
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            core_functions.debug_log(user=profile_id, command_run="Finance Delete Tx", device_id='server', command_id="000503", return_code="404", debug_msg="Failed to delete entry.")
            return {"status": "Failed. Most likely means the entry does not exist or bad input."}
        return {"status": "Completed"}


    # todo unfortunately this is probably something I should keep for finances, so I have to figure out a way to update the db with info
    def patch(self, profile_id):
        # verify fields
        args = finance_get_args.parse_args()
        # log
        core_functions.debug_log(user=profile_id, command_run="Journal Delete Entry", device_id=args['device_id'], command_id="000023", return_code="201", debug_msg="Entry was deleted.")
        # todo update entry at a date with info provided in json
        return {"status": "Code will go here, but this returned correctly?"}