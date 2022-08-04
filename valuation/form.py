# https://qiita.com/kotamatsuoka/items/c93129f6ade5974dc122
# https://wtforms.readthedocs.io/en/3.0.x/fields/

from flask_wtf import FlaskForm
from wtforms import Form, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange

class DataForm(FlaskForm):
    data_plus = IntegerField(validators=[NumberRange(0,10000000000,'数値で入力してください（0〜10,000,000')], default=0)
    data_minus = IntegerField(validators=[NumberRange(-10000000000,0,'数値で入力してください（-10,000,000〜0')], default=0)
    data_plus_minus = IntegerField(validators=[NumberRange(-10000000000,10000000,'数値で入力してください（-10,000,000〜10,000,000')], default=0)