from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, DataRequired, Regexp, EqualTo
from wtforms import ValidationError
import asset.models as models

class IDCFrom(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(1, 64)])
    memo = StringField('memo', validators=[DataRequired()])
    submit = SubmitField('add')
