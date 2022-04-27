OBJECTS = ['beef', 'tortilla', 'lemon', 'chicken', 'onion',
           'tomato', 'spice', 'mushroom', 'meat', 'garlic',
           'tomato sauce', 'sauce', 'pasta', 'bacon', 'sausage', 'fish',
           'cabbage', 'potato', 'butter', 'water', 'bread',
           'flour', 'nutmeg', 'parsley', 'dough', 'egg', 'black olive', 'olive',
           'gyoza filling', 'patty', 'jelly', 'fruit', 'strawberry', 'pineapple',
           'kiwi', 'orange', 'clams', 'cilantro', 'rice', 'celery',
           'carrots', 'beef stock', 'sour cream', 'vegetables', 'green onion', 'bread crumbs', 'crumbs', 'wine',
           'filling', 'stock', 'cream', 'oil', 'jelly roll',
           'lemon juice', 'lemon sauce', 'milk mixture', 'broth', 'beef broth', 'lemon glaze', 'red pepper',
           'jellyroll'] + ['fruit mix']

SPRINKLE_OBJECTS = ['spice', 'bacon', 'flour', 'parsley', 'nutmeg']

SPRINKLE_TOOLS = ['salt', 'pepper']

SPECIAL_OBJECTS = ['mixture']


PLACES = ['dish', 'bowl', 'pot', 'plate', 'pan', 'tinfoil',
          'cup', 'stove', 'baking dish', 'paper towel',
          'skillet', 'mixing bowl', 'board', 'fruit bowl', 'bottle', 'rectangular plate', 'strainer', 'frying pan',
          'cooking pot', 'rectangular plate']

POUR_PLACES = ['bowl', 'pot', 'cup', 'bottle']

TOOLS = ['knife', 'colander', 'spoon', 'towel', 'tongs', 'pin',
         'fork', 'spatula', 'gloves', 'faucet', 'rolling pin',
         'toothpick', 'oven', 'olive oil', 'salt', 'white wine', 'pepper', 'milk']

REMOTE_TOOLS = ['olive oil', 'salt', 'white wine', 'pepper', 'milk']

GOALS = ['cut', 'stir', 'pour', 'wrap', 'heat', 'squeeze', 'sprinkle', 'roll', 'dip']

SPECIAL_GOALS = ['transfer', 'unknown']

INTERACTIONS = ['holding', 'handover']

ALL_GOALS = GOALS + SPECIAL_GOALS

ALL_OBJECTS = OBJECTS + PLACES + TOOLS + SPECIAL_OBJECTS

KB = {'ingredients': OBJECTS, 'containers': PLACES, 'tools': TOOLS, 'actions': GOALS + SPECIAL_GOALS}

# use this color table to draw rectangle
color_table = {'knife': (255, 100, 100), 'spoon': (100, 150, 200), 'bowl': (150, 110, 50), 'plate': (125, 20, 40),
               'jelly': (200, 50, 60), 'fruit:mixed': (130, 70, 100), 'mushroom': (20, 50, 150),
               'chicken': (220, 20, 30), 'meat mix': (50, 120, 180), 'onion': (40, 70, 20),
               'garlic': (38, 49, 123), 'tomato sauce': (67, 234, 135), 'lemon': (57, 158, 45),
               'pasta': (145, 57, 25), 'flour': (210, 137, 24), 'nutmeg': (157, 59, 213),
               'parsley': (70, 150, 57), 'dough': (95, 157, 240), 'egg': (85, 145, 25),
               'black olive': (35, 77, 187), 'bacon': (89, 167, 45), 'sausage': (55, 221, 134),
               'olive oil': (51, 88, 134), 'pepper': (98, 46, 223), 'milk': (57, 87, 213),
               'butter': (213, 134, 233),
               'water': (235, 200, 57), 'bread': (156, 231, 244), 'mixture': (113, 234, 145),
               'patty': (231, 134, 175), 'egg mixture': (75, 150, 180), 'spice': (45, 58, 117),
               'towel': (175, 167, 223), 'fork': (185, 234, 176), 'spatula': (235, 157, 187),
               'rolling pin': (145, 167, 189), 'cooking pan': (234, 123, 247), 'pot': (25, 78, 145),
               'cup': (57, 93, 134), 'cutting board': (245, 56, 78), 'strainer': (158, 34, 145)}

PERSONS = ['person0', 'person1']
HANDS = ['right', 'left']

BODYPARTS = []
for person in PERSONS:
    for hand in HANDS:
        BODYPARTS.append('{}_{}'.format(person, hand))
