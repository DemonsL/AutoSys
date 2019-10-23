# coding: utf-8
from Config import db
from sqlalchemy import Column, String, Integer, Float, DECIMAL, Boolean, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DBConnection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % \
               (db.User, db.Passwd, db.Host, db.Port, db.DB, db.CharSet)
engine = create_engine(DBConnection)
DBSession = sessionmaker(bind=engine)

Base = declarative_base()
class AscAsinBussiness(Base):

    __tablename__ = 'Asc_Asin_Bussiness'

    ID = Column(Integer, primary_key=True)
    SnapDate = Column(DateTime)
    Country = Column(String(10))
    ParentAsin = Column(String(15))
    Asin = Column(String(15))
    Title = Column(String(500))
    Sessions = Column(Integer)
    SessionPercentage = Column(DECIMAL(10, 4))
    PageViews = Column(Integer)
    PageViewsPercentage = Column(DECIMAL(10, 4))
    BuyBoxPercentage = Column(DECIMAL(10, 4))
    Units = Column(Integer)
    UnitSessionPercentage = Column(DECIMAL(10, 4))
    Revenue = Column(DECIMAL(10, 4))
    Orders = Column(Integer)

    def __init__(self, SnapDate, Country, json_data):
        self.SnapDate = SnapDate
        self.Country = Country
        self.ParentAsin = json_data.get('(Parent) ASIN')
        self.Asin = json_data.get('(Child) ASIN')
        self.Title = json_data.get('Title')
        self.Sessions = json_data.get('Sessions')
        self.SessionPercentage = self.percentage_to_float(json_data.get('Session Percentage'))
        self.PageViews = json_data.get('Page Views')
        self.PageViewsPercentage = self.percentage_to_float(json_data.get('Page Views Percentage'))
        self.BuyBoxPercentage = self.percentage_to_float(json_data.get('Buy Box Percentage'))
        self.Units = json_data.get('Units Ordered')
        self.UnitSessionPercentage = self.percentage_to_float(json_data.get('Unit Session Percentage'))
        self.Revenue = float(json_data.get('Ordered Product Sales').strip('$').replace(',', ''))
        self.Orders = json_data.get('Total Order Items')

    def percentage_to_float(self, per_value):
        if per_value:
            f_value = float(per_value.strip('%')) / 100
            return f_value
