from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired


class IngredientForm(FlaskForm):
    category = SelectField("category", choices=['Todas', 'Doces e sobremesas', 'Bolos e tortas doces',
       'Alimentação Saudável', 'Massas',
       'Saladas, molhos e acompanhamentos', 'Peixes e frutos do mar',
       'Sopas', 'Lanches', 'Prato Único', 'Aves', 'Carnes', 'Bebidas',
       'Peixes', 'Light'], validators=[DataRequired()])
    ingredients = TextAreaField("ingredients", validators=[DataRequired()])