# coding: utf-8
import datetime
from Config import db
from sqlalchemy import Column, String, Integer, Float, DECIMAL, Boolean, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DBConnection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % \
               (db.User, db.Passwd, db.Host, db.Port, db.DB, db.CharSet)
engine = create_engine(DBConnection)
DBSession = sessionmaker(bind=engine)

Base = declarative_base()
class AscPaymentsOrder(Base):

    __tablename__ = 'Asc_Payments_Order'

    ID = Column(Integer, primary_key=True)
    PurchaseDate = Column(DateTime)
    Country = Column(String(10))
    InvoiceType = Column(String(20))
    SettlementId = Column(String(11))
    Type = Column(String(10))
    AmazonOrderId = Column(String(25))
    Sku = Column(String(50))
    Unit = Column(Integer)
    marketplace = Column(String(50))
    Logistics = Column(String(30))
    AddrCity = Column(String(30))
    AddrState = Column(String(30))
    AddrPostal = Column(String(15))
    TaxModel = Column(String(30))
    Revnue = Column(DECIMAL(10, 2))
    TaxRevnue = Column(DECIMAL(10, 2))
    RevShipping = Column(DECIMAL(10, 2))
    TaxShipping = Column(DECIMAL(10, 2))
    RevGiftwrap = Column(DECIMAL(10, 2))
    TaxGiftwrap = Column(DECIMAL(10, 2))
    RevPoint = Column(DECIMAL(10, 2))
    FeePromotionalRebates = Column(DECIMAL(10, 2))
    TaxPromotionalRebates = Column(DECIMAL(10, 2))
    TaxMarketplaceWithheld = Column(DECIMAL(10, 2))
    FeeSelling = Column(DECIMAL(10, 2))
    FeeFba = Column(DECIMAL(10, 2))
    FeeOtherTransaction = Column(DECIMAL(10, 2))
    FeeOther = Column(DECIMAL(10, 2))
    RevTotal = Column(DECIMAL(10, 2))
    Currency = Column(String(20))

    def __init__(self, country, currency, invoice, order_detail):
        self.PurchaseDate = date_format(order_detail, country)
        self.Country = country
        self.InvoiceType = invoice
        self.SettlementId = all_country_value(order_detail, 'SettlementId')
        self.Type = all_country_value(order_detail, 'Type')
        self.AmazonOrderId = all_country_value(order_detail, 'AmazonOrderId')
        self.Sku = all_country_value(order_detail, 'Sku')
        self.Unit = all_country_value(order_detail, 'Unit')
        self.marketplace = all_country_value(order_detail, 'marketplace')
        self.Logistics = all_country_value(order_detail, 'Logistics')
        self.AddrCity = all_country_value(order_detail, 'AddrCity')
        self.AddrState = all_country_value(order_detail, 'AddrState')
        self.AddrPostal = all_country_value(order_detail, 'AddrPostal')
        self.TaxModel = all_country_value(order_detail, 'TaxModel')
        self.Revnue = fee_format(all_country_value(order_detail, 'Revnue'))
        self.TaxRevnue = fee_format(all_country_value(order_detail, 'TaxRevnue'))
        self.RevShipping = fee_format(all_country_value(order_detail, 'RevShipping'))
        self.TaxShipping = fee_format(all_country_value(order_detail, 'TaxShipping'))
        self.RevGiftwrap = fee_format(all_country_value(order_detail, 'RevGiftwrap'))
        self.TaxGiftwrap = fee_format(all_country_value(order_detail, 'TaxGiftwrap'))
        self.RevPoint = fee_format(all_country_value(order_detail, 'RevPoint'))
        self.FeePromotionalRebates = fee_format(all_country_value(order_detail, 'FeePromotionalRebates'))
        self.TaxPromotionalRebates = fee_format(all_country_value(order_detail, 'TaxPromotionalRebates'))
        self.TaxMarketplaceWithheld = fee_format(all_country_value(order_detail, 'TaxMarketplaceWithheld'))
        self.FeeSelling = fee_format(all_country_value(order_detail, 'FeeSelling'))
        self.FeeFba = fee_format(all_country_value(order_detail, 'FeeFba'))
        self.FeeOtherTransaction = fee_format(all_country_value(order_detail, 'FeeOtherTransaction'))
        self.FeeOther = fee_format(all_country_value(order_detail, 'FeeOther'))
        self.RevTotal = fee_format(all_country_value(order_detail, 'RevTotal'))
        self.Currency = currency


class AscPaymentsAccount(Base):

    __tablename__ = 'Asc_Payments_Account'

    SnapDate = Column(DateTime, primary_key=True)
    Country = Column(String(20), primary_key=True)
    InvoiceType = Column(String(20), primary_key=True)
    SettlementId = Column(String(20), primary_key=True)
    Type = Column(String(100))
    Description = Column(String(300))
    Amount = Column(Float(10, 2))
    Currency = Column(String(20))

    def __init__(self, country, currency, invoice, account_detail):
        self.SnapDate = date_format(account_detail, country)
        self.Country = country
        self.InvoiceType = invoice
        self.SettlementId = all_country_value(account_detail, 'SettlementId')
        self.Type = all_country_value(account_detail, 'Type')
        self.Description = all_country_value(account_detail, 'Description')
        self.Amount = fee_format(all_country_value(account_detail, 'RevTotal'))
        self.Currency = currency


class AscPaymentsFee(Base):

    __tablename__ = 'Asc_Payments_Fee'

    ID = Column(Integer, primary_key=True)
    SnapDate = Column(DateTime)
    Country = Column(String(10))
    InvoiceType = Column(String(20))
    SettlementId = Column(String(15))
    Type = Column(String(100))
    FeeDescription = Column(String(300))
    FeeAmount = Column(Float(10, 2))
    Currency = Column(String(20))

    def __init__(self, country, currency, invoice, fee_detail):
        self.SnapDate = date_format(fee_detail, country)
        self.Country = country
        self.InvoiceType = invoice
        self.SettlementId = all_country_value(fee_detail, 'SettlementId')
        self.Type = all_country_value(fee_detail, 'Type')
        self.FeeDescription = all_country_value(fee_detail, 'Description')
        self.FeeAmount = fee_format(all_country_value(fee_detail, 'RevTotal'))
        self.Currency = currency


# 不同站点时间格式
def date_format(src_date, ct):
    format_str = ''
    if ct == 'US':    # 12小时制转24小时制
        src_date = src_date.get('date/time').strip('PST').strip()
        format_str = '%b %d, %Y %I:%M:%S %p'
    if ct == 'CA':    # 12小时制转24小时制
        src_date = src_date.get('date/time').strip('PST').strip('PDT').strip()
        format_str = '%Y-%m-%d %I:%M:%S %p'
    if ct == 'UK':
        src_date = src_date.get('date/time').strip('GMT+00:00').strip()
        format_str = '%d %b %Y %H:%M:%S'
    if ct == 'JP':
        src_date = src_date.get('日付/時間').strip('JST')
        format_str = '%Y/%m/%d %H:%M:%S'
    return datetime.datetime.strptime(src_date, format_str)

# US、CA、UK、DE、JP
def all_country_value(field_data, field_type):
    field_value = ''
    if field_type == 'SettlementId':
        field_value = field_data.get('settlement id') or field_data.get('決済番号')
    if field_type == 'Type':
        field_value = field_data.get('type') or (field_data.get('トランザクションの種類').replace('注文', 'Order').replace('返金', 'Refund') if field_data.get('トランザクションの種類') else field_data.get('トランザクションの種類'))
    if field_type == 'AmazonOrderId':
        field_value = field_data.get('order id') or field_data.get('注文番号')
    if field_type == 'Sku':
        field_value = field_data.get('sku') or field_data.get('SKU')
    if field_type == 'Unit':
        field_value = field_data.get('quantity') or field_data.get('数量')
    if field_type == 'marketplace':
        field_value = field_data.get('marketplace') or field_data.get('Amazon 出品サービス')
    if field_type == 'Logistics':
        field_value = field_data.get('fulfillment') or field_data.get('fulfilment') or field_data.get('フルフィルメント')
    if field_type == 'AddrCity':
        field_value = field_data.get('order city') or field_data.get('市町村')
    if field_type == 'AddrState':
        field_value = field_data.get('order state') or field_data.get('都道府県')
    if field_type == 'AddrPostal':
        field_value = field_data.get('order postal') or field_data.get('郵便番号')
    if field_type == 'TaxModel':
        field_value = field_data.get('tax collection model')
    if field_type == 'Revnue':
        field_value = field_data.get('product sales') or field_data.get('商品売上')
    if field_type == 'TaxRevnue':
        field_value = field_data.get('product sales tax') or 0
    if field_type == 'RevShipping':
        field_value = field_data.get('shipping credits') or field_data.get('postage credits') or field_data.get('配送料')
    if field_type == 'TaxShipping':
        field_value = field_data.get('shipping credits tax') or 0
    if field_type == 'RevGiftwrap':
        field_value = field_data.get('gift wrap credits') or field_data.get('ギフト包装手数料')
    if field_type == 'TaxGiftwrap':
        field_value = field_data.get('giftwrap credits tax') or 0
    if field_type == 'RevPoint':
        field_value = field_data.get('Amazonポイントの費用') or 0
    if field_type == 'FeePromotionalRebates':
        field_value = field_data.get('promotional rebates') or field_data.get('プロモーション割引額')
    if field_type == 'TaxPromotionalRebates':
        field_value = field_data.get('promotional rebates tax') or 0
    if field_type == 'TaxMarketplaceWithheld':
        field_value = field_data.get('marketplace withheld tax') or 0
    if field_type == 'FeeSelling':
        field_value = field_data.get('selling fees') or field_data.get('手数料')
    if field_type == 'FeeFba':
        field_value = field_data.get('fba fees') or field_data.get('FBA 手数料')
    if field_type == 'FeeOtherTransaction':
        field_value = field_data.get('other transaction fees') or field_data.get('トランザクションに関するその他の手数料')
    if field_type == 'FeeOther':
        field_value = field_data.get('other') or field_data.get('その他')
    if field_type == 'RevTotal':
        field_value = field_data.get('total') or field_data.get('合計')
    if field_type == 'Description':
        field_value = field_data.get('description') or field_data.get('説明')
    return field_value

def fee_format(fee):
    if fee and str(fee).find(','):
        return float(str(fee).replace(',', ''))
    else:
        return fee