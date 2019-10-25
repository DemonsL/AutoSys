# coding: utf-8
from Config import db
from sqlalchemy import Column, String, Integer, Float, DECIMAL, Boolean, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DBConnection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % \
               (db.User, db.Passwd, db.Host, db.Port, 'AmzSearch', db.CharSet)
engine = create_engine(DBConnection)
DBSession = sessionmaker(bind=engine)


class SearchWords:

    Department = Column(String(40))
    SearchTerm = Column(String(800))
    SearchFrequencyRank = Column(Integer, primary_key=True)
    Asin1 = Column(String(20))
    ProductTitle1 = Column(String(600))
    ClickShare1 = Column(DECIMAL(8, 6))
    ConversionShare1 = Column(DECIMAL(8, 6))
    Asin2 = Column(String(20))
    ProductTitle2 = Column(String(600))
    ClickShare2 = Column(DECIMAL(8, 6))
    ConversionShare2 = Column(DECIMAL(8, 6))
    Asin3 = Column(String(20))
    ProductTitle3 = Column(String(600))
    ClickShare3 = Column(DECIMAL(8, 6))
    ConversionShare3 = Column(DECIMAL(8, 6))

    def __init__(self, json_data):
        self.Department = json_data.get('Department')
        self.SearchTerm = json_data.get('Search Term')
        self.SearchFrequencyRank = json_data.get('Search Frequency Rank')
        self.Asin1 = json_data.get('#1 Clicked ASIN')
        self.ProductTitle1 = json_data.get('#1 Product Title')
        self.ClickShare1 = json_data.get('#1 Click Share')
        self.ConversionShare1 = self.convert_to_float(json_data.get('#1 Conversion Share'))
        self.Asin2 = json_data.get('#2 Clicked ASIN')
        self.ProductTitle2 = json_data.get('#2 Product Title')
        self.ClickShare2 = json_data.get('#2 Click Share')
        self.ConversionShare2 = json_data.get('#2 Conversion Share')
        self.Asin3 = json_data.get('#3 Clicked ASIN')
        self.ProductTitle3 = json_data.get('#3 Product Title')
        self.ClickShare3 = json_data.get('#3 Click Share')
        self.ConversionShare3 = json_data.get('#3 Conversion Share')

    def convert_to_float(self, value):
        try:
            if not isinstance(value, float) and not isinstance(value, str):
                return float(value)
        except Exception as e:
            print(e)



Base = declarative_base(cls=SearchWords)
class AscSearchWeek(Base):

    __tablename__ = 'Asc_Search_Week'

    Week = Column(Integer, primary_key=True)

    def __init__(self, json_data):
        SearchWords.__init__(self, json_data)
        self.Week = json_data.get('\u5e74\u5468')


class AscSearchMonth(Base):

    __tablename__ = 'Asc_Search_Month'

    Month = Column(Integer, primary_key=True)

    def __init__(self, json_data):
        SearchWords.__init__(self, json_data)
        self.Month = json_data.get('Month')


