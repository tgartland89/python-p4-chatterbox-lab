from datetime import datetime
import unittest

from app import app
from models import db, Message

class TestMessage(unittest.TestCase):
    '''Message model in models.py'''

    @classmethod
    def setUpClass(cls):
        with app.app_context():
            db.create_all()

            m = Message.query.filter(
                Message.body == "Hello 👋"
            ).filter(Message.username == "Liza").first()

            if m:
                db.session.delete(m)

            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def test_has_correct_columns(self):
        '''has columns for message body, username, and creation time.'''
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )
            
            db.session.add(hello_from_liza)
            db.session.commit()

            self.assertEqual(hello_from_liza.body, "Hello 👋")
            self.assertEqual(hello_from_liza.username, "Liza")
            self.assertIsInstance(hello_from_liza.created_at, datetime)

            db.session.delete(hello_from_liza)
            db.session.commit()

if __name__ == '__main__':
    unittest.main()
