grammar = {
    'Start': {'NT': [('NT','Node')]},

    'Node': {'T': {'(': [('NT', 'Symbol'), ('NT', 'NodeLabel?'), ('NT', 'Relation*'), ('T', ')')]}},


    'NodeLabel?': {'T': {'/': [('NT', 'Concept')]},
                   'NULL': []},

    'Concept': {
        'T': {'"': [('NT', 'Any_except_"*'), ('T', '"')]},
        'NT': [('NT', 'Symbol')]
    },

    'Relation*': {'T': {":":[("NT",'NameChar+?'),('NT','NodeAtom'),('NT','Relation*')]}, 
                  'NT':[]},

    'NodeAtom': {
        'T': {'/': [('NT', 'Concept')],
              '(': [('NT', 'Symbol'), ('NT', 'NodeLabel?'), ('NT', 'Relation*'), ('T', ')')]}
    },

    'Atom': {
        'T': {'"': [('NT', 'Any_except_"*'), ('T', '"')]},
        'NT': [('NT', 'Symbol')]
    },

    'Symbol': {'NT': [('NT', 'NameChar+')]},

    'NameChar+?' : {'T': {'s' :[('NT', 'NameChar*')]},
                    'NT':[]
    },

    'NameChar+': {'T': {'s':[('NT', 'NameChar*')]}}, #No_special_chars_or_digits_starting_word --> s

    'NameChar*': {'T': {'c':[('NT', 'NameChar*')]}, #'No_special_chars_or_digits_continuation --> c
                  'NT':[]
    },

    'Any_except_"*': {'T': {'a':[('NT', 'Any_except_"*')]}, 
                      'NT': [],
    }
    
}