# coding: utf-8
import json
import pandas as pd
from Models import bussiness
from Models import search_words


class ExcelToSql:

    def add_to_sql(self, tb_name, json_data, snap_date=None, country=None):
        if tb_name == 'AscAsinBussiness':
            tb_excute = 'bussiness.{}'.format(tb_name)
            b_session = bussiness.DBSession()
            for data in json_data:
                data_to_sql = eval(tb_excute)(snap_date, country, data)
                b_session.add(data_to_sql)
            b_session.commit()

        if tb_name in ['AscSearchWeek', 'AscSearchMonth']:
            tb_excute = 'search_words.{}'.format(tb_name)
            s_session = search_words.DBSession()
            for data in json_data:
                data_to_sql = eval(tb_excute)(data)
                s_session.add(data_to_sql)
            s_session.commit()

    def data_to_json(self, file_name):
        f_format = file_name.split('.')[1]
        data = ''
        if f_format == 'csv':
            data = pd.read_csv(file_name, encoding='utf-8')
        if f_format == 'xlsx':
            # d_keys = pd.read_excel(file_name, encoding='utf-8').keys()
            data = pd.read_excel(file_name, encoding='utf-8')
        json_data = data[:3].to_json(orient='records')
        return json.loads(json_data)


if __name__ == '__main__':

    tb_name = 'AscSearchWeek'
    csv_file_name = '/home/data/keyword/parse/week/201810Amazon Search Terms_US.xlsx'
    print(tb_name, csv_file_name)
    # file_date = csv_file_name.split('/')[-1].split('_')[1]
    # file_mkp = csv_file_name.split('/')[-1].split('_')[2].split('.')[0]

    ets = ExcelToSql()
    resp_data = ets.data_to_json(csv_file_name)
    ets.add_to_sql(tb_name, resp_data)
