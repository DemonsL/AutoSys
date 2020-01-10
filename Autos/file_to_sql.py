# coding: utf-8
import sys
sys.path.append('../')
import os, shutil
import json
import logging
import datetime
import pandas as pd
from Config import api_config
from Models import bussiness
from Models import search_words
from Models import settlements


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

    currency = ''
    invoice = ''

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

        if tb_name == 'AscPayments':
            st_session = settlements.DBSession()
            for data in json_data:
                d_type = data.get('type')
                if d_type in ['Order', 'Refund', '注文', '返金']:
                    data_to_sql = settlements.AscPaymentsOrder(country, self.currency, self.invoice, data)
                elif d_type in ['Transfer', 'マイナス残高']:
                    data_to_sql = settlements.AscPaymentsAccount(country, self.currency, self.invoice, data)
                else:
                    data_to_sql = settlements.AscPaymentsFee(country, self.currency, self.invoice, data)
                st_session.add(data_to_sql)
            st_session.commit()

    def get_bussiness(self, snap_date):
        session = bussiness.DBSession()
        buss = session.query(bussiness.AscAsinBussiness, bussiness.AscAsinBussiness.SnapDate)\
                      .filter_by(SnapDate=snap_date).all()
        session.close()
        return buss

    def delete_bussiness(self, snap_date):
        session = bussiness.DBSession()
        buss = session.query(bussiness.AscAsinBussiness).filter_by(SnapDate=snap_date).all()
        for bu in buss:
            session.delete(bu)
        session.commit()

    def delete_payments(self, snap_date, country, inv_type):
        session = settlements.DBSession()
        del_orders = 'delete from Asc_Payments_Order where date_format(PurchaseDate, "%Y%m") = "{sd}" ' \
                     'and Country = "{ct}" and InvoiceType = "{it}"'.format(sd = snap_date,
                                                                            ct = country,
                                                                            it = inv_type)
        del_fees = 'delete from Asc_Payments_Fee where date_format(SnapDate, "%Y%m") = "{sd}" ' \
                   'and Country = "{ct}" and InvoiceType = "{it}"'.format(sd = snap_date,
                                                                          ct = country,
                                                                          it = inv_type)
        del_account = 'delete from Asc_Payments_Account where date_format(SnapDate, "%Y%m") = "{sd}" ' \
                      'and Country = "{ct}" and InvoiceType = "{it}"'.format(sd = snap_date,
                                                                             ct = country,
                                                                             it = inv_type)
        session.execute(del_orders)
        session.execute(del_fees)
        session.execute(del_account)
        session.commit()
        session.close()


    def data_to_json(self, tb_name, file_name, country=None):
        f_format = file_name.split('.')[1]
        data = ''
        data_time = ''
        if f_format == 'csv':
            if tb_name == 'AscPayments':
                h_num = 7 if (country in ['US', 'CA']) else 6
                if country in ['US', 'CA', 'UK']:
                    self.currency = pd.read_csv(file_name, nrows=1, encoding='utf-8').values[0][0].split(',')[0].split(' ')[-1]
                elif country == 'JP':
                    self.currency = 'JPY'
                data = pd.read_csv(file_name, header=h_num, encoding='utf-8')
            else:
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
    if tb_name == 'AscAsinBussiness':
        f_date = f_name.split('_')[0]
        f_country = f_name.split('_')[1].split('.')[0]
        # 数据有更新时删除旧数据
        if ets.get_bussiness(f_date):
            ets.delete_bussiness(f_date)
        resp_data, resp_time = ets.data_to_json(tb_name, f_path)
        ets.add_to_sql(tb_name, resp_data, snap_date=f_date, country=f_country)
        shutil.move(f_path, d_path)
    if tb_name in ['AscSearchWeek', 'AscSearchMonth']:
        resp_data, resp_time = ets.data_to_json(tb_name, f_path)
        data_period = ''
        if tb_name == 'AscSearchWeek':
            data_period = datetime.datetime.strptime(resp_time, '%m/%d/%y').strftime('%Y%V')
        if tb_name == 'AscSearchMonth':
            data_period = datetime.datetime.strptime(resp_time, '%m/%d/%y').strftime('%Y%m')
        ets.add_to_sql(tb_name, resp_data, snap_date=data_period)
        d_name = data_period + '.xlsx'
        new_path = s_path + d_name
        os.renames(f_path, new_path)
        shutil.move(new_path, d_path)
    if tb_name == 'AscPayments':
        f_date = f_name.split('.')[0].split('_')[0]
        f_country = f_name.split('.')[0].split('_')[1]
        ets.invoice = 'Invoiced' if (f_name.split('.')[0].split('_')[-1] == 'Inv') else 'Standard'
        # 数据有更新时删除旧数据
        log.info('Delete old data...')
        ets.delete_payments(f_date, f_country, ets.invoice)
        log.info('Delete old data end!')
        resp_data, resp_time = ets.data_to_json(tb_name, f_path, country=f_country)
        ets.add_to_sql(tb_name, resp_data, country=f_country)
        if os.path.exists(d_path + f_name):
            os.remove(d_path + f_name)
        shutil.move(f_path, d_path)
    log.info('Add %s: %s to sql success, moving file bak...' % (tb_name, f))


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
