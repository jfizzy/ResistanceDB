import unittest
from mia import FileMover

class MiaTestCase(unittest.TestCase):
    def test_bad_dirs(self):
        try: 
            fm = FileMover.FileMover("asdjlka", "jlksdfakja", "asdkjlas")

            #shouldn't get here, bad directories
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)