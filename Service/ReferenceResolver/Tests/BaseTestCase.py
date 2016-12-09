import os
from ReferenceResolver import app, db
from ReferenceResolver.Common.DataBase import init_db
import unittest
import tempfile

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        # Before every test
        pass

    def tearDown(self):
        # After every test
        pass

    #---------------------------------------------------------------------------

    @classmethod
    def setUpClass(cls):
        # Before instanciating the object
        cls.db_fd, cls.db_filename = tempfile.mkstemp(suffix=".db")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+cls.db_filename
        app.config['TESTING'] = True
        cls.app = app.test_client()
        init_db(db)

    @classmethod
    def tearDownClass(cls):
        # Before destroying the Object
        os.close(cls.db_fd)
        os.unlink(cls.db_filename)

    #---------------------------------------------------------------------------

