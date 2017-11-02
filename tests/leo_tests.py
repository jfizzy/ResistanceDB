import unittest
from . import config

class LeoTestCase(unittest.TestCase):

    def test_config_parsing(self):        
        self.cfg = config.Config('tests/test_files/.cfg')
        self.cfg.read_config()
        self.assertNotEqual(self.cfg.COMPOUNDSFILE, None)
