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
import yaml# https://pyyaml.org/wiki/PyYAMLDocumentation
# local




class YAMLConfig():
    """Handle reading, writing, and creating YAML config files.
    Generic useless superclass."""
    # This is what we expect the YAML file to contain
    confg_template = {
        'csv_filepath': '',
        'images_dir': '',
        'zip_path': '',
        'board_name': '',
    }
    # Create empty vars
    self.config_path = None
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
        """Load configuration from YAML file."""
        return

    def save(self):
        """Save current configuration to YAML file."""
        return

    def create(self):
        """Create a new blank YAML file."""
        return

    def validate(self):
        """Validate current configuration values and crash if any value is invalid."""
        return



class YAMLConfig_Zip():
    """Handle reading, writing, and creating YAML config files.
    For step2_zip.py"""
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
        logging.debug('self.config_path = {0!r}'.format(self.config_path))
        # Ensure config dir exists.
        config_dir = os.path.dirname(config_path)
        if len(config_dir) > 0:# Only try to make a dir if ther is a dir to make.
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
        # Load/create config file
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
        """Load configuration from YAML file."""
        # Read the config from file.
        with open(self.config_path, 'rb') as load_f:
            config_data_in = yaml.safe_load(load_f)
        logging.debug('Loading config_data_in = {0!r}'.format(config_data_in))
        # Store values to class instance.
        self.csv_filepath = config_data_in['csv_filepath']
        self.images_dir = config_data_in['images_dir']
        self.zip_path = config_data_in['zip_path']
        self.board_name = config_data_in['board_name']
        return

    def save(self):
        """Save current configuration to YAML file."""
        logging.debug('Saving current configuration to self.config_path = {0!r}'.format(self.config_path))
        # Collect data together.
        config_data_out = {
            'csv_filepath': self.csv_filepath,
            'images_dir': self.images_dir,
            'zip_path': self.zip_path,
            'board_name': self.board_name,
        }
        logging.debug('Saving config_data_out = {0!r}'.format(config_data_out))
        # Write data to file.
        with open(self.config_path, 'wb') as save_f:
            yaml.dump(
                data=config_data_out,
                stream=save_f,
                explicit_start=True,# Begin with '---'
                explicit_end=True,# End with '...'
                default_flow_style=False# Output as multiple lines
            )
        return

    def create(self):
        """Create a new blank YAML file."""
        # Write a generic example config file.
        logging.debug('Creating example config file at self.config_path = {0!r}'.format(self.config_path))
        with open(self.config_path, 'wb') as create_f:
            yaml.dump(
                data=confg_template,
                stream=create_f,
                explicit_start=True,# Begin with '---'
                explicit_end=True,# End with '...'
                default_flow_style=False# Output as multiple lines
            )
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



class CommandLineConfig():
    """Accept configuration from command-line arguments.
    Generic useless superclass."""
    # Create empty vars

    def __init__(self):
        self.load()
        self.validate()
        return

    def load(self):
        return

    def validate(self):
        """Validate current configuration values and crash if any value is invalid."""
        return



class CommandLineConfig_Zip():
    """Accept configuration from command-line arguments.
    For step2_zip.py"""
    # Create empty vars
    csv_filepath = ''
    images_dir = ''
    zip_path = ''
    board_name = ''

    def __init__(self):
        self.load()
        self.validate()
        return

    def load(self):
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
    setup_logging(os.path.join("debug", "config_handlers.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception, e:
        logging.critical("Unhandled exception!")
        logging.exception(e)
    logging.info("Program finished.")
