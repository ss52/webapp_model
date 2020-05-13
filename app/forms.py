from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
# from wtforms.validators import DataRequired


class Change_json(FlaskForm):
    # name = StringField('name', validators=[DataRequired()])
    input_field = TextAreaField('Input', render_kw={"rows": 20, "cols": 10})
    submit = SubmitField('Do this')
