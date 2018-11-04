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



# We have a SQLite DB
connection_string = ''

# How many should we dump at once (Maximum?)
max_rows = 1000

# Connect to dump DB

db = minidb.MiniDB(connection_string=connection_string)
db.connect()


# Select some rows to dump

results = db.find_new(max_rows=max_rows)
# Iterate over results to export
row_counter = 0
for image_result in image_results:
    row_counter += 1
    if ((row_counter % 100) == 0):
        logging.info('Processed {0} rows.'.format(row_counter))
        db.commit()
    # For each result:

    # Add media to zip

    # Add preview_op to zip

    # Add preview_reply to zip

    # Mark row as processed
    db.mark_done(row)
    db.commit()
    continue

db.commit()
logging.info('Processed a total of {0} rows.'.format(row_counter))

