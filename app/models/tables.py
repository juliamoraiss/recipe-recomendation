from app import db


class Href(db.Model):
    __tablename__ = "href_df"

    id_href = db.Column(db.Integer, primary_key=True)
    href = db.Column(db.Text)

    def __init__(self, href):
        self.href = href


class Recipe(db.Model):
    __tablename__ = "recipes_df"

    id_recipes_df = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    tempo_preparo = db.Column(db.Text)
    rendimento = db.Column(db.Text)
    href = db.Column(db.Text)
    modo_preparo = db.Column(db.Text)
    categoria = db.Column(db.Text)
    ingredientes = db.Column(db.Text)
    qtd_ingrediente = db.Column(db.Integer)

    def __init__(self, nome, tempo_preparo, rendimento, href, modo_preparo, categoria, ingredientes, qtd_ingrediente):
        self.nome = nome
        self.tempo_preparo = tempo_preparo
        self.rendimento = rendimento
        self.href = href
        self.modo_preparo = modo_preparo
        self.categoria = categoria
        self.ingredientes = ingredientes
        self.qtd_ingrediente = qtd_ingrediente

    def __repr__(self):
        return "<Recipe %r>" % self.nome


class Ingredient(db.Model):
    __tablename__ = "ingredient"

    id_ingrediente = db.Column(db.Integer, primary_key=True)
    ingrediente = db.Column(db.Text)

    def __init__(self, ingrediente):
        self.ingrediente = ingrediente

    def __repr__(self):
        return "<Ingredient %r>" % self.ingrediente


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"

    id_recipe_ingredient = db.Column(db.Integer, primary_key=True)
    id_recipe = db.Column(db.Integer)
    id_ingredient = db.Column(db.Integer)

    def __init__(self, id_recipe, id_ingredient):
        self.id_recipe = id_recipe
        self.id_ingredient = id_ingredient


class Image(db.Model):
    __tablename__ = "images"

    id_images = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.Text)
    href = db.Column(db.Text)

    def __init__(self, image_url, href):
        self.image_url = image_url
        self.href = href


