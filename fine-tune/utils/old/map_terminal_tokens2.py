
def generate_token_maps(tokenizer):
    vocab = tokenizer.get_vocab().keys()


    #\u0120 rappresenta la lettera "Ġ" (G con punto sopra) nella codifica Unicode.
    # nei modelli basati su byte pair encoding (BPE), il prefisso \u0120 viene spesso usato per indicare uno spazio prima di una parola.

    regex_rules = {
        'regex_a': r'^(?!.*(\u0120<lit>|\u0120</lit>|\" )).+$',
        'regex_s': r'^\u0120(?!(?:-?$|<lit>$|</lit>$))[^"\n\t\r\f\v()/:~]+$',
        'regex_c': r'^(?!(?:-?$|<lit>$|</lit>$))[^"\u0120\n\t\r\f\v()/:~]+$',
        'regex_pointer': r'^\u0120<pointer:[0-9]+>$',
        'regex_operator': r'^\u0120:[^"\n\t\r\f\v()/~]+$',
        'regex_number': r'^[0-9]+$',
        'regex_lit': r'^<lit>.*?</lit>$'
    }

    map_terminal_tokens = {
        '(': ['(','Ġ('],
        '"': ['"','Ġ"'],
        ')': [')', 'Ġ)'],
        '-': ['-','Ġ-'],
        'regex_lit': [token for token in vocab if regex_pointer.match(token)],
        'pointer': [token for token in vocab if regex_pointer.match(token)],
        'operator' :[ token for token in vocab if regex_operator.match(token)],# and token != 'Ġ:'],
        'a': [token for token in vocab if regex_a.match(token)],  
        's': [token for token in vocab if regex_s.match(token)],  # Token di inizio parola (con "Ġ")
        'c': [token for token in vocab if regex_c.match(token)]   # Token di continuazione (senza "Ġ")
    }

    # Esegui gli assert per verificare che i gruppi siano distinti

    assert set(map_terminal_tokens['-']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['-']).isdisjoint(map_terminal_tokens['c']), "guarda map_terminal_tokens"

    assert set(map_terminal_tokens['c']).isdisjoint(map_terminal_tokens['operator']), "guarda map_terminal_tokens"

    assert set(map_terminal_tokens['"']).isdisjoint(map_terminal_tokens['a']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['(']).isdisjoint(map_terminal_tokens['c']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[')']).isdisjoint(map_terminal_tokens['c']), "guarda map_terminal_tokens"
    
   
    assert set(map_terminal_tokens['(']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[')']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    
    assert set(map_terminal_tokens['"']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"

    assert set(map_terminal_tokens['(']).isdisjoint(map_terminal_tokens['pointer']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[')']).isdisjoint(map_terminal_tokens['pointer']), "guarda map_terminal_tokens"

    assert set(map_terminal_tokens['"']).isdisjoint(map_terminal_tokens['pointer']), "guarda map_terminal_tokens"

    assert set(map_terminal_tokens['(']).isdisjoint(map_terminal_tokens['operator']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[')']).isdisjoint(map_terminal_tokens['operator']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['"']).isdisjoint(map_terminal_tokens['operator']), "guarda map_terminal_tokens"

    assert set(map_terminal_tokens['pointer']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['operator']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"


    #print("Esempi di token per 'a':", map_terminal_tokens['a'][:10])
    #print("Esempi di token per 's':", map_terminal_tokens['s'][:10])
    #print("Esempi di token per 'c':", map_terminal_tokens['c'][:10])
    return map_terminal_tokens
