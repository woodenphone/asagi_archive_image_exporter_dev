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





##class CSVExporterZipper():# WIP
##    """This may or may not go somewhere"""
##    def __init__(self):# WIP
##        return
##
##    def add_to_zip(zip_obj, filepath, internal_path):# WIP
##        """Return whether file was added to zip"""
##        try:
##    ##        logging.debug('Zipping {0!r} as {1!r}'.format(filepath, internal_path))# PERFORMANCE This might cause slowdowns, disable outside testing
##            zip_obj.write(filepath, internal_path)
##            return True
##        except OSError, err:
##            logging.error(err)
##        return False
##
##    def generate_image_filepath(board_dir, filename):# WIP
##        # Expects filename to look like: '1536631035276.webm'
##        # Outputs: 'BASE/153/6/1536631035276.webm'
##        # boards/<boardName>/<thumb or image>/<char 0-3>/<char 4-5>/<full image name>
##        # base/image/1536/63/1536631035276.webm
##        assert(len(filename) > 4)# We can't generate a path is this is lower, and the value is based on unix time so should always be over 1,000,000
##        media_filepath = os.path.join(board_dir, filename[0:4], filename[4:6], filename)# string positions 0,1,2,3/4,5/filename
##        return media_filepath
##
##    def generate_full_image_filepath(images_dir, board_name, filename):# WIP
##        # boards/<boardName>/<thumb or image>/<char 0-3>/<char 4-5>/<full image name>
##        board_dir = os.path.join(images_dir, board_name,  'image')
##        full_image_filepath = generate_image_filepath(board_dir, filename)
##        return full_image_filepath
##
##    def generate_thumbnail_image_filepath(images_dir, board_name, filename):# WIP
##        # boards/<boardName>/<thumb or image>/<char 0-3>/<char 4-5>/<full image name>
##        board_dir = os.path.join(images_dir, board_name, 'thumb')
##        full_image_filepath = generate_image_filepath(board_dir, filename)
##        return full_image_filepath
##
##    def attempt_to_export_csv_row_dict(self,row):# WIP
##        """
##        Given a dict where columname:value, using Foolfuuka columns,
##        Check whether to export it and then export/not as approriate
##        """
##        # Check if hash is in DB
##        md5_full = row['media_hash']
##        existing_row = self.check_for_image(md5_full)
##        if existing_row:
##            # Do not export
##            logging.debug('Not exporting this image')
##            return
##        else:
##            # Export
##            logging.debug('Exporting this image')
##            # Add files to zip
##        return
##
##    def export_csv_rows(self, rows):
##        row_counter = 0
##        for row in rows:
##            row_counter += 0
##            attempt_to_export_csv_row_dict(self,row)
##        return
##
##    def export_from_csv_file(self, csv_filepath):# WIP
##        # Validate input values, such as paths
##        # Open zip file
##        # Add CSV file to zip
##        # Open CSV file
##        # Process rows
##        return
##
##
##
##class DBExporterZipper():# WIP
##    """
##    Export directly from a Foolfuuka DB into a zip file
##    Zip file contains:
##        images from selected range
##        image table row data from selected range
##        metadata JSON containing run parameters
##    """
##    # Class instance variables
##    db_class = None
##    db_session = None
##    low_value = None
##    high_value = None
##    most_recent_row_primary_key = None
##    zip_filepath = None
##    images_dir = None
##    metadata_filepath = None
##    row_counter = None
##    file_counter = None
##
##    def __init__(self):# WIP
##        return
##
##    def export_range(self, low_value, high_value, images_dir, zip_filepath):# WIP
##        """Export a range of images"""
##        # Record run parameters temporarily
##        self.create_metadata_json()
##        # Prepare zip file
##        # Run a SELECT query for the range
##        # Iterate over results
##        # Record run parameters, overwriting old file
##        return
##
##    def export_rows(self, rows):# WIP
##        # Dump all row data to file
##        # Iterate over results and zip files
##        self.row_counter = 0
##        for row in rows:
##            self.row_counter += 1
##            self.export_row(row)
##            pass
##        return
##
##    def export_row(self, row):# WIP
##        # Zip row files
##        # media
##        self.file_counter += 1
##        # preview_op
##        self.file_counter += 1
##        # preview_reply
##        self.file_counter += 1
##        return
##
##    def create_metadata_json(self, short=False, metadata_filepath):# WIP
##        """Dump class values to JSON to record what went on in a run
##        if short is True, only include things relevant to the start of the run"""
##        logging.debug('metadata_filepath = {0!r}'.format(metadata_filepath))
##        logging.debug('short = {0!r}'.format(short))
##        # Prepare the data to export
##        metadata_dict = {}
##        # Add short/common values
##        metadata_dict['metadata_file_format_version'] = 0,# Update this every time this format changes. (There should be a unique format version number for each format that ever actually gets used)
##        metadata_dict['run_finish_time'] = None# TODO: Unix time int should go here, generated when run starts.
##        metadata_dict['metadata_dump_time'] = None# TODO: Unix time int should go here, generated when run starts.
##        metadata_dict['low_value'] = None# TODO: low value of export range
##        metadata_dict['high_value'] = None# TODO: High value of export range
##        if not short:
##            # Add long form values
##            metadata_dict['run_finish_time'] = None# TODO: Unix time int should go here, generated when run ends.
##            metadata_dict['number_of_files_exported'] = None# TODO:
##            metadata_dict['number_of_rows_exported'] = None# TODO:
##            pass
##        logging.debug('metadata_dict = {0!r}'.format(metadata_dict))
##        # Convert to JSON
##        metadata_json = json.dumps(metadata_dict)
##        # Write to file
##        metadata_dir = os.path.dirname(metadata_filepatn)
##        if (len(metadata_dir) != 0):
##            if not os.path.exists(metadata_filepath):
##                os.mkdirs()
##        with open(metadata_filepath, 'wb') as meta_f:
##            meta_f.write(metadata_json)
##        logging.debug('Finished exporting metadata.')
##        return





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











logging.warning('This stuff is all after a normal script would end now, just saiyan...')


logging.warning('Imports should really go at the beginning of the file.')
# https://www.blog.pythonlibrary.org/2010/09/10/sqlalchemy-connecting-to-pre-existing-databases/











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
# ===== Do things with the DB =====

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




range_images_q = session.query(Image)
logging.info('len(range_images_q.all()) = {0!r}'.format(len(range_images_q.all())))# PERFORMANCE This might cause slowdowns, disable outside testing

# Add one image
new_image = Image(
    board_name='mlp',
    origin_media_id=16,
    md5b64='qaM5T9h08awvwz86eLI+7w==',
    time_uploaded = 1536638719722,
    filename_full='1536638719722.webm',
    filename_thumb_op='1536638719722s.jpg',
    filename_thumb_reply='1536638719722s.jpg',
)

##session.add(new_image)
##session.commit()


try_to_add_image(session=session, image_to_add=new_image)

# Import data from CSV


range_images_q = session.query(Image)
logging.info('len(range_images_q.all()) = {0!r}'.format(len(range_images_q.all())))# PERFORMANCE This might cause slowdowns, disable outside testing

