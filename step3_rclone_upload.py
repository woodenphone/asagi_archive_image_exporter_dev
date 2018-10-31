#-------------------------------------------------------------------------------
# Name:        step3_rclone_upload
# Purpose:
#
# Author:      User
#
# Created:     28-10-2018
# Copyright:   (c) User 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# StdLib
import logging
import argparse
import os
import csv
import subprocess
# Remote libraries
# local
import common# Things like logging setup
import yaml_config_handlers
import cli_config_handlers



class RcloneRunner():
    """An attempt at implimenting this new rclone functionality as a class,
    because antonizoon wanted more classiness."""
    # Initialise class variables
    command = None
    command_result = None
    sourcepath = None
    destpath = None
    temp_dir = 'temp/'
    rclone_log_path = os.path.join(temp_dir, 'rclone_log.txt')

    def __init__(self, sourcepath, destpath):
        self.sourcepath, self.destpath = sourcepath, destpath
        self.prepare_command()
        return

    def prepare_command(self):
        """Prepare command and arguments to run rclone"""
        assert(type(self.sourcepath) in [str, unicode])# Should be text
        assert(type(self.destpath) in [str, unicode])# Should be text
        assert(type(self.log_file_path) in [str, unicode])# Should be text
        assert(len(log_file_path) > 0)# Should be positive
        cmd = []
        # Program to run
        cmd.append('rclone')
        # Mode
        cmd.append('copy')
        # Source and destination
        cmd.append('source:"{sp}"'.format(sp=self.sourcepath))
        cmd.append('destpath:"{dp}"'.format(dp=self.destpath))
        # Use a log file so validation is possible
        command.append('--log-file')
        command.append(log_file_path)
        # Store finished command
        self.command = cmd
        return

    def run(self):
        """Run the prepared command to run rclone."""
        # Execute command
        logging.debug('Running command = {0!r}'.format(command))
        self.command_result = subprocess.call(command)
        logging.debug('command_result = {0!r}'.format(command_result))
        # Verify successful execution
        return self.command_result

    def analyse_log(self):
        with open(self.rclone_log_path, 'ru') as log_f:
            for log_line in log_f:
                # Do stuff with the line
                pass
        return



def simple_rclone_copy(sourcepath, destpath):
    """"""
    logging.debug('upload_using_rclone() locals() = {0!r}'.format(locals()))# Record arguments.
    # https://rclone.org/commands/rclone_copy/
    # https://rclone.org/commands/rclone_sync/
    log_file_path = os.path.join('temp','rclone_log.txt')
    # Generate command
    command = []
    command.append('rclone')
    command.append('copy')
    command.append('source:"{sp}"'.format(sp=sourcepath))
    command.append('destpath:"{dp}"'.format(dp=destpath))

    command.append('--log-file')
    command.append(log_file_path)

    # Run command
    logging.debug('Running command = {0!r}'.format(command))
    result = subprocess.call(command)
    logging.debug('result = {0!r}'.format(result))

    # Confirm command worked
    if result != 0:
        # Command failed
        pass
    else:
        # Command succeeded
        pass

    return



# For IA we use this:
# ia upload desu-img-2018 /path/to/folder

def dev():

    # We want to run commands like this:
    # rclone copy /path/to/folder desubackup:20181031
    simple_rclone_copy(
        sourcepath='',
        destpath=''
    )
    return


def main():
    dev()
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
