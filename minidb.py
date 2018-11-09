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
import re
import time
import datetime
# Remote libraries
import sqlite3
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
# local
import common# Things like logging setup

# ===== Let us define tables =====
# We should really understand what we're doing, but we don't always get everything we want.


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
    exported = sqlalchemy.Column(sqlalchemy.Boolean, default=None)# Has this image already been exported to zip? True=yes, False=Any other value.
    exported_date = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), default=None)# Unix time. When this row was last exported. If not previously exported then NULL.
    broken = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)# Is there a problem with the image somehow? e.g. expected file does not exist. (0=No problem, all other integers=some specific problem case.)
    # Actual data about the files
    board_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    origin_media_id = sqlalchemy.Column(sqlalchemy.Integer)# (media_id column in Foolfuuka)
    md5_full = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)#File MD5 stored as a base64 string. Fixed length. (media_hash column in Foolfuuka)
    time_uploaded = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)# ?might be unixtime? that this filename was uploaded, based on the fact that 4chan image numbers are timestamps.
    filename_full = sqlalchemy.Column(sqlalchemy.String)# Filename of full version, if no filename then NULL. (media column in Foolfuuka)
    filename_thumb_op = sqlalchemy.Column(sqlalchemy.String)# Filename of op thumbnail, if no filename then NULL. (preview_op column in Foolfuuka)
    filename_thumb_reply = sqlalchemy.Column(sqlalchemy.String)# Filename of reply thumbnail, if no filename then NULL. (preview_reply column in Foolfuuka)
# ===== /Define tables =====




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
    logging.info('image_to_add.md5_full = {0!r}'.format(image_to_add.md5_full))
    exists_q = session.query(Image)\
        .filter(Image.md5_full == image_to_add.md5_full)
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


def convert_filepath_to_connect_string(filepath):
    """Convert a SQLite file filepath to a SQLAlchemy connection string"""
    # Convert windows-style backslashes to required forwardslashes
    fp_fslash = re.sub(r'\\\\', '/', filepath)
    connect_string = 'sqlite:///{0}'.format(fp_fslash)
    return connect_string


def get_current_unix_time_int():
    """Return the current UTC+0 unix time as an int"""
    # Get current time at UTC+0
    # Convert to time tuple
    # Convert time tuple to float seconds since epoch
    # Convert float to int
    current_unix_time_int = int(time.mktime(datetime.datetime.utcnow().timetuple()))
    return current_unix_time_int



class MiniDB():# WIP
    """Handle DB things for these tools, but using classes!"""
    # Create empty class vars. Any class instance vars should be initialized here to ensure a full list of them is easily available.
    connection_string = None# SQLAlchemy connection string
    echo_sql = None# Echo SQL emitted by SQLAlchemy
    db_filepath = None# Filepath of SQLite DB file
    db_dir = None# Dir portion of SQLite DB filepath
    engine = None# Actual SQLAlchemy DB engine object
    session = None# Actual SQLAlchemy DB session object

    def __init__(self, db_filepath, echo_sql=True):# WIP
        """Class startup."""
        logging.debug('MiniDB.__init__() called')
        self.db_filepath = db_filepath
        self.echo_sql = echo_sql
        self.db_dir, self.db_filename = os.path.split(self.db_filepath)
        assert(len(self.db_filename) != 0)# We need a filename

        self.connection_string = convert_filepath_to_connect_string(self.db_filepath)
        return

    def connect(self):# WIP
        """Start up DB stuff so DB interaction can happen."""
        logging.debug('Connecting to DB')
        # Ensure DB has a dir to be put in
        if len(self.db_dir) != 0:
            if not os.path.exists(self.db_dir):
                os.makedirs(self.db_dir)
        # Start the DB engine
        self.engine = sqlalchemy.create_engine(
            self.connection_string,# Points SQLAlchemy at a DB
            echo=True# Output DB commands to log
        )
        # Link table/class mapping to DB engine and make sure tables exist.
        Base.metadata.bind = self.engine# Link 'declarative' system to our DB
        Base.metadata.create_all(checkfirst=True)# Create tables based on classes
        # Create a session to interact with the DB
        self.SessionClass = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.session = self.SessionClass()
        return

    def close(self):# WIP
        """End DB insteraction gracefully.
        The class instance should be mostly useless after this is called."""
        logging.debug('Closing DB Connection')
        self.session.close()# Release connection back to pool.
        self.engine.dispose()# Close all connections.
        return

    def add_img(self, board_name, origin_media_id, md5_full, time_uploaded,
        filename_full, filename_thumb_op, filename_thumb_reply):
        """
        Add an image to the DB.
        This does not commit changes on it's own.
        (An image can be any stored media file, not just 2d static graphics. Basically can be arbitrary data.)
        board_name: shortname of board, we import from the FF <BOARDNAME>_images table.
        origin_media_id: FF 'media_id'.
        md5_full: md5 of the full image encoded as base 64, FF 'media_hash'.
        time_uploaded: The unixtime the image was uploaded, can be determined from the digits in the filename.
        filename_full: Filename of the full-sized version of the image, FF 'media'.
        filename_thumb_op: Filename of the OP version of the image, FF 'preview_op'.
        filename_thumb_reply: Filename of the small version of the image, FF 'preview_reply'.
        """
        logging.debug('Adding image to DB')
        image_already_added = self.check_for_image(md5_full)
        if image_already_added:
            logging.error('Image is already in DB')
            return
        new_image = Image(
            # Internal recordkeeping
            exported=None,# New image, therefore not exported
            exported_date=None,# New image, therefore not exported
            broken=0,# Not known to be broken
            # Actual data about image/files
            board_name=board_name,
            origin_media_id=origin_media_id,
            md5_full=md5_full,
            time_uploaded=time_uploaded,
            filename_full=filename_full,
            filename_thumb_op=filename_thumb_op,
            filename_thumb_reply=filename_thumb_reply
        )
        self.session.add(new_image)
        return

    def check_for_image(self, md5_full):
        """
        Check for the presence of an image in the DB
        md5_full: md5 of the full image encoded as base 64
        """
        # TODO: Better comparison method, using only md5 might miss results?
        logging.debug('Checking if image is in DB')
        # Check if in table
        logging.info('check_for_image.md5_full={0!r}'.format(md5_full))
        exists_q = self.session.query(Image)\
            .filter(Image.md5_full == md5_full)
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

    def find_new(self, max_rows):
        logging.debug('Finding unprocessed rows, max_rows={0!r}'.format(max_rows))
        query = self.session.query(Image)\
            .filter_by(exported=False)\
            .limit(max_rows)
        num_rows = query.count()
        logging.debug('Finished finding rows num_rows={0!r}'.format(num_rows))
        return query

    def mark_done(self, row):
        logging.debug('Marking row as dome, row.primary_key = {0!r}'.format(row.primary_key))
        unix_time_now = get_current_unix_time_int()
        row.exported = True
        row.exported_date = datetime.datetime.utcnow
        return

    def commit(self):
        """If a commit happens, it happens in this method"""
        logging.debug('Committing')
        self.session.commit()
        return

    def import_range_from_ff(self):
        """Import a group of rows from foolfuuka"""
        assert(False)# TODO: Impliment
        return


def main():
    logging.debug('main() called')

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
