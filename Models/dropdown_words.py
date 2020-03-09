# coding: utf-8
from Config import db
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DBConnection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % \
               (db.User, db.Passwd, db.Host, db.Port, 'Xcentz-New', db.CharSet)
engine = create_engine(DBConnection, pool_size=30, max_overflow=0)
DBSession = sessionmaker(bind=engine)

Base = declarative_base()
class ApbSpKeywordsRelation(Base):

    __tablename__ = 'Apb_Sp_Keywords_Relation'

    ID = Column(Integer)
    Country = Column(String(10), primary_key=True)
    Category = Column(String(50), primary_key=True)
    PKeyword = Column(String(100), primary_key=True)
    CKeywordRank = Column(Integer)
    CKeyword = Column(String(200), primary_key=True)
    SnapDate = Column(DateTime, primary_key=True)

    def __init__(self, country, category, snap_date, params):
        self.Country = country
        self.Category = category
        self.PKeyword = params.get('PKeyword')
        self.CKeywordRank = params.get('CKeywordRank')
        self.CKeyword = params.get('CKeyword')
        self.SnapDate = snap_date