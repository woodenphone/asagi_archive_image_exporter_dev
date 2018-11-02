#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     02-11-2018
# Copyright:   (c) User 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------











##class CSVExporterZipper():# WIP
##    """This may or may not go somewhere"""
##    def __init__(self):# WIP
##        return
##
##    def add_to_zip(zip_obj, filepath, internal_path):# WIP
##        """Return whether file was added to zip"""
##        try:
##    ##        logging.debug('Zipping {0!r} as {1!r}'.format(filepath, internal_path))# PERFORMANCE This might cause slowdowns, disable outside testing
##            zip_obj.write(filepath, internal_path)
##            return True
##        except OSError, err:
##            logging.error(err)
##        return False
##
##    def generate_image_filepath(board_dir, filename):# WIP
##        # Expects filename to look like: '1536631035276.webm'
##        # Outputs: 'BASE/153/6/1536631035276.webm'
##        # boards/<boardName>/<thumb or image>/<char 0-3>/<char 4-5>/<full image name>
##        # base/image/1536/63/1536631035276.webm
##        assert(len(filename) > 4)# We can't generate a path is this is lower, and the value is based on unix time so should always be over 1,000,000
##        media_filepath = os.path.join(board_dir, filename[0:4], filename[4:6], filename)# string positions 0,1,2,3/4,5/filename
##        return media_filepath
##
##    def generate_full_image_filepath(images_dir, board_name, filename):# WIP
##        # boards/<boardName>/<thumb or image>/<char 0-3>/<char 4-5>/<full image name>
##        board_dir = os.path.join(images_dir, board_name,  'image')
##        full_image_filepath = generate_image_filepath(board_dir, filename)
##        return full_image_filepath
##
##    def generate_thumbnail_image_filepath(images_dir, board_name, filename):# WIP
##        # boards/<boardName>/<thumb or image>/<char 0-3>/<char 4-5>/<full image name>
##        board_dir = os.path.join(images_dir, board_name, 'thumb')
##        full_image_filepath = generate_image_filepath(board_dir, filename)
##        return full_image_filepath
##
##    def attempt_to_export_csv_row_dict(self,row):# WIP
##        """
##        Given a dict where columname:value, using Foolfuuka columns,
##        Check whether to export it and then export/not as approriate
##        """
##        # Check if hash is in DB
##        md5_full = row['media_hash']
##        existing_row = self.check_for_image(md5_full)
##        if existing_row:
##            # Do not export
##            logging.debug('Not exporting this image')
##            return
##        else:
##            # Export
##            logging.debug('Exporting this image')
##            # Add files to zip
##        return
##
##    def export_csv_rows(self, rows):
##        row_counter = 0
##        for row in rows:
##            row_counter += 0
##            attempt_to_export_csv_row_dict(self,row)
##        return
##
##    def export_from_csv_file(self, csv_filepath):# WIP
##        # Validate input values, such as paths
##        # Open zip file
##        # Add CSV file to zip
##        # Open CSV file
##        # Process rows
##        return
##
##
##
##class DBExporterZipper():# WIP
##    """
##    Export directly from a Foolfuuka DB into a zip file
##    Zip file contains:
##        images from selected range
##        image table row data from selected range
##        metadata JSON containing run parameters
##    """
##    # Class instance variables
##    db_class = None
##    db_session = None
##    low_value = None
##    high_value = None
##    most_recent_row_primary_key = None
##    zip_filepath = None
##    images_dir = None
##    metadata_filepath = None
##    row_counter = None
##    file_counter = None
##
##    def __init__(self):# WIP
##        return
##
##    def export_range(self, low_value, high_value, images_dir, zip_filepath):# WIP
##        """Export a range of images"""
##        # Record run parameters temporarily
##        self.create_metadata_json()
##        # Prepare zip file
##        # Run a SELECT query for the range
##        # Iterate over results
##        # Record run parameters, overwriting old file
##        return
##
##    def export_rows(self, rows):# WIP
##        # Dump all row data to file
##        # Iterate over results and zip files
##        self.row_counter = 0
##        for row in rows:
##            self.row_counter += 1
##            self.export_row(row)
##            pass
##        return
##
##    def export_row(self, row):# WIP
##        # Zip row files
##        # media
##        self.file_counter += 1
##        # preview_op
##        self.file_counter += 1
##        # preview_reply
##        self.file_counter += 1
##        return
##
##    def create_metadata_json(self, short=False, metadata_filepath):# WIP
##        """Dump class values to JSON to record what went on in a run
##        if short is True, only include things relevant to the start of the run"""
##        logging.debug('metadata_filepath = {0!r}'.format(metadata_filepath))
##        logging.debug('short = {0!r}'.format(short))
##        # Prepare the data to export
##        metadata_dict = {}
##        # Add short/common values
##        metadata_dict['metadata_file_format_version'] = 0,# Update this every time this format changes. (There should be a unique format version number for each format that ever actually gets used)
##        metadata_dict['run_finish_time'] = None# TODO: Unix time int should go here, generated when run starts.
##        metadata_dict['metadata_dump_time'] = None# TODO: Unix time int should go here, generated when run starts.
##        metadata_dict['low_value'] = None# TODO: low value of export range
##        metadata_dict['high_value'] = None# TODO: High value of export range
##        if not short:
##            # Add long form values
##            metadata_dict['run_finish_time'] = None# TODO: Unix time int should go here, generated when run ends.
##            metadata_dict['number_of_files_exported'] = None# TODO:
##            metadata_dict['number_of_rows_exported'] = None# TODO:
##            pass
##        logging.debug('metadata_dict = {0!r}'.format(metadata_dict))
##        # Convert to JSON
##        metadata_json = json.dumps(metadata_dict)
##        # Write to file
##        metadata_dir = os.path.dirname(metadata_filepatn)
##        if (len(metadata_dir) != 0):
##            if not os.path.exists(metadata_filepath):
##                os.mkdirs()
##        with open(metadata_filepath, 'wb') as meta_f:
##            meta_f.write(metadata_json)
##        logging.debug('Finished exporting metadata.')
##        return


























def main():
    pass

if __name__ == '__main__':
    main()
