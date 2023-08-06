import unittest
from ds4biz_format_parsers.utils.email_utils import get_email
import logging
from ds4biz_format_parsers.business.converters import Email2TextEmail

class Email2TextEmailTest(unittest.TestCase):
    
    def setUp(self):
        self.converter=Email2TextEmail(None)
        logging.basicConfig(level=logging.DEBUG)
        self.path= "/home/lorenzo/Scaricati/Sinistro su polizza 4___7 - 4___8.eml"
        self.email = get_email(self.path)
    
    def test_get_sender(self):
        sender = self.converter.get_sender(self.email)
        recipients = self.converter.get_recipients(self.email)
        logging.debug(sender)
        logging.debug(recipients)
        
    def test_get_body(self):
        body_parts, attachments = self.converter.get_parts(self.email)
        
        for b in body_parts:
            logging.debug(body_parts)
            
        for k,v in attachments.items():
            print(k,v)
        
