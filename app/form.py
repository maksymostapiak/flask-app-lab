from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from app.users.models import User

class ContactForm(FlaskForm):
    name = StringField(
        "Ім’я",
        validators=[
            DataRequired(),
            Length(min=4, max=10, message="Довжина має бути 4–10 символів")
        ]
    )

    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Невірний формат email")
        ]
    )

    phone = StringField(
        "Телефон",
        validators=[
            DataRequired(),
            Regexp(r"^\+380\d{9}$", message="Формат телефону має бути: +380XXXXXXXXX")
        ]
    )

    subject = SelectField(
        "Тема звернення",
        choices=[
            ("support", "Підтримка"),
            ("order", "Замовлення"),
            ("other", "Інше питання")
        ],
        validators=[DataRequired()]
    )

    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(),
            Length(max=500, message="Максимум 500 символів")
        ]
    )

    submit = SubmitField("Надіслати")

class LoginForm(FlaskForm):
    username = StringField(
        "Username / Email",
        validators=[DataRequired(message="Це поле обовʼязкове")]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Це поле обовʼязкове"),
            Length(min=4, max=10, message="Пароль повинен містити від 4 до 10 символів")
        ]
    )

    remember = BooleanField("Запам'ятати мене")

    submit = SubmitField("Увійти")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Це поле обовʼязкове"),
            Length(min=4, max=10, message="Довжина username має бути 4–10 символів"),
            Regexp(
                r"^[A-Za-z][A-Za-z0-9_]*$",
                message="Username повинен починатися з літери та містити тільки латинські букви, цифри або _"
            )
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Це поле обовʼязкове"),
            Email(message="Невірний формат email")
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Це поле обовʼязкове"),
            Length(min=6, message="Пароль має містити мінімум 6 символів"),
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Це поле обовʼязкове"),
            EqualTo("password", message="Паролі повинні співпадати")
        ]
    )

    submit = SubmitField("Зареєструватись")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Цей email вже зареєстрований.")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("Цей username вже зайнятий.")