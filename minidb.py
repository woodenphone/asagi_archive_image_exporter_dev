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

# ===== Let us define tables =====
# We should really understand what we're doing, but we don't always get everything we want.

# We need a string to tell SQLAlchemy what DB we want to connect to
connect_string = 'sqlite:///temp/images.sqlite'



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
    # May already be handled better by native SQLalchemy?
    primary_key = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)# Just has to be unique. Ideally should have no significance.
##    record_created = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), default=sqlalchemy.func.utcnow())# Unix time. When this row was created.
##    record_updated = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), onupdate=sqlalchemy.func.utcnow())# Unix time. When this row was last updated.
##    exported = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=False)# Has this image already been exported to zip? True=yes, False=No. Should never be NULL.
    exported_date = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), default=None)# Unix time. When this row was last exported. If not previously exported then NULL.
    broken = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)# Is there a problem with the image somehow? e.g. expected file does not exist. (0=No problem, all other integers=some specific problem case.)
    # Actual data about the files
    board_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    origin_media_id = sqlalchemy.Column(sqlalchemy.Integer)# (media_id column in Foolfuuka)
    md5b64 = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)#File MD5 stored as a base64 string. Fixed length. (media_hash column in Foolfuuka)
    time_uploaded = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)# ?might be unixtime? that this filename was uploaded, based on the fact that 4chan image numbers are timestamps.
    filename_full = sqlalchemy.Column(sqlalchemy.String)# Filename of full version, if no filename then NULL. (media column in Foolfuuka)
    filename_thumb_op = sqlalchemy.Column(sqlalchemy.String)# Filename of op thumbnail, if no filename then NULL. (preview_op column in Foolfuuka)
    filename_thumb_reply = sqlalchemy.Column(sqlalchemy.String)# Filename of reply thumbnail, if no filename then NULL. (preview_reply column in Foolfuuka)

##class File(Base):
##    """Table to store data for the images we've been working with.
##    One row per file."""
##    # TODO: Check that we're handling timezones correctly for timestamps.
##    # Ideally we should be storing as timezone-agnostic UTC+0 Unix time or similar.
##    __tablename__ = 'files'
##    # Internal record keeping stuff
##    primary_key = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)# Just has to be unique. Ideally should have no significance.
##    record_created = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.func.utcnow())# Unix time. When this row was created.
##    record_updated = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), onupdate=sqlalchemy.func.utcnow())# Unix time. When this row was last updated.
##    # Actual data about the files
##    board_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
##    md5b64 = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)#File MD5 stored as a base64 string. Fixed length
##    time_uploaded = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)# ?might be unixtime? that this filename was uploaded, based on the fact that 4chan image numbers are timestamps.
##    filename = sqlalchemy.Column(sqlalchemy.String)# Filename of full version, if no filename then NULL
# ===== /Define tables =====



# Link table/class mapping to DB engine and make sure tables exist.
Base.metadata.bind = engine# Link 'declarative' system to our DB
Base.metadata.create_all(checkfirst=True)# Create tables based on classes


# Create a session to interact with the DB
SessionClass = sqlalchemy.orm.sessionmaker(bind=engine)
session = SessionClass()

# Notes
# https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
# https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime


# Function and class declarations

def calculate_time_uploaded(filename_full):
    the_digits = filename_full.split('.')[0]
    time_uploaded = int(the_digits)
    return time_uploaded


def try_to_add_image(session, image_to_add):
    """Add an image if it is not already present in the table.
    No checks to see which is a better version of the data, just checks for presence."""
    # Check if in table
    logging.info('image_to_add.md5b64 = {0!r}'.format(image_to_add.md5b64))
    exists_q = session.query(Image)\
        .filter(Image.md5b64 == image_to_add.md5b64)
    first_result = exists_q.first()# Get first result, returns None if no results.
    if first_result != None:
        # Already in table
        logging.debug('Image already in table, skipping')
        pass# Do nothing.
    else:
        # Not already in table
        logging.debug('Adding image to table')
        # Add to DB.
        session.add(new_image)
        session.commit()
    return


def get_time_int_from_filename(filename):
    """Convert an asagi/foolfuuka filename into the time it was posted.
    Based on the fact that 4chan image numbers are timestamps.
    Hopefully this is faster than regex."""
    filename_pieces = filename.split('.')
    numerals = filename_pieces[0]
    time_int = int(numerals)
    return time_int




class MiniDB():# WIP
    """Handle DB things for these tools, but using classes!"""
    # Create empty class vars. Any class instance vars should be initialized here to ensure a full list of them is easily available.
    connection_string = None# SQLAlchemy connection string
    db_filepath = None# Filepath of SQLite DB file
    db_instance = None# Actual SQLAlchemy DB object

    def __init__(self, connection_string):# WIP
        """Class startup."""
        logging.debug('MiniDB.__init__() called')
        self.connection_string = connection_string
        return

    def connect(self):# WIP
        """Start up DB stuff so DB interaction can happen."""
        logging.debug('Connecting to DB')
        return

    def close(self):# WIP
        """End DB insteraction gracefully.
        The class instance should be mostly useless after this is called."""
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

    def check_for_image(self, md5_full):
        """
        Check for the presence of an image in the DB
        md5_full: md5 of the full image encoded as base 64
        """
        # TODO: Better comparison method, using only md5 might miss results?
        logging.debug('Checking if image is in DB')
        # Check if in table
        logging.info('image_to_add.md5b64 = {0!r}'.format(image_to_add.md5b64))
        exists_q = session.query(Image)\
            .filter(Image.md5b64 == image_to_add.md5b64)
        first_result = exists_q.first()# Get first result, returns None if no results.
        if first_result != None:
            # Already in table
            logging.debug('Image is in table')
            return first_result# Return result instead of just True so that the row's data is available.
        else:
            # Not already in table
            logging.debug('Image not in table')
            return False# False to signify no match.

    def decide_should_we_add_image(self, new_image):# WIP
        """Decide if an image should be inserted to the table"""
        # TODO: Better comparison method, using only md5 might miss results?
        # TODO: This function might be pointlessly redundant, consider removing later?
        return check_for_image(self, md5_full=new_image.md5_full)









def main():
    logging.debug('main() called')
##    begin_db()
    logging.debug('main() returning')
    return


if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "minidb.log.txt"))# Setup logging globally
    try:
        main()
    # Log exceptions
    except Exception, e:
        logging.critical("Unhandled exception!")
        logging.exception(e)
    logging.info("Program finished.")
