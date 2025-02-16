grammar = {
    'Start': {'T': {'(': [('NT','Node'), ('NT','EL'), ('T', ')')]}},
    
    'Node': {'T': {
        '(': [('NT','Node'),('NT','EL'),('T', ')')],
        'pointer': [('NT','L')],
        '-': [('NT','Node'),('NT','EL'),('T', ')')],
        '"': [('NT','Any_except_quote'), ('T','"')],
        'number': [('NT', 'Num')],
        'lit': [('T', '<lit>'), ('NT', 'Any_except_lit'), ('T', '</lit>')]
    }},
    
    'L': {'T': {'s': [('NT','LC')]}, 'NT': []},
    
    'LC': {'T': {'c': [('NT','LC')]}, 'NT': []},
    
    'Num': {'T': {'digit': [('NT','Num')]}, 'NT': []},
    
    'Any_except_quote': {'T': {'a': [('NT','Any_except_quote')]}, 'NT': []},
    
    'Any_except_lit': {'T': {'a': [('NT','Any_except_lit')]}, 'NT': []},
    
    'EL': {'T': {
        'operator': [('NT','LC'),('NT','Node'),('NT','EL')],
        'op': [('NT','LC'),('NT','Node'),('NT','EL')],
        'ARG': [('NT','Num'), ('NT','Node'), ('NT','EL')],
        'ARG-of': [('NT','Num'), ('NT','Node'), ('NT','EL')],
        'degree': [('NT','Node')],
        'mod': [('NT','Node')],
        'polarity': [('T','-')],
        'frequency': [('NT','Num')],
        'time': [('NT','Node')],
        'medium': [('NT','Node')],
        'manner': [('NT','Node')],
        'purpose': [('NT','Node')],
        'topic': [('NT','Node')],
        'quant': [('NT','Node')],
        'source-of': [('NT','Node')],
        'domain': [('NT','Node')]
    }}
}