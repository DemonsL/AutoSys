# coding: utf-8
import os, sys, shutil
sys.path.append('../')
import json
import logging
import datetime
import pandas as pd
from Config import api_config
from Models import bussiness
from Models import search_words


formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_name = '/home/develop/logs/file_to_sql/{}.log'.format(datetime.date.today())
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


class FileToSql:

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
                data_to_sql = eval(tb_excute)(snap_date, data)
                s_session.add(data_to_sql)
            s_session.commit()

    def data_to_json(self, file_name):
        f_format = file_name.split('.')[1]
        data = ''
        data_time = ''
        if f_format == 'csv':
            data = pd.read_csv(file_name, encoding='utf-8')
        if f_format == 'xlsx':
            d_keys = pd.read_excel(file_name, encoding='utf-8').keys()
            data_time = d_keys[4].split('-')[1].strip(']').strip()
            data = pd.read_excel(file_name, header=1, encoding='utf-8')
        json_data = json.loads(data.to_json(orient='records'))
        return json_data, data_time


def start_add_files(f_name, s_path, d_path, tb_name):
    ets = FileToSql()
    f_path = s_path + f_name
    resp_data, resp_time = ets.data_to_json(f_path)
    if tb_name == 'AscAsinBussiness':
        f_date = f_name.split('_')[0]
        f_country = f_name.split('_')[1].split('.')[0]
        ets.add_to_sql(tb_name, resp_data, snap_date=f_date, country=f_country)
        shutil.move(f_path, d_path)
    if tb_name in ['AscSearchWeek', 'AscSearchMonth']:
        data_week = datetime.datetime.strptime(resp_time, '%m/%d/%y').strftime('%Y%V')
        ets.add_to_sql(tb_name, resp_data, snap_date=data_week)
        d_name = data_week + '.xlsx'
        os.renames(f_name, d_name)
        shutil.move(s_path + d_name, d_path)
    log.info('Add %s to sql success, moving file bak...' % f)


if __name__ == '__main__':

    tb_names = api_config.file_sql_name
    for tb in tb_names:
        src_path = api_config.file_path.get(tb).get('src')
        dst_path = api_config.file_path.get(tb).get('dst')

        files = os.listdir(src_path)
        if files:
            log.info('Starting add file to sql... | FileCount: %s' % len(files))
            for f in files:
                try:
                    start_add_files(f, src_path, dst_path, tb)
                except Exception as e:
                    log.error('Add to sql error: %s' % e)
            log.info('Add file to sql success!')
        else:
            log.info('TB: %s Now is no files.' % tb)