import unittest
from app import create_app, db, bcrypt
from app.users.models import User


class UserTestCase(unittest.TestCase):

    def setUp(self):
        """Створення тестового оточення"""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        """Очищення після тестів"""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_register_page_loads(self):
        response = self.client.get("/users/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Username", response.data)

    def test_login_page_loads(self):
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Вхід у систему", response.get_data(as_text=True))

    def test_user_registration(self):
        response = self.client.post(
            "/users/register",
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "secret123",
                "confirm_password": "secret123",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Account created for testuser!", response.data)

        user = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")

    def test_user_login(self):
        hashed = bcrypt.generate_password_hash("secret123").decode("utf-8")
        user = User(username="tester", email="t@t.com", password=hashed)
        db.session.add(user)
        db.session.commit()

        response = self.client.post(
            "/users/login",
            data={"username": "tester", "password": "secret123"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You have been logged in successfully!", response.data)

    def test_user_logout(self):
        hashed = bcrypt.generate_password_hash("pass123").decode("utf-8")
        user = User(username="abc", email="abc@test.com", password=hashed)
        db.session.add(user)
        db.session.commit()

        self.client.post(
            "/users/login",
            data={"username": "abc", "password": "pass123"},
            follow_redirects=True,
        )

        response = self.client.get("/users/logout", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You have successfully logged out.", response.data)


if __name__ == "__main__":
    unittest.main()
