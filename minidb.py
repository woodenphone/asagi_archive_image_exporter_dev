#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     01-11-2018
# Copyright:   (c) User 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# StdLib
import logging
import os
# Remote libraries
import sqlite3
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
# local
import common# Things like logging setup



# Notes
# https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
# https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime



def get_time_int_from_filename(filename):
    """Convert an asagi/foolfuuka filename into the time it was posted.
    Based on the fact that 4chan image numbers are timestamps.
    Hopefully this is faster than regex."""
    filename_pieces = filename.split('.')
    numerals = filename_pieces[0]
    time_int = int(numerals)
    return time_int






Base = declarative_base()

class Image(Base):
    """Table to store data for the images we've been working with"""
    __tablename__ = 'Images'
    # Internal record keeping stuff
    primaty_key = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)# Just has to be unique
    record_created = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), server_default=func.utcnow())# Unix time. When this row was created.
    record_updated = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), onupdate=func.utcnow())# Unix time. When this row was last updated.
    # Actual data about the files
    board_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    md5b64 = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)#File MD5 stored as a base64 string. Fixed length
    disk_filename = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    est_time_uploaded = sqlalchemy.Column(sqlalchemy.Integer)# ?might be unixtime? that this filename was uploaded, based on the fact that 4chan image numbers are timestamps.




# Given a DB filepath, make sure we have a dir to put it in and create the connection string
db_path = os.path.join('temp','images.sqlite')
connect_string = 'sqlite:///'.format(db_path)

# Ensure DB dir exists.
db_dir = os.path.dirname(db_path)
if len(db_dir) > 0:# Only try to make a dir if ther is a dir to make.
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = sqlalchemy.create_engine('sqlite:///temp/images.sqlite')


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)




new_image = Image(board_name='mlp')
session.add(new_image)
session.commit()








class MiniDB():
    """Handle DB things for these tools"""
    # Create empty class vars
    connection_string = None
    db_filepath = None

    def __init__(self, connection_string):
        return
    def connect(self):
        return












def main():
    pass

if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "minidb.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception, e:
        logging.critical("Unhandled exception!")
        logging.exception(e)
    logging.info( "Program finished.")
