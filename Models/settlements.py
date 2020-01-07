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
    marketplace = Column(String(30))
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
        self.PurchaseDate = date_format(order_detail.get('date/time').strip(' PST'))
        self.Country = country
        self.InvoiceType = invoice
        self.SettlementId = order_detail.get('settlement id')
        self.Type = order_detail.get('type')
        self.AmazonOrderId = order_detail.get('order id')
        self.Sku = order_detail.get('sku')
        self.Unit = order_detail.get('quantity')
        self.marketplace = order_detail.get('marketplace')
        self.Logistics = order_detail.get('fulfillment')
        self.AddrCity = order_detail.get('order city')
        self.AddrState = order_detail.get('order state')
        self.AddrPostal = order_detail.get('order postal')
        self.TaxModel = order_detail.get('tax collection model')
        self.Revnue = fee_format(order_detail.get('product sales'))
        self.TaxRevnue = fee_format(order_detail.get('product sales tax'))
        self.RevShipping = fee_format(order_detail.get('shipping credits'))
        self.TaxShipping = fee_format(order_detail.get('shipping credits tax'))
        self.RevGiftwrap = fee_format(order_detail.get('gift wrap credits'))
        self.TaxGiftwrap = fee_format(order_detail.get('giftwrap credits tax'))
        self.RevPoint = fee_format(order_detail.get('Amazonポイントの費用')) or 0
        self.FeePromotionalRebates = fee_format(order_detail.get('promotional rebates'))
        self.TaxPromotionalRebates = fee_format(order_detail.get('promotional rebates tax'))
        self.TaxMarketplaceWithheld = fee_format(order_detail.get('marketplace withheld tax'))
        self.FeeSelling = fee_format(order_detail.get('selling fees'))
        self.FeeFba = fee_format(order_detail.get('fba fees'))
        self.FeeOtherTransaction = fee_format(order_detail.get('other transaction fees'))
        self.FeeOther = fee_format(order_detail.get('other'))
        self.RevTotal = fee_format(order_detail.get('total'))
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
        self.SnapDate = date_format(account_detail.get('date/time').strip(' PST'))
        self.Country = country
        self.InvoiceType = invoice
        self.SettlementId = account_detail.get('settlement id')
        self.Type = account_detail.get('type')
        self.Description = account_detail.get('description')
        self.Amount = fee_format(account_detail.get('total'))
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
        self.SnapDate = date_format(fee_detail.get('date/time').strip(' PST'))
        self.Country = country
        self.InvoiceType = invoice
        self.SettlementId = fee_detail.get('settlement id')
        self.Type = fee_detail.get('type')
        self.FeeDescription = fee_detail.get('description')
        self.FeeAmount = fee_format(fee_detail.get('total'))
        self.Currency = currency


# 12小时制转24小时制
def date_format(src_date):
    format_str = '%b %d, %Y %I:%M:%S %p'
    return datetime.datetime.strptime(src_date, format_str)

def fee_format(fee):
    if fee and str(fee).find(','):
        return float(str(fee).replace(',', ''))
    else:
        return fee