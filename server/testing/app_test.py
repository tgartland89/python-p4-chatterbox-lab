from datetime import datetime
import unittest

from flask import Flask
from models import db, Message

from app import app

class TestApp(unittest.TestCase):
    '''Flask application in app.py'''

    @classmethod
    def setUpClass(cls):
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def setUp(self):
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )

            db.session.add(hello_from_liza)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            hello_from_liza = Message.query.filter_by(body="Hello 👋").first()

            db.session.delete(hello_from_liza)
            db.session.commit()

    def test_has_correct_columns(self):
        '''has columns for message body, username, and creation time.'''
        with app.app_context():
            hello_from_liza = Message.query.filter_by(
                body="Hello 👋",
                username="Liza"
            ).first()

            self.assertIsNotNone(hello_from_liza)
            self.assertEqual(hello_from_liza.body, "Hello 👋")
            self.assertEqual(hello_from_liza.username, "Liza")
            self.assertIsInstance(hello_from_liza.created_at, datetime)

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        '''returns a list of JSON objects for all messages in the database.'''
        with app.app_context():
            response = app.test_client().get('/messages')
            records = Message.query.all()

            for message in response.json:
                self.assertIn(message['id'], [record.id for record in records])
                self.assertIn(message['body'], [record.body for record in records])

    def test_creates_new_message_in_the_database(self):
        '''creates a new message in the database.'''
        with app.app_context():
            app.test_client().post(
                '/messages',
                json={
                    "body": "Hello 👋",
                    "username": "Liza",
                }
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            self.assertIsNotNone(h)

    def test_returns_data_for_newly_created_message_as_json(self):
        '''returns data for the newly created message as JSON.'''
        with app.app_context():
            response = app.test_client().post(
                '/messages',
                json={
                    "body": "Hello 👋",
                    "username": "Liza",
                }
            )

            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.json["body"], "Hello 👋")
            self.assertEqual(response.json["username"], "Liza")

            h = Message.query.filter_by(body="Hello 👋").first()
            self.assertIsNotNone(h)

    def test_updates_body_of_message_in_database(self):
        '''updates the body of a message in the database.'''
        with app.app_context():
            m = Message.query.first()
            id = m.id
            body = m.body

            app.test_client().patch(
                f'/messages/{id}',
                json={
                    "body": "Goodbye 👋",
                }
            )

            g = Message.query.filter_by(body="Goodbye 👋").first()
            self.assertIsNotNone(g)

            g.body = body
            db.session.commit()

    def test_returns_data_for_updated_message_as_json(self):
        '''returns data for the updated message as JSON.'''
        with app.app_context():
            m = Message.query.first()
            id = m.id
            body = m.body

            response = app.test_client().patch(
                f'/messages/{id}',
                json={
                    "body": "Goodbye 👋",
                }
            )

            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.json["body"], "Goodbye 👋")

            g = Message.query.filter_by(body="Goodbye 👋").first()
            self.assertIsNotNone(g)

            g.body = body
            db.session.commit()

    def test_deletes_message_from_database(self):
        '''deletes the message from the database.'''
        with app.app_context():
            new_message = Message(
                body="New message",
                username="Test User"
            )
            db.session.add(new_message)
            db.session.commit()

            app.test_client().delete(
                f'/messages/{new_message.id}'
            )

            h = Message.query.filter_by(body="New message").first()
            self.assertIsNone(h)


if __name__ == '__main__':
    unittest.main()
