#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     27-09-2018
# Copyright:   (c) User 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# StdLib
import logging
import argparse
import os
import csv
import zipfile
import shutil
import json
# Remote libraries
import yaml# https://pyyaml.org/wiki/PyYAMLDocumentation
# local
from common import *# Things like logging setup
import yaml_config_handlers
import minidb


def calculate_time_uploaded(filename_full):
    """Calculate the time a 4chan image was uploaded based on the filename of its foolfuuka 'media' column value"""
    assert(type(filename_full) in [str, unicode])
    assert(len(filename_full) > 0)
    the_digits = filename_full.split('.')[0]
    time_uploaded = int(the_digits)
    return time_uploaded


def get_current_unix_time_int():
    """Return the current UTC+0 unix time as an int"""
    # Get current time at UTC+0
    # Convert to time tuple
    # Convert time tuple to float seconds since epoch
    # Convert float to int
    current_unix_time_int = int(time.mktime(datetime.datetime.utcnow().timetuple()))
    return current_unix_time_int


def save_to_json_file(data, filepath):
    """Save some python data into JSON"""
    assert(type(filepath) in [str, unicode])
    assert(len(filepath) > 0)
    data_json = json.dumps(data)
    write_file(
        file_path=filepath,
        data=data_json
    )
    return


def add_to_zip(zip_obj, filepath, internal_path):
    """Return whether file was added to zip"""
    assert(type(filepath) in [str, unicode])
    assert(len(filepath) > 0)
    assert(type(internal_path) in [str, unicode])
    assert(len(internal_path) > 0)
    try:
##        logging.debug('Zipping {0!r} as {1!r}'.format(filepath, internal_path))# PERFORMANCE This might cause slowdowns, disable outside testing
        zip_obj.write(filepath, internal_path)
        return True
    except OSError, err:
        logging.error(err)
    return False


def add_column_to_zip(zip_obj, column_value, images_dir, board_name):
    filepath = make_img_path(root=images_dir, m_type='', filename=column_value)
    internal_path = make_img_path(root=images_dir, m_type='', filename=column_value)
    return add_to_zip(zip_obj, filepath, internal_path)


def add_row_to_zip(zip_obj, row, images_dir, board_name):
    """Add the files for one row to the supplied zip file."""
    column_names = ['media', 'preview_op', 'preview_reply']
    for column_name in column_names:
        column_value = row[column_value]
        add_column_to_zip(zip_obj, column_value, images_dir, board_name)
    return


def dump_rows_to_csv(query, csv_filepath):
    """Dump rows from our SQLite DB into CSV, so we can easily package them in our export zip"""
    assert(type(csv_filepath) in [str, unicode])
    assert(len(csv_filepath) > 0)
    logging.debug('Dumping exported rows to CSV')
    with open(csv_filepath, 'wb') as csvfile:
        outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_ALL, lineterminator='\n')
        # Write header
        header = minidb.Image.__table__.columns.keys()
        outcsv.writerow(header)
        # Write records
        for record in query.all():# Write only images in the specified range
            outrow = [getattr(record, c) for c in header ]
    ##        logging.debug('outrow = {0!r}'.format(outrow))# PERFORMANCE This might cause slowdowns, disable outside testing
            outcsv.writerow(outrow)
    assert(os.path.exists(csv_filepath))# Be sure an output file was created.
    return

def make_img_path(root, m_type, filename):
    """
    root: path of FoolFuuka images dir
    m_type: media_type, 'image' for fullsized media or 'thumb' for thumbnails (either op or reply)
    boards/<boardName>/<thumb or image>/<char 0-3>/<char 4-5>/<full image name>
    """
    assert(type(root) in [str, unicode])
    assert(m_type in ['image', 'thumb'])# Only supported modes
    assert(type(filename) in [str, unicode])
    assert(len(filename) > 4)# We can't generate a path is this is lower, and the value is based on unix time so should always be over 1,000,000
    filepath = os.path.join(images_dir, board_name,  m_type, filename[0:4], filename[4:6], filename)# string positions 0,1,2,3/4,5/filename
    return filepath

##def generate_image_filepath(board_dir, filename):
##    # Expects filename to look like: '1536631035276.webm'
##    # Outputs: 'BASE/153/6/1536631035276.webm'
##    # boards/<boardName>/<thumb or image>/<char 0-3>/<char 4-5>/<full image name>
##    # base/image/1536/63/1536631035276.webm
##    assert(len(filename) > 4)# We can't generate a path is this is lower, and the value is based on unix time so should always be over 1,000,000
##    media_filepath = os.path.join(board_dir, filename[0:4], filename[4:6], filename)# string positions 0,1,2,3/4,5/filename
##    return media_filepath
##
##
##def generate_full_image_filepath(images_dir, board_name, filename):
##    # boards/<boardName>/<thumb or image>/<char 0-3>/<char 4-5>/<full image name>
##    board_dir = os.path.join(images_dir, board_name,  'image')
##    full_image_filepath = generate_image_filepath(board_dir, filename)
##    return full_image_filepath
##
##
##def generate_thumbnail_image_filepath(images_dir, board_name, filename):
##    # boards/<boardName>/<thumb or image>/<char 0-3>/<char 4-5>/<full image name>
##    board_dir = os.path.join(images_dir, board_name, 'thumb')
##    full_image_filepath = generate_image_filepath(board_dir, filename)
##    return full_image_filepath


def import_from_csv(db, csv_filepath, board_name, max_import_rows=1000):
    """Read data from a CSV file into our SQLite DB"""
    assert(type(csv_filepath) in [str, unicode])
    assert(len(csv_filepath) > 0)
    assert(type(board_name) in [str, unicode])
    assert(len(board_name) > 0)
    assert(type(max_import_rows) is int)
    assert(max_import_rows > 0)
    #
    assert(os.path.exists(csv_filepath))
    # Import
    logging.info('Beginning CSV import phase')
    row_count_before_csv_import = db.count_total_rows()
    logging.info('Database curerntly has {0!r} rows'.format(row_count_before_csv_import))
    # Import posts from CSV to dump DB
    # Open CSV file
    with open(csv_filepath, 'rb', ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_ALL, lineterminator='\n')
        # Iterate over CSV rows
        logging.info('Attempting to import CSV rows')
        import_row_counter = 0
        for csv_row in reader:
            import_row_counter += 1
            if ((import_row_counter % 100) == 0):
                logging.info('Imported {0} rows.'.format(import_row_counter))
##                db.commit()
            logging.debug('csv_row={0!r}'.format(csv_row))# DISABLE FOR PERFORMANCE
            # For each result to import
            db.add_img(
                board_name=board_name,
                origin_media_id=csv_row['media_id'],
                md5_full=csv_row['media_hash'],
                time_uploaded=calculate_time_uploaded(filename_full=csv_row['media']),
                filename_full=csv_row['media'],
                filename_thumb_op=csv_row['preview_op'],
                filename_thumb_reply=csv_row['preview_reply']
            )
            continue
        db.commit()
        logging.info('Attempted to import a total of {0} rows.'.format(import_row_counter))
    logging.info('Finished CSV import phase')
    row_count_after_csv_import = db.count_total_rows()
    logging.info('Database curerntly has {0!r} rows'.format(row_count_after_csv_import))
    number_of_new_rows = (row_count_after_csv_import - row_count_before_csv_import)
    logging.info('Added {0!r} rows during CSV import phase'.format(number_of_new_rows))
    return


def export_to_zip(db, zip_filepath, images_dir, run_name, board_name, temp_dir='temp', max_export_rows=1000, ):
    """
    zip_filepath: Where on the disk the zip file will end up.
    images_dir: Path to the Foolfuuka installation's images dir.
    run_name: What we're calling this run and naming its files.
    temp_dir: Where we can store things while we're working.
    max_export_rows: How many should we dump at once (Maximum?).
    """
    logging.debug('export_to_zip() locals()={0!r}'.format(locals()))# Record arguments.
    # Validate arguments
    assert(type(zip_filepath) in [str, unicode])
    assert(len(zip_filepath) > 0)
    assert(type(images_dir) in [str, unicode])
    assert(len(images_dir) > 0)
    assert(type(run_name) in [str, unicode])
    assert(len(run_name) > 0)
    assert(type(board_name) in [str, unicode])
    assert(len(board_name) > 0)
    assert(type(temp_dir) in [str, unicode])
    assert(len(temp_dir) > 0)
    assert(type(max_export_rows) is int)
    assert(max_export_rows > 0)
    # Export
    # Build filenames & filepaths
    export_csv_filename = '{0}.csv'.format(run_name)
    export_csv_filepath = os.path.join(temp_dir, export_csv_filename)# Location of CSV file, goes into temp dir and ends up in the zip
    zip_filename = '{0}.zip'.format(run_name)
    temp_zip_filepath = os.path.join(temp_dir, zip_filename)
    temp_metadata_filepath = os.path.join(temp_dir, '{0}.json'.format(run_name))# Location of JSON file, goes into temp dir and ends up in the zip
    # Display paths for debugging
    logging.debug('export_csv_filepath={0!r}'.format(export_csv_filepath))
    logging.debug('temp_zip_filepath={0!r}'.format(temp_zip_filepath))
    logging.debug('zip_filepath={0!r}'.format(zip_filepath))
    logging.debug('temp_metadata_filepath={0!r}'.format(temp_metadata_filepath))
    logging.info('Beginning ZIP export phase')
    # Prepare zip file
    with zipfile.ZipFile(temp_zip_filepath, 'w') as myzip:
        # Select some rows to dump
        image_query = db.find_new(max_rows=max_export_rows)
        number_of_rows_to_export = image_query.count()
        logging.info('number_of_rows_to_export={0!r}'.format(number_of_rows_to_export))
        # Dump exported rows to CSV and put that into the zip file
        # Dump rows to CSV file
        dump_rows_to_csv(image_query, export_csv_filepath)
        # Add CSV file to zip
        logging.debug('Adding media rows CSV file to zip')
        add_to_zip(
            zip_obj=myzip,
            filepath=os.path.join(export_csv_filepath),
            internal_path=export_csv_filename# Root level in zip
        )
        # Iterate over results to export
        file_counter = 0# Total number of files attempted.
        failed_file_counter = 0# Total number of files that had a failure in some way.
        success_file_counter = 0# Total number of files that were successfully added to zip.
        export_row_counter = 0
        for image_row in image_query:
            export_row_counter += 1
            if ((export_row_counter % 100) == 0):
                logging.info('Exported {0} rows.'.format(export_row_counter))
            logging.debug('image_row={0!r}'.format(image_row))# DISABLE FOR PERFORMANCE

            # For each result to export:
            row_primary_key = image_row.origin_media_id
            print('SIMULATE zipping result general')

            # Add filename_full (FF media) to zip
            logging.info('SIMULATE zipping result filename_full (FF media)')
            filename_full = image_row.filename_full
            logging.debug('filename_full={0!r}')
            if filename_full:
                # Generate paths
                filepath_full = generate_full_image_filepath(# Filesystem
                    images_dir=images_dir,
                    board_name=board_name,
                    filename=filename_full
                )
                zip_filepath_full = generate_full_image_filepath(# Zip internal
                    images_dir='',
                    board_name=board_name,
                    filename=filename_full
                )
                # Put in zip file
                media_success = add_to_zip(
                    zip_obj=myzip,
                    filepath=filepath_full,
                    internal_path=zip_filepath_full,# Zip internal
                )
                if media_success:
                    success_file_counter += 1
                else:
                    failed_file_counter += 1
                file_counter += 1
            # Add filename_thumb_op (FF preview_op) to zip
            filename_thumb_op = image_row.filename_thumb_op
            logging.debug('filename_thumb_op={0!r}')

            if filename_thumb_op:
                # Generate paths
                thumb_op_filepath = generate_thumbnail_image_filepath(# Filesystem
                    images_dir=images_dir,
                    board_name=board_name,
                    filename=filename_thumb_op
                )
                thumb_op_zippath = generate_thumbnail_image_filepath(# Zip internal
                    images_dir='',
                    board_name=board_name,
                    filename=filename_thumb_op
                )
                # Put in zip file
                preview_op_success = add_to_zip(
                    zip_obj=myzip,
                    filepath=thumb_op_filepath,
                    internal_path=thumb_op_zippath,# Zip internal
                )
                if preview_op_success:
                    success_file_counter += 1
                else:
                    failed_file_counter += 1
                file_counter += 1
            # Add filename_thumb_reply (FF preview_reply) to zip
            filename_thumb_reply = image_row.filename_thumb_reply
            logging.debug('filename_thumb_reply={0!r}')
            if rowfilename_thumb_reply:
                # Generate paths
                thumb_reply_filepath = generate_thumbnail_image_filepath(# Filesystem
                    images_dir=images_dir,
                    board_name=board_name,
                    filename=filename_thumb_reply
                )
                thumb_reply_zippath = generate_thumbnail_image_filepath(# Zip internal
                    images_dir='',
                    board_name=board_name,
                    filename=filename_thumb_reply
                )
                # Put in zip file
                preview_reply_success = add_to_zip(
                    zip_obj=myzip,
                    filepath=thumb_reply_filepath,
                    internal_path=thumb_reply_zippath
                )
                if preview_reply_success:
                    success_file_counter += 1
                else:
                    failed_file_counter += 1
                file_counter += 1
            db.mark_done(image_row)# Mark row as processed
            continue
        # After zipping rows:
        logging.debug('row_counter = {rc}'.format(rc=row_counter))
        logging.debug('file_counter = {tot}, success_file_counter = {suc}, failed_file_counter = {fail}'.format(
            tot=file_counter, suc=success_file_counter, fail=failed_file_counter
            ))
        # Store run metadata as JSON
        logging.debug('Saving info about this run to zip')
        run_info = {
            'format_version': 1,# Increment this each time something changes how this output is made.
            'zip_filepath': zip_filepath,
            'images_dir': images_dir,
            'run_name': run_name,
            'temp_dir': temp_dir,
            'max_export_rows': max_export_rows,
            'run_finish_time': get_current_unix_time_int(),
            'board_name': board_name,
            'export_csv_filename': export_csv_filename,
##            '': None,
        }
        save_to_json_file(data=run_info, filepath=temp_metadata_filepath)
        add_to_zip(
            zip_obj=myzip,
            filepath=temp_metadata_filepath,
            internal_path=os.path.basename(temp_metadata_filepath)# Root level in zip
        )
    # After working with the zip file
    assert(os.path.exists(temp_zip_filepath))# If the zip doesn't exist at this point we're fucked.
    logging.info('Finished adding things to zip file')
    # Commit changes to DB now that zip file is finished
    logging.info('Committing changes')
    db.commit()# Only commit after we've finished the job
    logging.info('Exported a total of {0} rows.'.format(export_row_counter))
    db.close()
    # Move zip file to output location
    logging.debug('Moving files. temp_zip_filepath={0}, zip_filepath={1}')
    assert(os.path.exists(temp_zip_filepath))
    shutil.move(src=temp_zip_filepath, dst=zip_filepath)
    assert(os.path.exists(zip_filepath))
    assert(not os.path.exists(temp_zip_filepath))
    logging.info('Finished ZIP export phase')
    return


def connect_to_sqllite_db():
    # Setup DB stuff
    logging.info('Beginning DB setup phase')
    # We have a SQLite DB
    db_filepath = os.path.join('temp', 's2z.sqlite')
    # Connect to dump DB
    db = minidb.MiniDB(db_filepath=db_filepath, echo_sql=False)
    db.connect()
    logging.info('Finished DB setup phase')
    return db



def dev():
    """For development/debugging in IDE/editor without CLI arguments"""
    logging.warning('running dev()')
    db = connect_to_sqllite_db()
    # Settings for MySQL -> sqlite
    # Settings for MySQL -> csv


    # Settings for csv -> sqlite
    import_from_csv(
        db=db,
        csv_filepath=os.path.join('data', 'mysql_gif_images.csv'),
        board_name='gif',
        max_import_rows=10000
    )

    # Settings for sqlite -> zip
    run_name = ''
    export_to_zip(
        db=db,
        zip_filepath=os.path.join('temp', 'gif.zip'),
        image_dir=os.path.join('DUMMY_IMAGEDIR_VALUE'),# TODO FIXME
        run_name='DUMMY_RUNNAME_VALUE',# TODO FIXME
        board_name='gif',
        temp_dir='temp',
        max_export_rows=10000,
    )

    logging.warning('exiting dev()')
    return


def main():
##    cli()
    dev()
    return

if __name__ == '__main__':
    setup_logging(os.path.join("debug", "step2_zip.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception, e:
        logging.critical("Unhandled exception!")
        logging.exception(e)
    logging.info("Program finished.")






