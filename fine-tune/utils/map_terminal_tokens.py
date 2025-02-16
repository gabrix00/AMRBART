import re

def generate_token_maps(tokenizer):
    vocab = tokenizer.get_vocab().keys()


    
    #regex_a = re.compile(r'^[^"<lit>]+$')  # Qualsiasi tranne '"'
    regex_a = re.compile(r'^(?!.*(Ġ<lit>|Ġ</lit>|")).+$')

    #regex_s = re.compile(r'^Ġ(?!<lit>|</lit>|-)[^"\n\t\r\f\v()/:~]+$')
    #regex_s = re.compile(r'^Ġ(?!(?:-?$|<lit>$|</lit>$|[0-9]+$))[^"\n\t\r\f\v()/:~]+$')
    #regex_s = re.compile(r'^Ġ(?!(?:-?$|<lit>$|</lit>$))[^"\n\t\r\f\v()/:~]+$')
    #regex_s = re.compile(r'^Ġ(?!(<lit>$|</lit>$|prep$))[^"\n\t\r\f\v()/:~]+$')#|op$
    regex_s = re.compile(r'^Ġ(?!(<lit>$|</lit>$|prep$|op$))[^"\n\t\r\f\v()/:~]+$')

    #regex_c = re.compile(r'^(?!<lit>|</lit>|-)[^"Ġ\n\t\r\f\v()/:~]+$')  # Non inizia con "Ġ" e non ha caratteri proibiti
    #regex_c = re.compile(r'^(?!(?:-?$|<lit>$|</lit>$!|[0-9]+$))[^"Ġ\n\t\r\f\v()/:~]+$')
    #regex_c = re.compile(r'^(?!(<lit>$|</lit>$!|[0-9]+$))[^"Ġ\n\t\r\f\v()/:~]+$')
    regex_c = re.compile(r'^(?!(<lit>$|</lit>$))[^"Ġ\n\t\r\f\v()/~]+$')
    



    regex_pointer = re.compile(r'^Ġ<pointer:[0-9]+>$')
    
    #regex_operator = re.compile(r'^Ġ:[^"\n\t\r\f\v()/~]+$')
    #regex_operator = re.compile(r'^Ġ:[^"\n\t\r\f\v()/~]*$')
    regex_operator = re.compile(r'^Ġ:[^"\n\t\r\f\v()/~]*$')


    #regex_digit = re.compile(r'^(?!pointer)[Ġ]?\d+$')
    
    #regex_digit = re.compile(r'^(?!Ġ<pointer:\d+>$)[Ġ]?\d+$')
    
    

    map_terminal_tokens = {
        '(': ['(','Ġ('],
        '"': ['"','Ġ"','Ġ<lit>','Ġ</lit>'],
        ')': [')', 'Ġ)'],
        #'-': ['Ġ-'],
        #'digit': [token for token in vocab if regex_digit.match(token)],
        'pointer': [token for token in vocab if regex_pointer.match(token)],
        'operator' :[ token for token in vocab if regex_operator.match(token)],#+["Ġop"],# and token != 'Ġ:'],
        'a': [token for token in vocab if regex_a.match(token)],  
        's': [token for token in vocab if regex_s.match(token)],  # Token di inizio parola (con "Ġ")
        'c': [token for token in vocab if regex_c.match(token)]+["Ġprep","Ġop"]   # Token di continuazione (senza "Ġ")
    }
    print("Esempi di token per 'operator':", map_terminal_tokens['operator'][:100])
    # Esegui gli assert per verificare che i gruppi siano distinti

    #assert set(map_terminal_tokens['digit']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    #assert set(map_terminal_tokens['digit']).isdisjoint(map_terminal_tokens['c']), "guarda map_terminal_tokens"


    #assert set(map_terminal_tokens['-']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    #assert set(map_terminal_tokens['-']).isdisjoint(map_terminal_tokens['c']), "guarda map_terminal_tokens"

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

    #print("Esempi di token per 'digit':", map_terminal_tokens['digit'][:100])
    print('\n')
    print("Esempi di token per 'operator':", map_terminal_tokens['operator'][:100])
    return map_terminal_tokens
