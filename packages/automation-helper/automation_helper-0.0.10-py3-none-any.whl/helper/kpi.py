import datetime
from helper.db_connector import DBConnector
import json


def _getFormatDate():
    date = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
    return date


def _getQuery():
    query = """ INSERT INTO kpi.kpi (sdes, status, data, execution_date) VALUES (%s,%s,%s,%s)"""
    return query


class KPI:
    def __init__(self, db=DBConnector):
        self.DB = db
        self.date = _getFormatDate()
        self.query = _getQuery()

    def successProcess(self, sdes, log):
        json_data = {
                    'detail': log
                }
        data = json.dumps(json_data)
        
        record_to_insert = (sdes, 200, data, self.date)
        self.DB.executeInsertQuery(self.query, record_to_insert)

    def systemException(self, sdes, log):
        json_data = {
                    'detail': log
                }
        data = json.dumps(json_data)
        
        record_to_insert = (sdes, 503, data, self.date)
        self.DB.executeInsertQuery(self.query, record_to_insert)

    def businessException(self, sdes, log):
        json_data = {
                    'detail': log
                }
        data = json.dumps(json_data)
        
        record_to_insert = (sdes, 417, data, self.date)
        self.DB.executeInsertQuery(self.query, record_to_insert)
