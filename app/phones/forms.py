from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class PhoneForm(FlaskForm):
    model_name = StringField("Назва моделі", validators=[DataRequired(), Length(max=100)])
    price = FloatField("Ціна ($)", validators=[DataRequired()])
    description = TextAreaField("Опис / Характеристики")
    
    brand_id = SelectField("Оберіть бренд", coerce=int, validators=[DataRequired()])
    
    submit = SubmitField("Зберегти")