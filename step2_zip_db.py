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



# def import(db, csv_filepath, board_name, max_import_rows):
# Import parameters
max_import_rows = 1000
csv_filepath = os.path.join('data', 'mysql_gif_images.csv')
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
    logging.info('Attempting to import a CSV rows')
    import_row_counter = 0
    for csv_row in reader:
        import_row_counter += 1
        if ((import_row_counter % 100) == 0):
            logging.info('Imported {0} rows.'.format(import_row_counter))
            db.commit()
        logging.debug('csv_row={0!r}'.format(csv_row))
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


# def import(db, zip_filepath, image_dir):
# Export
# Export parameters
max_export_rows = 1000# How many should we dump at once (Maximum?)
logging.info('Beginning ZIP export phase')
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
        db.commit()
    logging.debug('image_row={0!r}'.format(image_row))
    # For each result to export:
    print('SIMULATE zipping result general')
    # Add filename_full (FF media) to zip
    media = image_row.filename_full
    filename_thumb_op = image_row.filename_thumb_op
    filename_thumb_reply = image_row.filename_thumb_reply
    print('SIMULATE zipping result filename_full (FF media)')
    # Add  filename_thumb_op (FF preview_op) to zip
    print('SIMULATE zipping result filename_thumb_op (FF preview_op)')
    # Add filename_thumb_reply (FF preview_reply) to zip
    print('SIMULATE zipping result filename_thumb_reply (FF preview_reply)')
    # Mark row as processed
    db.mark_done(image_row)
    continue
db.commit()
logging.info('Exported a total of {0} rows.'.format(export_row_counter))
db.close()
logging.info('Finished ZIP export phase')
