from __future__ import division
from ReferenceResolver import app, db
from ReferenceResolver.Common.DataBase import init_db
from flask import json
import os
import argparse
import pandas as pd
import tempfile
import urllib
from log import setup_logging, logging
setup_logging()

def set_up(app, db):
    """
    Set-up a temporary database to be used by the unit tests.

    Parameters
    ----------
    app : flask application
    db : SQLAlchemy engine

    Returns
    -------
    client_db_fd : file
        Database file descriptor.
    client_db_filename : string
        Database filename.
    client_app : flask client app
    """
    client_db_fd, client_db_filename = tempfile.mkstemp(suffix=".db")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+client_db_filename
    app.config['TESTING'] = True
    client_app = app.test_client()
    init_db(db)
    return client_db_fd, client_db_filename, client_app

def tear_down(client_db_fd, client_db_filename):
    """
    Remove the temporary database used by the unit tests.

    Parameters
    ----------
    client_db_fd : file
        Database file descriptor.
    client_db_filename : string
        Database filename.
    """
    os.close(client_db_fd)
    os.unlink(client_db_filename)

def analyse_sample(client_app, sample_filename, output_filename):
    """
    Resolve the sample of refstrings contained in a file.

    Parameters
    ----------
    client_app : flask app
    sample_filename : string
        Input filename with bibcodes and refstrings.
    output_filename : string
        Output filename with resolved bibcodes.
    """
    refsample = pd.read_fwf(sample_filename, widths=[19,10000], names=['bibcode', 'refstring'])
    refsample['suggested_bibcode'] = " "*19
    refsample['status'] = " "*100
    n_total = len(refsample)
    for idx, row in refsample.iterrows():
        try:
            # Do not accept '/' in refstring or they will be interpret as part of the URL (even if properly encoded with quote)
            response = client_app.get(urllib.quote("/resolve/"+row['refstring'].replace("/", ":")))
            json_response = json.loads(response.get_data())
        except Exception, e:
            row['suggested_bibcode'] = None
            row['status'] = "Exception error: {0}".format(str(e))
        else:
            row['suggested_bibcode'] = json_response['bibcode']
            row['status'] = json_response['status']
        print "[{}/{}] Processed '{}'".format(idx, n_total, row['refstring'])
        # Write after every analysis to make sure we do not lose results in case of failure
        # TODO: Optimise this approach
        refsample.iloc[:idx+1][['bibcode', 'suggested_bibcode', 'status']].to_csv(output_filename, sep="\t", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a sample of reference strings and bibcodes")
    parser.add_argument('sample_filename', action='store', help='Filename with the sample of reference strings and bibcodes (e.g., ReferenceResolver/Tests/input/refsample.txt)')
    parser.add_argument('output_filename', action='store', help='Filename where results will be written (e.g., ReferenceResolver/Tests/output/refsample_analysed.txt)')
    args = parser.parse_args()
    #
    client_db_fd, client_db_filename, client_app = set_up(app, db)
    analyse_sample(client_app, args.sample_filename, args.output_filename)
    tear_down(client_db_fd, client_db_filename)
