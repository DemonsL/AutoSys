# coding: utf-8
from .settings import User, Passwd, Host, Port, DB, CharSet
from sqlalchemy import Column, String, Integer, DECIMAL, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DBConnection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % \
               (User, Passwd, Host, Port, DB, CharSet)
engine = create_engine(DBConnection)
DBSession = sessionmaker(bind=engine)

Base = declarative_base()
class ApbBestSeller(Base):

    __tablename__ = 'Apb_Best_Seller'

    ID = Column(Integer)
    SnapDate = Column(DateTime, primary_key=True)
    Country = Column(String(10), primary_key=True)
    CategoryID = Column(String(50), primary_key=True)
    Rank = Column(Integer, primary_key=True)
    Asin = Column(String(20))
    Title = Column(String(400))
    Keywords = Column(String(400))
    Pic = Column(String(50))
    Review = Column(Integer)
    Star = Column(DECIMAL(4, 1))
    Price = Column(DECIMAL(8, 2))

    def __init__(self, snap_date, best_seller):
        self.SnapDate = snap_date
        self.Country = best_seller.get('Country')
        self.CategoryID = best_seller.get('CategoryID')
        self.Rank = best_seller.get('Rank')
        self.Asin = best_seller.get('Asin')
        self.Title = best_seller.get('Title')
        self.Keywords = best_seller.get('Keywords')
        self.Pic = best_seller.get('Pic')
        self.Review = best_seller.get('Review')
        self.Star = best_seller.get('Star')
        self.Price = best_seller.get('Price')

def update_best_seller(best_seller):
    return {
        'Asin' : best_seller.get('Asin'),
        'Title' : best_seller.get('Title'),
        'Keywords' : best_seller.get('Keywords'),
        'Pic' : best_seller.get('Pic'),
        'Review' : best_seller.get('Review'),
        'Star' : best_seller.get('Star'),
        'Price' : best_seller.get('Price')
    }


class PubCategory(Base):

    __tablename__ = 'Pub_Category'

    SubCategoryID = Column(String(100), primary_key=True)
    Level  = Column(Integer)



