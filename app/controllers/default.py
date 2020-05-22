from app import app
from flask import render_template, url_for
from app.models.forms import IngredientForm
from app.models.tables import Recipe, Ingredient
import pandas as pd
from fuzzywuzzy import fuzz
import sqlalchemy as db
import os
from app.controllers.clean_ingredients import clean_ingredient
from unidecode import unidecode


@app.route('/')
def index():
    form = IngredientForm()
    return render_template('index.html', form=form)

@app.route('/receitas', methods=['POST'])
def receitas():
    df_ingredientes = pd.read_csv('./app/data/df_ingredient2.csv')
    form = IngredientForm()
    if form.category.data and form.ingredients.data:
        category = form.category.data

        user_ingredients = form.ingredients.data
        user_ingredients = [ingredient.strip() for ingredient in user_ingredients.split(',')]

        id_ingredient_user = []
        for ingredient in user_ingredients:
            ingredient = unidecode(ingredient)
            ingredient = clean_ingredient(ingredient)
            print(ingredient)
            lst_id_ingredient = df_ingredientes.loc[df_ingredientes['ingrediente'] == f'{ingredient}', :]['id_ingrediente'].values

            if len(lst_id_ingredient) > 0:
                id_ingredient = lst_id_ingredient[0]
                id_ingredient_user.append(id_ingredient)
            else:
                for unique_ingredient in df_ingredientes['ingrediente']:
                    ratio = fuzz.partial_ratio(ingredient, unique_ingredient)

                    if ratio > 80:
                        lst_id_ingredient = df_ingredientes.loc[df_ingredientes['ingrediente'] == f'{unique_ingredient}', :]['id_ingrediente'].values
                        id_ingredient = lst_id_ingredient[0]
                        id_ingredient_user.append(id_ingredient)
                        break
        print(id_ingredient_user)
        if len(id_ingredient_user) > 1:
            id_ingredient_user = tuple(id_ingredient_user)
        elif len(id_ingredient_user) == 1:
            id_ingredient_user = f'({id_ingredient_user[0]})'
        if len(id_ingredient_user) == 0:
            recipes = []
        else:

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
                            t.ingredients_ratio > 0.6
    '''

            if category != 'Todas':
                clause = f''' AND
                            t.categoria IN ("{category}")
                            '''
                query += clause

            query += ''' LIMIT 200) AS t2
                LEFT JOIN
            recipes.images rim ON t2.href = rim.href
            WHERE rim.image_url IS NOT NULL
            ORDER BY t2.ingredients_ratio DESC
            LIMIT 21'''


            results = engine.execute(query)
            recipes = [recipe for recipe in results]

    return render_template('receitas.html', recipes=recipes)
