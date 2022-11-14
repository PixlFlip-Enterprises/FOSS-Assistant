from flask_restful import Resource, reqparse
from datetime import datetime
import pymysql as MySQLdb
import json
from API_Server.core_utilities import core_functions

# load config
config = json.load(open('config.json',))

########################################################################################################################
#                                                   JOURNAL RESOURCE
########################################################################################################################
# journal get args
journal_get_args = reqparse.RequestParser()
journal_get_args.add_argument("date", type=str, help="Date of journal entry", required=False)
journal_get_args.add_argument("device_id", type=str, help="Device created on", required=True)

# journal put args
journal_put_args = reqparse.RequestParser()
journal_put_args.add_argument("date", type=str, help="Date of journal entry", required=False)
journal_put_args.add_argument("entry", type=str, help="Journal entry", required=True)
journal_put_args.add_argument("creation_device", type=str, help="Device created on", required=True)
journal_put_args.add_argument("starred", type=str, help="Favorited or not", required=True)
journal_put_args.add_argument("time_zone", type=str, help="Timezone created in", required=True)

# journal del args
journal_del_args = reqparse.RequestParser()
journal_del_args.add_argument("date", type=str, help="Date of journal entry to be deleted", required=True)


# create journal resource
class Journal(Resource):

    def get(self, profile_id):
        # verify fields
        args = journal_get_args.parse_args()

        if args['date'] is None:
            # return all entries
            try:
                # open the database
                db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
                cursor = db.cursor()
                # Execute the SQL command
                cursor.execute("select * from JOURNAL where PROFILE_ID LIKE '" + profile_id + "%';")
                # get all records
                records = cursor.fetchall()
                records = list(reversed(list(records)))
                # log
                core_functions.debug_log(profile_id, "Journal View Entries", args['device_id'], "000024", "201", "View Journal")
                try:
                    dates = []
                    entries = {"status": "Completed.", 'total_entries': len(records), 'by_date': dates}
                    # convert to dicts and store with usable data
                    for r in records:
                        dates.append(r[2])
                        entries[r[2]] = [r[3], r[5], r[6], r[7]]
                    return entries, 201
                except:
                    # log
                    core_functions.debug_log(profile_id, "Journal View Entries", args['device_id'], "000025", "404", "Error while retrieving the entry")
                    return {"status": "Failed."}
            except:
                # Rollback in case there is any error
                db.rollback()
            # disconnect from server
            db.close()
        else:
            # one entry get request
            try:
                # open the database
                db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
                cursor = db.cursor()
                # Execute the SQL command
                cursor.execute("select * from JOURNAL where PROFILE_ID LIKE '" + profile_id + "' AND DATE LIKE '" + args['date'] + "%';")
                # get all records
                records = cursor.fetchall()
                # first is entry
                try:
                    entry = records[0]
                    # log
                    core_functions.debug_log(user=profile_id, command_run="Journal View Entry", device_id=args['device_id'], command_id="000020", return_code="201")
                    return {"status": "Completed.", "date": entry[2], "entry": entry[3], "starred": entry[5], "creation_device": entry[6], "timezone": entry[7]}, 201
                except:
                    # log
                    core_functions.debug_log(user=profile_id, command_run="Journal View Entry", device_id=args['device_id'], command_id="000020", return_code="404", debug_msg="Error while retrieving the entry")
                    return {"status": "Failed. Entry does not exist"}
            except:
                # Rollback in case there is any error
                db.rollback()
            # disconnect from server
            db.close()
            # return since entry doesn't exist
            core_functions.debug_log(user=profile_id, command_run="Journal View Entry", device_id=args['device_id'], command_id="000020", return_code="404", debug_msg="Entry was not found in the database")
            return {"status": "Failed. Entry does not exist"}


    def put(self, profile_id):
        # verify fields
        args = journal_put_args.parse_args()
        # log
        # todo add a thing in here to allow for arbitrary dates to be added instead of just the second the put is received
        x = datetime.now().__str__().replace(" ", "")
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
            cursor = db.cursor()
            # Execute the SQL command
            sql = "INSERT INTO JOURNAL (PROFILE_ID, DATE, ENTRY, UUID, STARRED, CREATIONDEVICE, TIMEZONE) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            val = (profile_id, x, args['entry'], "UPDATED SO THIS IS AN UNUSED FIELD FOR NOW", args['starred'], args['creation_device'], args['time_zone'])
            print(val)
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
        args = journal_del_args.parse_args()

        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
            cursor = db.cursor()
            # Execute the SQL command
            sql = "DELETE FROM JOURNAL WHERE PROFILE_ID = '" + profile_id + "' AND DATE = '" + args['date'] + "%'"
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            core_functions.debug_log(user=profile_id,
                                     command_run="Journal Delete Entry", device_id=args['device_id'], command_id="000023",
                                     return_code="404", debug_msg="Failed to delete entry.")
            return {"status": "Failed. Most likely means the entry does not exist or bad input."}
        return {"status": "Completed"}


    def patch(self, profile_id):
        # verify fields
        args = journal_get_args.parse_args()
        # log
        core_functions.debug_log(user=profile_id, command_run="Journal Delete Entry", device_id=args['device_id'], command_id="000023", return_code="201", debug_msg="Entry was deleted.")
        # todo update entry at a date with info provided in json
        return {"status": "Code will go here, but this returned correctly?"}