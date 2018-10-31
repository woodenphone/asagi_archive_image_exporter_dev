#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     31-10-2018
# Copyright:   (c) User 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# StdLib
import os
import logging
import argparse
# Remote libraries
# local
import common



##class CommandLineConfig():
##    """Accept configuration from command-line arguments.
##    Generic useless superclass."""
##    # Create empty vars
##
##    def __init__(self):
##        self.load()
##        self.validate()
##        return
##
##    def load(self):
##        """Read and store the command line arguments"""
##        return
##
##    def validate(self):
##        """Validate current configuration values and crash if any value is invalid."""
##        return


class CommandLineConfigStep1():
    """Accept configuration from command-line arguments.
    For step1_dump_img_table.py"""
    # Create empty vars
    connection_string = ''
    table_name = ''
    csv_filepath = ''
    lower_bound = ''
    upper_bound = ''

    def load(self):
        """Read and store the command line arguments"""
        # Read args
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser()
        parser.add_argument('--connection_string', help='connection_string see https://docs.sqlalchemy.org/en/latest/core/engines.html',# https://docs.sqlalchemy.org/en/latest/core/engines.html
                        type=str)
        parser.add_argument('--table_name', help='table_name, mandatory.',
                        type=str)
        parser.add_argument('--csv_filepath', help='csv_filepath, mandatory.',
                        type=str)
        parser.add_argument('--lower_bound', help='lower_bound, defaults to None',
                        type=str, default=None)
        parser.add_argument('--upper_bound', help='upper_bound, defaults to None',
                        type=str, default=None)
        args = parser.parse_args()
        logging.debug('args: {0!r}'.format(args))# Record CLI arguments
        # Store to class instance
        self.connection_string = args.connection_string
        self.table_name = args.table_name
        self.csv_filepath = args.csv_filepath
        self.lower_bound = args.lower_bound
        self.upper_bound = args.upper_bound
        return

    def validate(self):
        """Validate current configuration values and crash if any value is invalid."""
        # self.connection_string
        assert(type(self.connection_string) in [str, unicode])
        assert(len(self.connection_string) != 0)
        # self.table_name
        assert(type(self.table_name) in [str, unicode])
        assert(len(self.table_name) != 0)
        # self.csv_filepath
        assert(type(self.csv_filepath) in [str, unicode])
        assert(len(self.csv_filepath) != 0)
        # self.lower_bound
        assert(type(self.lower_bound) in [str, unicode, type(None)])
        assert(len(self.lower_bound) != 0)
        # self.upper_bound
        assert(type(self.upper_bound) in [str, unicode, type(None)])
        assert(len(self.upper_bound) != 0)
        return



class CommandLineConfigStep2():
    """Accept configuration from command-line arguments.
    For step2_zip.py"""
    # Create empty vars
    csv_filepath = ''
    images_dir = ''
    zip_path = ''
    board_name = ''

    def load(self):
        """Read and store the command line arguments"""
        # Read args
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
        # Store to class instance
        self.csv_filepath = args.csv_filepath
        self.images_dir = args.images_dir
        self.zip_path = args.zip_path
        self.board_name = args.board_name
        return

    def validate(self):
        """Validate current configuration values and crash if any value is invalid."""
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





def main():
    pass

if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "cli_config_handlers.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception, e:
        logging.critical("Unhandled exception!")
        logging.exception(e)
    logging.info("Program finished.")

