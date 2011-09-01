import unittest
import fudge
from ..auth import notifications


class NotificationTest(unittest.TestCase):
    """
    See if the notifications works

    """ 
    def setUp(self):
       pass 

    def test_base_props(self):
        """
        is there the method we want
        """
        self.assertTrue(hasattr(notifications, "send_new_user_notification"))


    @fudge.patch('smtplib.SMTP')
    def test_mailer(self, FakeSMTP):
        # Declare how the SMTP class should be used:
        (FakeSMTP.expects_call()
                 .returns_fake()
                 .expects('sendmail').with_arg_count(3)
                 .expects('quit'))

        notifications.send_new_user_notification("foo@bar.com", "abcdefghij")

