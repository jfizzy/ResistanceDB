import datetime
import sqlite3
from mia_backend import raw_file

class MiaDB():
    """ handle mia database interaction """
    SQLITE3_DATEFORMAT = "%Y-%m-%d %H:%M:%S.000"

    def __init__(self, database):

        self._database = database
        # try:
        #     self._connection = sqlite3.connect(database)
        #     self._cursor = self._connection.cursor()
        # except Exception as ex:
        #     print("Exception: {}".format(str(ex)))

        self._master_table = "files"
        self._table_columns = " filename, date_created, date_moved, new_location "

    def insert(self, file):
        """ inserts a file into the database as being moved """
        if not isinstance(file, raw_file.RawFile):
            return

        #YYYY-MM-DD HH:MM:SS.SSS

        connection = sqlite3.connect(self._database)
        cursor = connection.cursor()

        filename = file.get_full_file_src()
        datecreated = file.get_formatted_cdate(self.SQLITE3_DATEFORMAT)
        datemoved = datetime.datetime.now().strftime(self.SQLITE3_DATEFORMAT)
        newlocation = file.get_full_file_dest()

        query = "INSERT INTO {} ".format(self._master_table)
        query += " VALUES (?,?,?,?)"

        cursor.execute(query, (filename, datecreated, datemoved, newlocation))
        connection.commit()
        connection.close()

    def file_parsed(self, file):
        """ checks if a file has been parsed by querying the database """
        if not isinstance(file, raw_file.RawFile):
            return True

        connection = sqlite3.connect(self._database)
        cursor = connection.cursor()

        filename = file.get_full_file_src()
        datecreated = file.get_formatted_cdate(self.SQLITE3_DATEFORMAT)

        query = "SELECT filename, date_created, date_moved, new_location FROM {} ".format(self._master_table)
        query += " WHERE filename = ? AND date_created = ?"

        cursor.execute(query, (filename, datecreated))

        # row exists for exact filename and creation date, dont move file
        row = cursor.fetchone()
        connection.close()
        if row:
            return True

        return False







