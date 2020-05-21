from app import app
from flask import render_template, url_for
from app.models.forms import IngredientForm
from app.models.tables import Recipe, Ingredient
import pandas as pd
from fuzzywuzzy import fuzz
import sqlalchemy as db
import os
from flask import Flask 
  
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

@app.route('/')
def index():
    form = IngredientForm()
    return render_template('index.html', form=form)

@app.route('/receitas', methods=['POST'])
def receitas():
    df_ingredientes = pd.read_csv('./app/data/df_ingredientes2.csv')
    form = IngredientForm()
    if form.category.data and form.ingredients.data:
        category = form.category.data

        user_ingredients = form.ingredients.data
        user_ingredients = [ingredient.strip() for ingredient in user_ingredients.split(',')]

        id_ingredient_user = []
        for ingredient in user_ingredients:
            lst_id_ingredient = df_ingredientes.loc[df_ingredientes['ingrediente'] == f'{ingredient}', :]['id_ingrediente'].values

            if len(lst_id_ingredient) > 0:
                id_ingredient = lst_id_ingredient[0]
                id_ingredient_user.append(id_ingredient)
            else:
                for unique_ingredient in df_ingredientes['ingrediente']:
                    ratio = fuzz.token_set_ratio(ingredient, unique_ingredient)
                    if ratio > 85:
                        lst_id_ingredient = df_ingredientes.loc[df_ingredientes['ingrediente'] == f'{unique_ingredient}', :]['id_ingrediente'].values
                        id_ingredient = lst_id_ingredient[0]
                        id_ingredient_user.append(id_ingredient)
                        break

        if len(id_ingredient_user) > 1:
            id_ingredient_user = tuple(id_ingredient_user)
        else:
            id_ingredient_user = f'({id_ingredient_user[0]})'

        engine = db.create_engine(os.environ.get('DATABASE_URL'))


        query = f'''SELECT 
                    t2.href,
                    t2.rendimento,
                    t2.tempo_preparo,
                    t2.nome,
                    t2.qtde_ingrediente_usuario,
                    t2.qtd_ingrediente,
                    t2.ingredients_ratio,
                    t2.categoria,
                    rim.image_url
                FROM
                    (SELECT 
                        *
                    FROM
                        (SELECT 
                        r.href,
                            r.rendimento,
                            r.tempo_preparo,
                            r.nome,
                            COUNT(i.id_ingrediente) AS qtde_ingrediente_usuario,
                            r.qtd_ingrediente,
                            (COUNT(i.id_ingrediente) / r.qtd_ingrediente) AS ingredients_ratio,
                            r.categoria
                    FROM
                        ingredient i
                    JOIN recipe_ingredient ri ON i.id_ingrediente = ri.id_ingredient
                    JOIN recipes_df r ON r.id_recipes_df = ri.id_recipe
                    WHERE
                        i.id_ingrediente IN {id_ingredient_user}
                    GROUP BY ri.id_recipe
                    ORDER BY qtde_ingrediente_usuario DESC) AS t
                    WHERE
                        t.ingredients_ratio > 0.5
'''

        if category != 'Todas':
            clause = f''' AND
                        t.categoria IN ("{category}")'''
            query += clause

        query += ''' ORDER BY t.qtde_ingrediente_usuario DESC
        LIMIT 21) AS t2
            LEFT JOIN
        recipes.images rim ON t2.href = rim.href'''


        results = engine.execute(query)
        recipes = [recipe for recipe in results]

    return render_template('receitas.html', recipes=recipes)
