grammar = {
    'Start': {'T': {'(': [('NT','Node'), ('NT','EL'), ('T', ')')]}
    },

    'Node': {'T': {'(': [('NT','Node'),('NT','EL'),('T', ')')],
                   'pointer': [('NT','L')],
                   '"': [('NT','Any_except_"*'), ('T','"')],
                   's': [('NT','LC')]}
    },

    'L': {'T': {'s':[('NT','LC')]},
          'NT': []
    },

    'LC': {'T': {'c':[('NT','LC')]},
           'NT': []
    },

    'Any_except_"*': {'T': {'a':[('NT','Any_except_"*')]}, 
                      'NT': []
    },

    'EL': {'T': {'operator':[('NT','LC'),('NT','Node'),('NT','EL')]},
           'NT': []
    }
}