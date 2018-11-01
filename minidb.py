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
#from sqlalchemy.ext.declarative import declarative_base
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






def get_connect_string():
    # Given a DB filepath, make sure we have a dir to put it in and create the connection string
    db_path = os.path.join('temp','images.sqlite')
    logging.debug('db_path = {0!r}'.format(db_path))

    # Ensure DB dir exists.
    db_dir = os.path.dirname(db_path)
    if len(db_dir) > 0:# Only try to make a dir if ther is a dir to make.
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

    # 'sqlite:///temp/images.sqlite'
    connect_string = 'sqlite:///'.format(db_path)
    logging.debug('connect_string = {0!r}'.format(connect_string))
    return connect_string




def begin_db():
    """Test starting DB as statements in a function rather than as global sequential statements"""
    logging.debug('begin_db() called')

    # ===== Put the DB somewhere =====
    # Given a DB filepath, make sure we have a dir to put it in and create the connection string
    db_path = os.path.join('temp','images.sqlite')
    logging.debug('db_path = {0!r}'.format(db_path))

    # Ensure DB dir exists.
    db_dir = os.path.dirname(db_path)
    if len(db_dir) > 0:# Only try to make a dir if ther is a dir to make.
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

    # 'sqlite:///temp/images.sqlite'
    connect_string = 'sqlite:///'.format(db_path)
    logging.debug('connect_string = {0!r}'.format(connect_string))



    # ===== Start and connect to DB =====
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = sqlalchemy.create_engine(connect_string, echo=True)


    Base = declarative_base()

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)


    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    # ===== Start a session with the DB so we can interact with it =====

    DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    session = DBSession()




    # ===== Define tables =====
    class Image(Base):
        """Table to store data for the images we've been working with"""
        # TODO: Check that we're handling timezones correctly for timestamps.
        # Ideally we should be storing as timezone-agnostic UTC+0 Unix time or similar.
        __tablename__ = 'Images'
        # Internal record keeping stuff
        primaty_key = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)# Just has to be unique
        record_created = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.func.utcnow())# Unix time. When this row was created.
        record_updated = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), onupdate=sqlalchemy.func.utcnow())# Unix time. When this row was last updated.
        # Actual data about the files
        board_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
        md5b64 = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)#File MD5 stored as a base64 string. Fixed length
        disk_filename = sqlalchemy.Column(sqlalchemy.String, nullable=False)
        est_time_uploaded = sqlalchemy.Column(sqlalchemy.Integer)# ?might be unixtime? that this filename was uploaded, based on the fact that 4chan image numbers are timestamps.



    # ===== Do stuff with our DB =====

    new_image = Image(board_name='mlp')
    session.add(new_image)
    session.commit()

    logging.debug('begin_db() returning')
    return







class MiniDB():# WIP
    """Handle DB things for these tools, but using classes!"""
    # Create empty class vars. Any class instance vars should be initialized here to ensure a full list of them is easily available.
    connection_string = None# SQLAlchemy connection string
    db_filepath = None# Filepath of SQLite DB file
    db_instance = None# Actual SQLAlchemy DB object

    def __init__(self, connection_string):# WIP
        """Class startup"""
        logging.debug('MiniDB.__init__() called')
        self.connection_string = connection_string
        return

    def connect(self):# WIP
        """Start up DB stuff so DB interaction can happen"""
        logging.debug('Connecting to DB')
        return

    def close(self):# WIP
        """End DB insteraction gracefully"""
        logging.debug('Closing DB Connection')
        return

    def add_img(self, md5_full, filename_full, filename_op, filename_small):# WIP
        """
        Add an image to the DB
        (An image can be any stored media file, not just 2d static graphics. Basically can be arbitrary data.)
        md5_full: md5 of the full image encoded as base 64
        filename_full: Filename of the full-sized version of the image
        filename_op: Filename of the OP version of the image
        filename_small: Filename of the small version of the image
        """
        logging.debug('Adding image to DB')
        return

    def check_for_image(self, md5_full):# WIP
        """
        Check for the presence of an image in the DB
        md5_full: md5 of the full image encoded as base 64
        """
        logging.debug('Checking if image is in DB')
        return




def main():
    logging.debug('main() called')
##    begin_db()
    logging.debug('main() returning')
    return


if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "minidb.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception, e:
        logging.critical("Unhandled exception!")
        logging.exception(e)
    logging.info( "Program finished.")











logging.warning('This stuff is all after a normal script would end now, just saiyan...')


logging.warning('Imports should really go at the beginning of the file.')
# https://www.blog.pythonlibrary.org/2010/09/10/sqlalchemy-connecting-to-pre-existing-databases/











# ===== Let us define tables =====
# We should really understand what we're doing, but we don't always get everything we want.

# We need a string to tell SQLAlchemy what DB we want to connect to
connect_string = get_connect_string()



engine = sqlalchemy.create_engine(# Start the DB engine
    connect_string,# Points SQLAlchemy at a DB
    echo=True# Output DB commands to log
)

Base = declarative_base()# Setup system to keep track of tables and classes






# ===== Define tables =====
class Image(Base):
    """Table to store data for the images we've been working with.
    One row per image table row."""
    # TODO: Check that we're handling timezones correctly for timestamps.
    # Ideally we should be storing as timezone-agnostic UTC+0 Unix time or similar.
    __tablename__ = 'images'
    # Internal record keeping stuff
    primary_key = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)# Just has to be unique
    record_created = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.func.utcnow())# Unix time. When this row was created.
    record_updated = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), onupdate=sqlalchemy.func.utcnow())# Unix time. When this row was last updated.
    # Actual data about the files
    board_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    origin_media_id = sqlalchemy.Column(sqlalchemy.Integer)# (media_id column in Foolfuuka)
    md5b64 = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)#File MD5 stored as a base64 string. Fixed length. (media_hash column in Foolfuuka)
    time_uploaded = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)# ?might be unixtime? that this filename was uploaded, based on the fact that 4chan image numbers are timestamps.
    filename_full = sqlalchemy.Column(sqlalchemy.String)# Filename of full version, if no filename then NULL. (media column in Foolfuuka)
    filename_thumb_op = sqlalchemy.Column(sqlalchemy.String)# Filename of op thumbnail, if no filename then NULL. (preview_op column in Foolfuuka)
    filename_thumb_reply = sqlalchemy.Column(sqlalchemy.String)# Filename of reply thumbnail, if no filename then NULL. (preview_reply column in Foolfuuka)

class File(Base):
    """Table to store data for the images we've been working with.
    One row per file."""
    # TODO: Check that we're handling timezones correctly for timestamps.
    # Ideally we should be storing as timezone-agnostic UTC+0 Unix time or similar.
    __tablename__ = 'files'
    # Internal record keeping stuff
    primary_key = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)# Just has to be unique
    record_created = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.func.utcnow())# Unix time. When this row was created.
    record_updated = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), onupdate=sqlalchemy.func.utcnow())# Unix time. When this row was last updated.
    # Actual data about the files
    board_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    md5b64 = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)#File MD5 stored as a base64 string. Fixed length
    time_uploaded = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)# ?might be unixtime? that this filename was uploaded, based on the fact that 4chan image numbers are timestamps.
    filename = sqlalchemy.Column(sqlalchemy.String)# Filename of full version, if no filename then NULL
# ===== /Define tables =====



# Link table/class mapping to DB engine and make sure tables exist.
Base.metadata.bind = engine# Link 'declarative' system to our DB
Base.metadata.create_all()# Create tables based on classes

# ===== Do things with the DB =====




new_image = Image(board_name='mlp',md5b64)
session.add()





