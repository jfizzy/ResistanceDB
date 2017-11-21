import datetime
import sqlite3
from mia_backend import raw_file

class MiaDB():
    """ handle mia database interaction """
    SQLITE3_DATEFORMAT = "%Y-%m-%d %H:%M:%S.000"

    def __init__(self, database):
        try:
            self._connection = sqlite3.connect(database)
        except Exception as ex:
            print("Exception: {}".format(str(ex)))

        self._master_table = "files"

    def insert(self, file):
        """ inserts a file into the database as being moved """
        if not isinstance(file, raw_file.RawFile):
            return

        #YYYY-MM-DD HH:MM:SS.SSS

        filename = file.get_full_file_src()
        datecreated = file.get_formatted_cdate(self.SQLITE3_DATEFORMAT)
        datemoved = datetime.datetime.now().strftime(self.SQLITE3_DATEFORMAT)
        newlocation = file.get_full_file_dest()

        query = "INSERT INTO {} ".format(self._master_table)
        query += " VALUES (?,?,?,?)"


        print(query)
        self._connection.execute(query, (filename, datecreated, datemoved, newlocation))
        self._connection.commit()



        