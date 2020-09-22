"""Forms for cupcakes app"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField
#  IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import Optional, InputRequired, AnyOf, NumberRange, URL


class AddCupcakeForm(FlaskForm):
    """Form for adding cupcakes"""
    flavor = StringField(label="Flavor", validators=[
                         InputRequired(message="Flavore cannot be blank.")])
    size = SelectField(label="Size", choices=[('small', 'small'), ('medium', 'medium'), ('large', 'large')], validators=[InputRequired(
        message="Size cannot be blank."), AnyOf(['small', 'medium', 'large'], message="Size must be small, medium, or large.")])
    rating = DecimalField(label="Rating", places=1, validators=[
                          InputRequired(message="Rating cannot be blank."), NumberRange(min=0, max=10, message="Rating must be between 0 and 10.")])
    image = StringField(label="Photo URL", validators=[
        Optional(),
        URL(require_tld=True, message="URL must be valid.")])
