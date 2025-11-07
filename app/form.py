from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp

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