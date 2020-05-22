import re
import spacy
import pt_core_news_sm


nlp = pt_core_news_sm.load()

customize_stop_words = [
    'lata', 'copo', 'colher', 'pacote', 'caixa', 'caixas', 'caixinha', 'caixinhas', 'ml', 'g', 'gramas', 'l',
    'litros', 'ml', 'colheres', 'vidrinho', 'xicaras', 'xicara', 'fatias', 'pitada', 'xicarade', 'bandeja',
    'bandejas', 'kg', 'cubo', 'cubos', 'barra', 'rasas', 'rasa', 'raso', 'rasos', 'cheia', 'cheias', 'cheio',
    'cheios', 'litro', 'medio', 'grande', 'pequeno', 'dentes', 'pequena', 'pequenas', 'pequenos', 'media',
    'medias', 'medios', 'folha', 'folhas', 'medida', 'inteiro', 'inteiros', 'inteiras', 'inteira', 'e', 'saches',
    'morna', 'morno' 'cortada', 'cortadas', 'cortado', 'cortados', 'maco', 'tira', 'tirinha', 'tiras', 'tirinhas',
    'sache', 'picada', 'picadas', 'picado', 'picados', 'picadinho', 'picadinhos', 'picadinha', 'picadinhas', 'ralado',
    'ralada', 'ralados', 'raladas', 'raladinho', 'raladinhos', 'raladinha', 'raladinhas', 'misturada', 'misturado',
    'cozido', 'cozidos', 'cozida', 'cozidas', 'a', 'gosto', 'tablete', 'tabletes', 'pacotes', 'pele', 'ate', 'o',
    'copos', 'bolo', 'fina', 'flocos', 'grossas', 'grossa', 'grosso', 'grossos', 'casca', 'cascas', 'descascada',
    'descascadas', 'descascado', 'descascados', 'cascas', 'aproximadamente', 'sal', 'tempero', 'quente', 'sabor',
    'temperos', 'sopa', 'desfiado', 'desfiados', 'desfiada', 'desfiadas', 'cha', 'opcional', 'saquinho', 'saco',
    'preferencia', 'usei', 'madura', 'maduras', 'maduro', 'maduros', 'amassada', 'amassadas', 'amassado', 'amassados',
    'latas', 'rasgadas', 'rasgada', 'temperada', 'temperadas', 'temperado', 'temperados', 'vidro', 'vidrinho', 'vidros',
    'vidrinhos', 'panela', 'escolheres', 'pote', 'potes', 'potinho', 'potinhos', 'americano', 'prato', 'refratario',
    'forno', 'preaquecido', 'pronta', 'banda', 'tradicional', 'fio', 'unidade', 'unidades', 'dissolvida', 'sobra',
    'sobras', 'servir', 'separado', 'separados', 'separada', 'separadas', 'semente', 'sementes', 'cubinho',
    'cubinhos', 'ja', 'refogada', 'refogar', 'refogadas', 'refogados', 'refogado', 'frio', 'fria', 'congelada',
    'congeladas', 'congelado', 'congelados', 'fresca', 'frescas', 'fresco', 'frescos', 'diluir', 'escorrido',
    'escorrida', 'envelope', 'envelopes', 'forma', 'formas', 'forminhas', 'redondo', 'redondos', 'refinado',
    'ramo', 'ramos', 'raminhos', 'desidratada', 'desidratadas', 'desidratado', 'desidratados', 'cozinho', 'dente',
    'pressao', 'hora', 'gelado', 'gelada', 'gelados', 'geladas', 'geladinhos', 'geladinhas', 'fica', 'criterio',
    'industrializado', 'industrializada', 'industrializados', 'industrializadas', 'quantidade', 'rodelas','laminas',
    'maos', 'diferentes', 'pedaco', 'pedacos', 'grosseiros', 'suficiente', 'cobrir'
]

for w in customize_stop_words:
    nlp.vocab[w].is_stop = True

def clean_ingredient(ingredient: str):
    '''
    The function receives an ingredient and returns a clean string of that ingredient.

    Example: input > '1 lata de leite condensado'
             output > 'leite condensado'
    '''

    ingredient = ingredient.lower()
    doc = nlp(ingredient)
    tokens = []
    for token in doc:
        if token.is_stop == False and token.is_punct == False and token.is_alpha == True:
            if token.is_digit == False:
                tokens.append(token.text)
    ingredient = ' '.join(tokens)
    if len(ingredient) > 0:
        if ingredient[-1] == 's':
            ingredient = ingredient[:-1]  ## this prevents words in plural

    ingredient = re.sub('gemas|claras|ovos|gema|clara', 'ovo', ingredient)
    ingredient = re.sub('fermento po', 'fermento', ingredient)
    ingredient = re.sub('azeite oliva', 'azeite', ingredient)
    ingredient = re.sub('queijo mussarela', 'mussarela', ingredient)
    ingredient = re.sub('maisena', 'maizena', ingredient)

    return ingredient