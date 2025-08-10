# models/tables.py
from sqlalchemy import Column, BigInteger, Integer, String, Date, ForeignKey, DECIMAL, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Race(Base):
    __tablename__ = 'races'
    race_id = Column(BigInteger, primary_key=True, comment="例: 202507210901")
    date = Column(Date, nullable=False)
    venue = Column(String(50), nullable=False, comment="開催地")
    race_number = Column(Integer, nullable=False, comment="第何レース")
    distance = Column(Integer, comment="距離(m)")
    track_type = Column(String(10), comment="芝・ダート")
    course_shape = Column(String(10), comment="左回り・右回り")
    weather_text = Column(String(50), comment="天候")
    avg_temp = Column(DECIMAL(4,1))
    max_temp = Column(DECIMAL(4,1))
    min_temp = Column(DECIMAL(4,1))
    avg_humidity = Column(DECIMAL(4,1))
    max_wind_kph = Column(DECIMAL(4,1))
    track_condition = Column(String(20), comment="良・稍重など")

# horses, entries, odds, results, payouts, workouts も同様に定義
