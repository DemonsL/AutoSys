# coding: utf-8
import json
import pandas as pd
from Models import bussiness


class ExcelToSql:

    def add_to_sql(self, snap_date, country, json_data):
        session = bussiness.DBSession()
        for data in json_data:
            data_to_sql = bussiness.AscAsinBussiness(snap_date, country, data)
            session.add(data_to_sql)
        session.commit()

    def csv_to_json(self, file_name):
        csv_data = pd.read_csv(file_name, encoding='utf-8')
        json_data = csv_data.to_json(orient='records')
        return json.loads(json_data)

if __name__ == '__main__':

    csv_file_name = 'C:/Users/coolpad/Downloads/BusinessReport_2019-10-19_US.csv'
    file_date = csv_file_name.split('/')[-1].split('_')[1]
    file_mkp = csv_file_name.split('/')[-1].split('_')[2].split('.')[0]

    ets = ExcelToSql()
    resp_data = ets.csv_to_json(csv_file_name)
    ets.add_to_sql(file_date, file_mkp, resp_data)
