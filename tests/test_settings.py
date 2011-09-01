import unittest

from ..auth import settings 


class SettingsTest(unittest.TestCase):
    
    def test_base_props(self):
        """
        See if the base properties are there
        """ 

        self.assertTrue(hasattr(settings, "PROJECT_PATH"))
        self.assertTrue(hasattr(settings, "DATABASE_PATH"))
        self.assertTrue(hasattr(settings, "EMAIL_HOST"))
        self.assertTrue(hasattr(settings, "EMAIL_FROM"))
