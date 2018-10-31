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
import yaml
# local
from common import *# Things like logging setup






def add_to_zip(zip_obj, filepath, internal_path):
    """Return whether file was added to zip"""
    try:
##        logging.debug('Zipping {0!r} as {1!r}'.format(filepath, internal_path))# PERFORMANCE This might cause slowdowns, disable outside testing
        zip_obj.write(filepath, internal_path)
        return True
    except OSError, err:
        logging.error(err)
    return False


def generate_image_filepath(board_dir, filename):
    # Expects filename to look like: '1536631035276.webm'
    # Outputs: 'BASE/153/6/1536631035276.webm'
    # boards/<boardName>/<thumb or image>/<char 0-3>/<char 4-5>/<full image name>
    # base/image/1536/63/1536631035276.webm
    assert(len(filename) > 4)# We can't generate a path is this is lower, and the value is based on unix time so should always be over 1,000,000
    media_filepath = os.path.join(board_dir, filename[0:4], filename[4:6], filename)# string positions 0,1,2,3/4,5/filename
    return media_filepath


def generate_full_image_filepath(images_dir, board_name, filename):
    # boards/<boardName>/<thumb or image>/<char 0-3>/<char 4-5>/<full image name>
    board_dir = os.path.join(images_dir, board_name,  'image')
    full_image_filepath = generate_image_filepath(board_dir, filename)
    return full_image_filepath


def generate_thumbnail_image_filepath(images_dir, board_name, filename):
    # boards/<boardName>/<thumb or image>/<char 0-3>/<char 4-5>/<full image name>
    board_dir = os.path.join(images_dir, board_name, 'thumb')
    full_image_filepath = generate_image_filepath(board_dir, filename)
    return full_image_filepath


def zip_from_csv(csv_filepath, images_dir, zip_path, board_name):
    """Attempt to zip all images from the CSV file"""
    logging.debug('zip_from_csv() locals() = {0!r}'.format(locals()))# Record arguments
    logging.info('Zipping files in {0} to {1}'.format(csv_filepath, zip_path))

    # Error checking before any work is done
    if not (os.path.exists(csv_filepath)):# We can't do anything if this is not present.
        logging.error('CSV file does not exist, cannot export! csv_filepath = {0!r}'.format(csv_filepath))
        raise ValueError()
    if not (os.path.exists(images_dir)):# We can't do anything if this is not present.
        logging.error('Image dir does not exist, cannot export! images_dir = {0!r}'.format(images_dir))
        raise ValueError()

    # Ensure output dir exists
    output_dir = os.path.dirname(zip_path)
    if not os.path.exists(output_dir):
        logging.debug('Creating output_dir = {0!r}'.format(output_dir))
        os.makedirs(output_dir)
        assert(os.path.exists(output_dir))# the dir should now exist

    file_counter = 0# Total number of files attempted.
    failed_file_counter = 0# Total number of files that had a failure in some way.
    success_file_counter = 0# Total number of files that were successfully added to zip.
    row_counter = 0
    with zipfile.ZipFile(zip_path, 'w') as myzip:
        # First, add the CSV to the zip
        add_to_zip(
            zip_obj=myzip,
            filepath=os.path.join(csv_filepath),
            internal_path=os.path.basename(csv_filepath)
        )

        # Add images from each row in the CSV file
        with open(csv_filepath, 'rb', ) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_ALL, lineterminator='\n')
            for row in reader:
                row_counter += 1
                if (row_counter % 100 == 0):
                    logging.info('Processed {0} rows.'.format(row_counter))
                # Add media to zip
                if row['media']:
                    media_success = add_to_zip(
                        zip_obj=myzip,
                        filepath=generate_full_image_filepath(# Filesystem
                            images_dir=images_dir,
                            board_name=board_name,
                            filename=row['media']
                        ),
                        internal_path=generate_full_image_filepath(# Zip internal
                            images_dir='',
                            board_name=board_name,
                            filename=row['media']
                        )
                    )
                    if media_success:
                        success_file_counter += 1
                    else:
                        failed_file_counter += 1
                    file_counter += 1
                # Add preview_op to zip
                if row['preview_op']:
                    preview_op_success = add_to_zip(
                        zip_obj=myzip,
                        filepath=generate_thumbnail_image_filepath(# Filesystem
                            images_dir=images_dir,
                            board_name=board_name,
                            filename=row['preview_op']
                        ),
                        internal_path=generate_thumbnail_image_filepath(# Zip internal
                            images_dir='',
                            board_name=board_name,
                            filename=row['preview_op']
                        )
                    )
                    if preview_op_success:
                        success_file_counter += 1
                    else:
                        failed_file_counter += 1
                    file_counter += 1

                # Add preview_reply to zip
                if row['preview_reply']:
                    preview_reply_success = add_to_zip(
                        zip_obj=myzip,
                        filepath=generate_thumbnail_image_filepath(# Filesystem
                            images_dir=images_dir,
                            board_name=board_name,
                            filename=row['preview_reply']
                        ),
                        internal_path=generate_thumbnail_image_filepath(# Zip internal
                            images_dir='',
                            board_name=board_name,
                            filename=row['preview_reply']
                        )
                    )
                    if preview_reply_success:
                        success_file_counter += 1
                    else:
                        failed_file_counter += 1
                    file_counter += 1

    logging.debug('row_counter = {rc}'.format(rc=row_counter))
    logging.debug('file_counter = {tot}, success_file_counter = {suc}, failed_file_counter = {fail}'.format(
        tot=file_counter, suc=success_file_counter, fail=failed_file_counter
        ))

    assert(os.path.exists(zip_path))# The zip file should now exist.
    logging.info('Finished zipping files from {0} rows in {1} to {2}'.format(row_counter, csv_filepath, zip_path))
    return


def read_yaml(yaml_config_path):
    """Load a YAML config file"""
    #import yaml
    confg_template = {# This is what we expect the YAML file to contain
        'csv_filepath': '',
        'images_dir': '',
        'zip_path': '',
        'board_name': '',
    }

    if not os.path.exists(yaml_config_path):
        # Write a generic example config file
        logging.debug('Creating example config file at yaml_config_path = {0!r}'.format(yaml_config_path))
        with open(yaml_config_path, 'wb') as new_f:
            yaml.dump(confg_template, new_f)

    # Read the config from file
    with open(yaml_config_path, 'rb') as config_f:
        config_data = yaml.safe_load(config_f)
    logging.debug('config_data = {0!r}'.format(config_data))

    # Validate config file
    has_correct_keys = ( set(confg_template.keys()) == set(config_data.keys()) )
    logging.debug('has_correct_keys = {0!r}'.format(has_correct_keys))

    logging.info('exiting yaml()')
    return config_data



class YAMLConfig():
    """Handle reading, writing, and creating YAML config files"""
    # This is what we expect the YAML file to contain
    confg_template = {
        'csv_filepath': '',
        'images_dir': '',
        'zip_path': '',
        'board_name': '',
    }
    # Create empty vars
    csv_filepath = ''
    images_dir = ''
    zip_path = ''
    board_name = ''

    def __init__(self, config_path):
        # Store argument value to class instance.
        self.config_path = config_path
        # Ensure config dir exists.
        config_dir = os.path.dirname(config_path)
        if len(config_dir) > 0:# Only try to make a dir if ther is a dir to make.
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)

        if os.path.exists(self.config_path):
            # Load config file if it exists.
            self.load()
        else:
            # Create an example config file if no file exists.
            self.save()
        # Ensure config looks valid.
        self.validate()
        return

    def load(self):
        """Load configuration from YAML file"""
        # Read the config from file.
        with open(self.config_path, 'rb') as load_f:
            config_data = yaml.safe_load(load_f)
        logging.debug('Loading config_data = {0!r}'.format(config_data))
        # Store values to class instance.
        self.csv_filepath = config_data['csv_filepath']
        self.images_dir = config_data['images_dir']
        self.zip_path = config_data['zip_path']
        self.board_name = config_data['board_name']
        return

    def save(self):
        """Save current configuration to YAML file"""
        logging.debug('Saving current configuration to self.config_path = {0!r}'.format(self.config_path))
        # Collect data together.
        output_dict = {
            'csv_filepath': self.csv_filepath,
            'images_dir': self.images_dir,
            'zip_path': self.zip_path,
            'board_name': self.board_name,
        }
        # Write data to file.
        with open(self.config_path, 'wb') as save_f:
            yaml.dump(output_dict, save_f)
        return

    def create(self):
        """Create a new blank YAML file"""
        # Write a generic example config file.
        logging.debug('Creating example config file at self.config_path = {0!r}'.format(self.config_path))
        with open(self.config_path, 'wb') as create_f:
            yaml.dump(confg_template, create_f)
        return

    def validate(self):
        """Validate current configuration values and crash if any value is invalid"""
        # self.csv_filepath
        assert(type(self.csv_filepath) in [str, unicode])
        assert(len(self.csv_filepath) != 0)
        # self.images_dir
        assert(type(self.images_dir) in [str, unicode])
        assert(len(self.images_dir) != 0)
        # self.zip_path
        assert(type(self.zip_path) in [str, unicode])
        assert(len(self.zip_path) != 0)
        # self.board_name
        assert(type(self.board_name) in [str, unicode])
        assert(len(self.board_name) != 0)
        return




def cli():
    """Command line running"""
    # Handle command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_filepath', help='csv_filepath, mandatory.',
                    type=str)
    parser.add_argument('--images_dir', help='images_di, mandatory.r',
                    type=str)
    parser.add_argument('--zip_path', help='zip_path, mandatory.',
                    type=str)
    parser.add_argument('--board_name', help='board_name, mandatory.',
                    type=str)
    args = parser.parse_args()

    logging.debug('args: {0!r}'.format(args))# Record CLI arguments

    zip_from_csv(
        csv_filepath=args.csv_filepath,
        images_dir=args.images_dir,
        zip_path=args.zip_path,
        board_name=args.board_name
    )

    logging.info('exiting cli()')
    return


def dev():
    """For development/debugging in IDE/editor without CLI arguments"""
    logging.warning('running dev()')


##    config_data = read_yaml(yaml_config_path=os.path.join('config.yaml'))
    config_obj = YAMLConfig(config_path=os.path.join('config.yaml'))

    zip_from_csv(
        csv_filepath=config_obj.csv_filepath,
        images_dir=config_obj.images_dir,
        zip_path=config_obj.zip_path,
        board_name=config_obj.board_name,
    )
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







