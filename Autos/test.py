# coding: utf-8
import os, sys, shutil
sys.path.append('../')
import json
import logging
import datetime
import pandas as pd
from Models import bussiness
from Models import search_words


formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_name = '/home/develop/logs/excel_to_sql/{}.log'.format(datetime.date.today())
log = logging.getLogger()
log.setLevel(logging.INFO)

fh = logging.FileHandler(file_name, mode='a+')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
log.addHandler(ch)


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
        json_data = data.to_json(orient='records')
        return json.loads(json_data)


if __name__ == '__main__':

    tb_name = 'AscSearchWeek'
    file_path = '/home/data/keyword/parse/week/'
    dst_path = '/home/data/keyword/achieve/week/'
    # file_date = csv_file_name.split('/')[-1].split('_')[1]
    # file_mkp = csv_file_name.split('/')[-1].split('_')[2].split('.')[0]


    files = os.listdir(file_path)
    if files:
        for f in files:
            f_name = file_path + f
            ets = ExcelToSql()
            resp_data = ets.data_to_json(f_name)
            try:
                ets.add_to_sql(tb_name, resp_data)
                log.info('Add %s to sql success, moving file...' % f_name)
                shutil.move(f_name, dst_path + f)
            except Exception as e:
                log.error('Add to sql error: %s' % e)
    else:
        log.info('Now is no files.')
