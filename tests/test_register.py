import unittest
import fudge

from .. import auth 


class RegisterTest(unittest.TestCase):
    """
    See if registering works
    """ 
    def setUp(self):
       pass 

    
    @fudge.patch('smtplib.SMTP')
    def test_register(self, FakeSMTP):
        """
        creates a new user
        """
        (FakeSMTP.expects_call()
                 .returns_fake()
                 .expects('sendmail').with_arg_count(3)
                 .expects('quit'))

        login = "testuser@aaa.com"
        password = "testpass"
        status = auth.register(login, password)
        self.assertTrue(status[0])
        self.assertEqual(status[1],"Success")

    def test_empty_email(self):
        """
        Email must be filled 
        """
        login = None
        password = "testpass"
        status = auth.register(login, password)
        self.assertFalse(status[0])
        self.assertEqual(status[1],"Empty email")


    def test_empty_password(self):
        """
        The password must be filled also
        """
        login = "testuser@aaa.com"
        password = None
        status = auth.register(login, password)
        self.assertFalse(status[0])
        self.assertEqual(status[1],"Empty password")

    def test_minimum_password_size(self):
        """
        Password must have at least 6 chars
        """
        login = "testuser@aaa.com"
        password = "testy"
        status = auth.register(login, password)
        self.assertFalse(status[0])
        self.assertEqual(status[1],"Invalid password")




    @fudge.patch('smtplib.SMTP')
    def test_register_email_uniqueness(self, FakeSMTP):
        """
        tries to create 2 users with same email
        """
        (FakeSMTP.expects_call()
                 .returns_fake()
                 .expects('sendmail').with_arg_count(3)
                 .expects('quit'))

        login = "testuser1@a.com"
        password = "testpass"
        status = auth.register(login, password)
        self.assertEqual(status[1],"Success")
        self.assertTrue(status[0])

        #should not create
        login = "testuser1@a.com"
        status = auth.register(login, password)
        self.assertFalse(status[0])
        self.assertNotEqual(status[1],"Success")
        self.assertEqual(status[1],"Fail")



    def test_register_invalid_emails(self):
        """
        Those are invalid emails
        """
        login = "testuser"
        password = "testpass"
        status = auth.register(login, password)
        self.assertFalse(status[0])
        self.assertEqual(status[1],"Invalid email")

        #need a domain and tld
        login = "testuser@"
        status = auth.register(login, password)
        self.assertFalse(status[0])

        #need a tld
        login = "testuser@a"
        status = auth.register(login, password)
        self.assertFalse(status[0])

        #need a domain
        login = "testuser@.aa"
        status = auth.register(login, password)
        self.assertFalse(status[0])
        
        # tld must be between 2 and 4 chars
        login = "testuser@a.a"
        status = auth.register(login, password)
        self.assertFalse(status[0])
        
        # tld must be between 2 and 4 chars
        login = "testuser@a.abcde"
        status = auth.register(login, password)
        self.assertFalse(status[0])

        #no spaces
        login = "te stuser@c.aa"
        status = auth.register(login, password)
        self.assertFalse(status[0])


    @fudge.patch('smtplib.SMTP')
    def test_register_valid_email(self, FakeSMTP):
        """
        valid emails
        """
        (FakeSMTP.expects_call()
                 .returns_fake()
                 .expects('sendmail').with_arg_count(3)
                 .expects('quit'))
        #simplest
        login = "a@a.cc"
        password = "testpass"
        status = auth.register(login, password)
        self.assertTrue(status[0])

        (FakeSMTP.expects_call()
                 .returns_fake()
                 .expects('sendmail').with_arg_count(3)
                 .expects('quit'))
        #most outrageous
        login = "test%._222user@a2-aa.ccc.bb"
        status = auth.register(login, password)
        self.assertTrue(status[0])


    def test_salt_size(self):
        """
        Get a salt, does it have the proper size
        """
        salt = auth.registering.get_salt()

        self.assertEqual(len(salt),32)

    def test_salt_uniqueness(self):
        """
        Although possible it is very unliquely that 2 salts are equal
        """
        salt1 = auth.registering.get_salt()
        salt2 = auth.registering.get_salt()

        self.assertNotEqual(salt1,salt2)

    def test_salt_letters(self):
        """
        Are all letters in the ASCII safe zone  
        """
        salt = auth.registering.get_salt()
        
        self.assertTrue(all([32 < ord(i) < 127 for i in salt]))


