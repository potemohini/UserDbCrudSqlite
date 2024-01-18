import os
from subprocess import getoutput
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from os import getenv
from datetime import datetime
from loguru import logger

cdb = None
DBSession: sessionmaker = None
Base = declarative_base()
alter_table_names = ['modbus_device_registers_in_template', 'modbus_device_registers_in']


def init_db():
    try:
        global cdb, DBSession
        config_path = getenv("CONFIG_PATH")
        # cdb = create_engi
        # ne(f'sqlite:////home/pi/iam-gateway/config/config_new_mod.db', connect_args={'check_same_thread': False})
        cdb = create_engine(f'sqlite:///{config_path}/Mohini-Test.db', connect_args={'check_same_thread': False})
        # TODO: To Solve Error: (sqlite3.OperationalError) database is locked, I added below TWO-lines of Code
        conn = cdb.connect()
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.close()
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        Base.metadata.create_all(cdb)
        Base.metadata.bind = cdb
        DBSession = sessionmaker(bind=cdb)
        return True

    except Exception as e:
        logger.critical(f'{e}')
        return False


def get_session():
    if DBSession is not None:
        session = DBSession()
        return session
    else:
        return None

class Users(Base):
    __tablename__ = 'users'
    u_id = Column(Integer, primary_key=True)
    user_name = Column(String(1000), nullable=True)
    user_dob = Column(Date, default=datetime.now)
    is_deleted = Column(Integer, nullable=True)

class Address(Base):
    __tablename__ = 'address'
    a_id = Column(Integer, primary_key=True)
    u_id= Column(Integer)
    user_address = Column(String(1000), nullable=True)
    is_deleted = Column(Integer, nullable=True)


