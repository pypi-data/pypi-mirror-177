import psycopg2
import pandas as pd
import sys


class DBConnector:
    def __init__(self, log, params_db, debug):
        self.log = log
        if debug:
            self.connection = None
            self.cursor = None
            self.simulation = True
            self.log.info("Debug mode. No connection made to the PostgreSQL database.")
        else:
            try:
                self.log.info(f'Connecting to the database.')
                self.log.info(
                    f'HOST: {params_db["host"]}, DATABASE: {params_db["database"]}, USER: {params_db["user"]}, PORT: {params_db["port"]}')
                connection = psycopg2.connect(**params_db)
                cursor = connection.cursor()
                self.log.info('Connected.')
                self.simulation = False
            except psycopg2.Error as ex:
                connection = None
                cursor = None
                sqlstate = ex.args[1]
                self.log.warning('Error connecting to database: ' + sqlstate)
                self.simulation = False

            self.connection = connection
            self.cursor = cursor

    def executeSelectQuery(self, query, debug_file, returntype="dataframe"):
        if not self.simulation:
            self.log.info("Executing query.")
            self.cursor.execute(query)
            columns = [desc[0] for desc in self.cursor.description]
            data = self.cursor.fetchall()
            if returntype == "dataframe":
                output = pd.DataFrame(list(data), columns=columns)
            else:
                output = {"columns": columns, "data": data}
        else:
            if ".csv" in debug_file:
                output = pd.read_csv(debug_file)
            elif ".xlsx" in debug_file:
                output = pd.read_excel(debug_file)
            else:
                self.log.warning(f"No valid debug file extension. Supported: ['.csv', '.xlsx']. Used: .{debug_file.split('.')[1]}")
                sys.exit(-1)
        return output

    def executeInsertQuery(self, query, record_to_insert):
        self.log.info("Executing query.")
        self.cursor.execute(query, record_to_insert)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
        self.log.info("Connection closed.")
