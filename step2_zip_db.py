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
# Remote libraries
import yaml# https://pyyaml.org/wiki/PyYAMLDocumentation
# local
from common import *# Things like logging setup
import yaml_config_handlers
import minidb


def calculate_time_uploaded(filename_full):
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
    data_json = json.dumps(data)
    write_file(
        file_path=filepath,
        data=data_json
    )
    return


def dev():
    """For development/debugging in IDE/editor without CLI arguments"""
    logging.warning('running dev()')

    # Load configuration for run
##    config_obj = yaml_config_handlers.YAMLConfigStep2(config_path=os.path.join('config_step2.yaml'))
##    config_obj = CommandLineConfigStep2()
##    # Run
##    zip_from_csv(
##        csv_filepath=config_obj.csv_filepath,
##        images_dir=config_obj.images_dir,
##        zip_path=config_obj.zip_path,
##        board_name=config_obj.board_name,
##    )
##    import config

##    csv_filepath = config.CSV_FILEPATH
##    zip_path = config.ZIP_PATH
##    images_dir = '.'
##    board_name = config.BOARD_NAME
##    zip_from_csv(
##        csv_filepath=csv_filepath,
##        images_dir=images_dir,
##        zip_path=zip_path,
##        board_name=board_name,
##    )

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


# Setup DB stuff
logging.info('Beginning DB setup phase')
# We have a SQLite DB
db_filepath = os.path.join('temp', 's2z.sqlite')
# Connect to dump DB
db = minidb.MiniDB(db_filepath=db_filepath, echo_sql=False)
db.connect()
logging.info('Finished DB setup phase')


import_from_csv(db, csv_filepath, board_name, max_import_rows)


def import_from_csv(db, csv_filepath, board_name, max_import_rows):
    # Import parameters
    max_import_rows = 1000
    csv_filepath = os.path.join('data', 'mysql_gif_images.csv')
    assert(os.path.exists(csv_filepath))
    board_name = 'gif'
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



def add_to_zip(zip_obj, filepath, internal_path):
    """Return whether file was added to zip"""
    try:
##        logging.debug('Zipping {0!r} as {1!r}'.format(filepath, internal_path))# PERFORMANCE This might cause slowdowns, disable outside testing
        zip_obj.write(filepath, internal_path)
        return True
    except OSError, err:
        logging.error(err)
    return False


def dump_rows_to_csv(query, csv_filepath):
    logging.debug('Dumping exported rows to CSV')
    with open(csv_filepath, 'wb') as csvfile:
        outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_ALL, lineterminator='\n')
        # Write header
        header = Images.__table__.columns.keys()
        outcsv.writerow(header)
        # Write records
        for record in range_images_q.all():# Write only images in the specified range
            outrow = [getattr(record, c) for c in header ]
    ##        logging.debug('outrow = {0!r}'.format(outrow))# PERFORMANCE This might cause slowdowns, disable outside testing
            outcsv.writerow(outrow)
    assert(os.path.exists(csv_filepath))# Be sure an output file was created.
    return



def export_to_zip(db, zip_filepath, image_dir, run_name, board_name, temp_dir='temp', max_export_rows=1000, ):
    """
    zip_filepath: Where on the disk the zip file will end up.
    image_dir: Path to the Foolfuuka installation's images dir.
    run_name: What we're calling this run and naming its files.
    temp_dir: Where we can store things while we're working.
    max_export_rows: How many should we dump at once (Maximum?).
    """
    logging.debug('export_to_zip() locals()={0!r}'.format(locals()))# Record arguments.
    # Export
    # Build filenames & filepaths
    csv_filename = '{0}.csv'.format(run_name)
    csv_filepath = os.path.join(temp_dir, csv_filename)# Location of CSV file, goes into temp dir and ends up in the zip
    zip_filename = '{0}.zip'.format(run_name)
    temp_zip_filepath = os.path.join(temp_dir, zip_filename)
    temp_metadata_filepath = os.path.join(temp_dir, '{0}.json'.format(run_name))# Location of JSON file, goes into temp dir and ends up in the zip
    # Display paths for debugging
    logging.debug('csv_filepath={0!r}'.format(csv_filepath))
    logging.debug('temp_zip_filepath={0!r}'.format(temp_zip_filepath))
    logging.debug('zip_filepath={0!r}'.format(zip_filepath))
    logging.debug('temp_metadata_filepath={0!r}'.format(temp_metadata_filepath))
    logging.info('Beginning ZIP export phase')
    # Prepare zip file
    with zipfile.ZipFile(zip_path, 'w') as myzip:
        # Select some rows to dump
        image_query = db.find_new(max_rows=max_export_rows)
        number_of_rows_to_export = image_query.count()
        logging.info('number_of_rows_to_export={0!r}'.format(number_of_rows_to_export))
        # Iterate over results to export
        export_row_counter = 0
        for image_row in image_query:
            export_row_counter += 1
            if ((export_row_counter % 100) == 0):
                logging.info('Exported {0} rows.'.format(export_row_counter))
            logging.debug('image_row={0!r}'.format(image_row))# DISABLE FOR PERFORMANCE

            # For each result to export:
            print('SIMULATE zipping result general')

            # Add filename_full (FF media) to zip
            print('SIMULATE zipping result filename_full (FF media)')
            media = image_row.filename_full

            # Add  filename_thumb_op (FF preview_op) to zip
            print('SIMULATE zipping result filename_thumb_op (FF preview_op)')
            filename_thumb_op = image_row.filename_thumb_op

            # Add filename_thumb_reply (FF preview_reply) to zip
            print('SIMULATE zipping result filename_thumb_reply (FF preview_reply)')
            filename_thumb_reply = image_row.filename_thumb_reply

            # Mark row as processed
            db.mark_done(image_row)
            continue

        # Dump exported rows to CSV and put that into the zip file
        # Dump rows to CSV file
        dump_rows_to_csv(image_query, csv_filepath)
        # Add CSV file to zip
        logging.debug('Adding media rows CSV file to zip')
        add_to_zip(
            zip_obj=myzip,
            filepath=os.path.join(csv_filepath),
            internal_path=os.path.basename(csv_filepath)# Root level in zip
        )
        # Store run metadata as JSON
        logging.debug('Saving info about this run to zip')
        run_info = {
            'format_version': 1,# Increment this each time something changes how this output is made.
            'zip_filepath': zip_filepath,
            'image_dir': image_dir,
            'run_name': run_name,
            'temp_dir': temp_dir,
            'max_export_rows': max_export_rows,
            'run_finish_time': get_current_unix_time_int(),
            'board_name': board_name,
##            '': None,
##            '': None,
        }
        save_to_json_file(data=run_info, filepath=temp_metadata_filepath)
        add_to_zip(
            zip_obj=myzip,
            filepath=temp_metadata_filepath,
            internal_path=os.path.basename(temp_metadata_filepath)# Root level in zip
        )
    logging.info('Finished adding things to zip file')
    # Commit changes to DB now that zip file is finished
    logging.info('Committing changes')
    db.commit()# Only commit after we've finished the job
    logging.info('Exported a total of {0} rows.'.format(export_row_counter))
    db.close()
    # Move zip file to output location
    shutil.move(src=temp_zip_filepath, dst=zip_filepath)
    logging.info('Finished ZIP export phase')
