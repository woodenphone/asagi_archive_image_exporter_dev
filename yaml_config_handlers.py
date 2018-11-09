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
# Remote libraries
import yaml# https://pyyaml.org/wiki/PyYAMLDocumentation
# local
import common




##class YAMLConfig():
##    """Handle reading, writing, and creating YAML config files.
##    Generic useless superclass."""
##    # This is what we expect the YAML file to contain
##    confg_template = {
##    }
##    # Create empty vars
##    config_path = None
##
##    def __init__(self, config_path):
##        # Store argument value to class instance.
##        self.config_path = config_path
##        logging.debug('self.config_path = {0!r}'.format(self.config_path))
##        # Ensure config dir exists.
##        config_dir = os.path.dirname(config_path)
##        if len(config_dir) > 0:# Only try to make a dir if ther is a dir to make.
##            if not os.path.exists(config_dir):
##                os.makedirs(config_dir)
##        # Load/create config file
##        if os.path.exists(self.config_path):
##            # Load config file if it exists.
##            self.load()
##        else:
##            # Create an example config file if no file exists.
##            self.save()
##        # Ensure config looks valid.
##        self.validate()
##        return
##
##    def load(self):
##        """Load configuration from YAML file."""
##        logging.warning('This line should never run!')
##        return
##
##    def save(self):
##        """Save current configuration to YAML file."""
##        logging.warning('This line should never run!')
##        return
##
##    def create(self):
##        """Create a new blank YAML file."""
##        logging.warning('This line should never run!')
##        return
##
##    def validate(self):
##        """Validate current configuration values and crash if any value is invalid."""
##        logging.warning('This line should never run!')
##        return



class YAMLConfigStep1():
    """Handle reading, writing, and creating YAML config files.
    For step1_dump_img_table.py"""
    # This is what we expect the YAML file to contain
    confg_template = {
        'connection_string': '',
        'table_name': '',
        'csv_filepath': '',
        'lower_bound': None,
        'upper_bound': None
    }
    # Create empty vars
    config_path = None
    connection_string = ''
    table_name = ''
    csv_filepath = ''
    lower_bound = ''
    upper_bound = ''

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
        logging.debug('Reading config from self.config_path = {0!r}'.format(self.config_path))
        with open(self.config_path, 'rb') as load_f:
            config_data_in = yaml.safe_load(load_f)
        # Store values to class instance.
        logging.debug('Loading config data config_data_in = {0!r}'.format(config_data_in))
        self.connection_string = config_data_in['connection_string']
        self.table_name = config_data_in['table_name']
        self.csv_filepath = config_data_in['csv_filepath']
        self.lower_bound = config_data_in['lower_bound']
        self.upper_bound = config_data_in['upper_bound']
        return

    def save(self):
        """Save current configuration to YAML file."""
        logging.debug('Saving current configuration to self.config_path = {0!r}'.format(self.config_path))
        # Collect data together.
        config_data_out = {
            'connection_string': self.connection_string,
            'table_name': self.table_name,
            'csv_filepath': self.csv_filepath,
            'lower_bound': self.lower_bound,
            'upper_bound': self.upper_bound,
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



class YAMLConfigStep2():
    """Handle reading, writing, and creating YAML config files.
    For step2_zip.py"""
    # This is what we expect the YAML file to contain
    confg_template = {
        'csv_filepath': '',
        'images_dir': '',
        'zip_path': '',
        'board_name': '',
        'db_path': '',
    }
    # Create empty vars
    config_path = None
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
        logging.debug('Reading config from self.config_path = {0!r}'.format(self.config_path))
        with open(self.config_path, 'rb') as load_f:
            config_data_in = yaml.safe_load(load_f)
        # Store values to class instance.
        logging.debug('Loading config data config_data_in = {0!r}'.format(config_data_in))
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



class YAMLconfigRclone():# WIP
    """Class for YAML-based rclone script configuration"""
    # This is what we expect the YAML file to contain
    confg_template = {
        'csv_filepath': '',
        'images_dir': '',
        'zip_path': '',
        'board_name': '',
    }
    # Create empty vars
    config_path = None
    csv_filepath = ''
    images_dir = ''
    zip_path = ''
    board_name = ''

    def __init__(self, config_path):# WIP
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

    def load(self):# WIP
        """Load configuration from YAML file."""
        # Read the config from file.
        logging.debug('Reading config from self.config_path = {0!r}'.format(self.config_path))
        with open(self.config_path, 'rb') as load_f:
            config_data_in = yaml.safe_load(load_f)
        # Store values to class instance.
        logging.debug('Loading config data config_data_in = {0!r}'.format(config_data_in))
        self.csv_filepath = config_data_in['csv_filepath']
        self.images_dir = config_data_in['images_dir']
        self.zip_path = config_data_in['zip_path']
        self.board_name = config_data_in['board_name']
        return

    def save(self):# WIP
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

    def create(self):# WIP
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

    def validate(self):# WIP
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
    common.setup_logging(os.path.join("debug", "yaml_config_handlers.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception, e:
        logging.critical("Unhandled exception!")
        logging.exception(e)
    logging.info("Program finished.")
