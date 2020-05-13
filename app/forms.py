from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
# from wtforms.validators import DataRequired


class Change_json(FlaskForm):
    input_field = TextAreaField('Input', render_kw={"rows": 24, "cols": 10})
    submit = SubmitField('Расчёт')
