import os
import src
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, src.app.config['DATABASE'] = tempfile.mkstemp()
        src.app.testing = True
        self.app = src.app.test_client()
        with src.app.app_context():
            src.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(src.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
