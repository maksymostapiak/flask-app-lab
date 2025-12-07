from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length
from datetime import datetime

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    content = TextAreaField("Content", validators=[DataRequired()])
    is_active = BooleanField("Enabled", default=True)
    author_id = SelectField("Author", coerce=int)
    tags = SelectMultipleField("Tags", coerce=int)
    submit = SubmitField("Save")
    posted = DateTimeLocalField(
        "Posted",
        format="%Y-%m-%dT%H:%M",
        default=datetime.utcnow
    )