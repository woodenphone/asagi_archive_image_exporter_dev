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
# Remote libraries
##import sqlite3
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
# local
import common# Things like logging setup
import yaml_config_handlers
import cli_config_handlers



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
