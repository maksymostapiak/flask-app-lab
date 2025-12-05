import unittest
from app import create_app, db
from app.posts.models import Post
from config import TestingConfig


class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        """Тестуємо створення поста через POST /posts/create"""

        with self.client.session_transaction() as sess:
            sess["user"] = "test"

        resp = self.client.post(
            "/posts/create",
            data={
                "title": "Test",
                "content": "This is test!",
                "is_active": True,
                "posted": "2025-01-01T12:00"
            },
            follow_redirects=True
        )

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Post added successfully", resp.data)

        
        with self.app.app_context():
            post = Post.query.filter_by(title="Test").first()
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is test!")
            self.assertEqual(post.author, "test")
