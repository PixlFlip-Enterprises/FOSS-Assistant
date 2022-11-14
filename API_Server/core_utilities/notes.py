from flask_restful import Resource, reqparse
from datetime import datetime
import pymysql as MySQLdb
import json
from API_Server.core_utilities import core_functions
# load config
config = json.load(open('config.json',))

########################################################################################################################
#                                                   NOTE RESOURCE
########################################################################################################################
# notes put args
notes_put_args = reqparse.RequestParser()
notes_put_args.add_argument("title", type=str, help="Note Title", required=True)
notes_put_args.add_argument("body", type=str, help="Note", required=True)
notes_put_args.add_argument("creation_device", type=str, help="Device created on", required=True)
notes_put_args.add_argument("starred", type=str, help="Favorited or not", required=True)
notes_put_args.add_argument("time_zone", type=str, help="Timezone created in", required=True)

# notes del args
notes_del_args = reqparse.RequestParser()
notes_del_args.add_argument("id", type=str, help="ID of the note to be deleted", required=True)

# notes patch args
notes_patch_args = reqparse.RequestParser()
notes_del_args.add_argument("id", type=str, help="ID of the note to be deleted", required=True)
notes_patch_args.add_argument("title", type=str, help="Note Title", required=False)
notes_patch_args.add_argument("body", type=str, help="Note", required=False)
notes_patch_args.add_argument("creation_device", type=str, help="Device created on", required=False)
notes_patch_args.add_argument("starred", type=str, help="Favorited or not", required=False)
notes_patch_args.add_argument("time_zone", type=str, help="Timezone created in", required=False)

class Notes(Resource):

    def get(self, profile_id):
        # no fields to verify, just grab literally all notes of a profile, json them, then fling them over to the client so it's their problem
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute("select * from NOTE where OWNING_USER LIKE '" + profile_id + "';")
            # get all records
            records = cursor.fetchall()
            # log
            core_functions.debug_log(user=profile_id, command_run="Notebook View Notes", device_id="Client", command_id="000050", return_code="201")
            return {"status": "Completed.", "notes": records}, 201
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        # return since entry doesn't exist
        core_functions.debug_log(user=profile_id, command_run="Notebook View Notes", device_id="Client", command_id="000050", return_code="404", debug_msg="Notes were not found in the database")
        return {"status": "Failed.", "err_msg": "No notes exist for this profile."}


    def put(self, profile_id):
        # verify fields
        args = notes_put_args.parse_args()
        # date
        x = datetime.now().__str__().replace(" ", "")
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
            cursor = db.cursor()
            # Execute the SQL command
            sql = "INSERT INTO NOTE (OWNING_USER, DATE, TITLE, BODY, STARRED, CREATION_DEVICE, TIMEZONE) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            val = (profile_id, x, args['title'], args['body'], args['starred'], args['creation_device'], args['time_zone'])
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
        args = notes_del_args.parse_args()
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
            cursor = db.cursor()
            # Execute the SQL command
            sql = "DELETE FROM NOTE WHERE OWNING_USER = '" + profile_id + "' AND DATE = '" + args['id'] + "%'"
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            core_functions.debug_log(user=profile_id,
                                     command_run="Note Delete Entry", device_id=args['device_id'], command_id="000503",
                                     return_code="404", debug_msg="Failed to delete note.")
            return {"status": "Failed. Most likely means the note does not exist or bad input."}
        return {"status": "Completed"}


# todo make this actually work
    def patch(self, profile_id):
        # verify fields
        args = notes_patch_args.parse_args()
        # get the note and store it


        # check what's in our note
        valuesOriginal = ['title','body','creation_device','starred','time_zone']
        valuesToCopy = args.values()
        inc = 1
        for value in valuesOriginal:
            if value == valuesToCopy[inc]:
                valuesOriginal[inc] = valuesToCopy[inc]

        # final db query to store the updated note

        # UPDATE employees SET email = 'mary.patterson@classicmodelcars.com' WHERE employeeNumber = 1056;

        # log
        core_functions.debug_log(user=profile_id, command_run="Update Note", device_id=args['device_id'], command_id="000504", return_code="201", debug_msg="Note Updated.")
        # todo update entry at a date with info provided in json
        return {"status": "Code will go here, but this returned correctly?"}