import re

def generate_token_maps(tokenizer):
    vocab = tokenizer.get_vocab().keys()


    
    #regex_a = re.compile(r'^[^"<lit>]+$')  # Qualsiasi tranne '"'
    regex_a = re.compile(r'^(?!.*(Ġ<lit>|Ġ</lit>|")).+$') #(?!.*("<lit>|")) → Esclude qualsiasi stringa che contenga "<lit>" o " (virgolette doppie).
    #.+$ → Assicura che ci sia almeno un carattere valido nella stringa (evita di accettare stringhe vuote).
    #regex_s = re.compile(r'^Ġ[^"\n\t\r\f\v()/:~0-9]+$')  # Inizia con "Ġ" e non ha caratteri proibiti
    #regex_s = re.compile(r'^Ġ[^"\n\t\r\f\v()/:~]+$') 
    regex_s = re.compile(r'^Ġ(?!<lit>|</lit>)[^"\n\t\r\f\v()/:~]+$')
    #regex_s = re.compile(r'^Ġ.+$')
    regex_c = re.compile(r'^[^Ġ\n\t\r\f\v()/:~]+$')  # Non inizia con "Ġ" e non ha caratteri proibiti
    #regex_c = re.compile(r'^[^Ġ].+$')
    regex_pointer = re.compile(r'^Ġ<pointer:[0-9]+>$')
    #regex_operator = re.compile(r'^Ġ:[^"\n\t\r\f\v()/:~]+$')
    regex_operator = re.compile(r'^Ġ:[^"\n\t\r\f\v()/:~]+$')

    map_terminal_tokens = {
        '(': ['(','Ġ('],
        '"': ['"','Ġ"','Ġ<lit>','Ġ</lit>'],
        #'/': ['/','Ġ/'],
        ')': [')', 'Ġ)'],
        ':': [':'],#'Ġ:'],
        'pointer': [token for token in vocab if regex_pointer.match(token)],
        #'operator': [token for token in vocab if regex_operator.match(token)],
        'operator' :[ token for token in vocab if regex_operator.match(token)],# and token != 'Ġ:'],
        'a': [token for token in vocab if regex_a.match(token)],  
        's': [token for token in vocab if regex_s.match(token)],  # Token di inizio parola (con "Ġ")
        'c': [token for token in vocab if regex_c.match(token)]   # Token di continuazione (senza "Ġ")
    }

    # Esegui gli assert per verificare che i gruppi siano distinti
    assert set(map_terminal_tokens['"']).isdisjoint(map_terminal_tokens['a']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['(']).isdisjoint(map_terminal_tokens['c']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[')']).isdisjoint(map_terminal_tokens['c']), "guarda map_terminal_tokens"
    #assert set(map_terminal_tokens['/']).isdisjoint(map_terminal_tokens['c']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[':']).isdisjoint(map_terminal_tokens['c']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['(']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[')']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    #assert set(map_terminal_tokens['/']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[':']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['"']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"

    assert set(map_terminal_tokens['(']).isdisjoint(map_terminal_tokens['pointer']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[')']).isdisjoint(map_terminal_tokens['pointer']), "guarda map_terminal_tokens"
    #assert set(map_terminal_tokens['/']).isdisjoint(map_terminal_tokens['pointer']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[':']).isdisjoint(map_terminal_tokens['pointer']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['"']).isdisjoint(map_terminal_tokens['pointer']), "guarda map_terminal_tokens"

    assert set(map_terminal_tokens['(']).isdisjoint(map_terminal_tokens['operator']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[')']).isdisjoint(map_terminal_tokens['operator']), "guarda map_terminal_tokens"
    #assert set(map_terminal_tokens['/']).isdisjoint(map_terminal_tokens['operator']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[':']).isdisjoint(map_terminal_tokens['operator']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['"']).isdisjoint(map_terminal_tokens['operator']), "guarda map_terminal_tokens"

    assert set(map_terminal_tokens['pointer']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['operator']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"


    print("Esempi di token per 'a':", map_terminal_tokens['a'][:10])
    print("Esempi di token per 's':", map_terminal_tokens['s'][:10])
    print("Esempi di token per 'c':", map_terminal_tokens['c'][:10])
    return map_terminal_tokens
