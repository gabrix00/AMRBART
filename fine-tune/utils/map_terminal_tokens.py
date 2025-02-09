import re

def generate_token_maps(tokenizer):
    vocab = tokenizer.get_vocab().keys()

    regex_a = re.compile(r'^[^"]+$')  # Qualsiasi tranne '"'
    regex_s = re.compile(r'^Ġ[^\n\t\r\f\v()/:~0-9]+$')  # Inizia con "Ġ" e non ha caratteri proibiti
    #regex_s = re.compile(r'^Ġ.+$')
    regex_c = re.compile(r'^[^Ġ\n\t\r\f\v()/:~0-9]+$')  # Non inizia con "Ġ" e non ha caratteri proibiti
    #regex_c = re.compile(r'^[^Ġ].+$')

    map_terminal_tokens = {
        '(': ['('],
        '"': ['"'],
        '/': ['/'],
        ')': [')'],
        ':': [':'],
        'a': [token for token in vocab if regex_a.match(token)],  
        's': [token for token in vocab if regex_s.match(token)],  # Token di inizio parola (con "Ġ")
        'c': [token for token in vocab if regex_c.match(token)]   # Token di continuazione (senza "Ġ")
    }

    # Esegui gli assert per verificare che i gruppi siano distinti
    assert set(map_terminal_tokens['"']).isdisjoint(map_terminal_tokens['a']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['(']).isdisjoint(map_terminal_tokens['c']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[')']).isdisjoint(map_terminal_tokens['c']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['/']).isdisjoint(map_terminal_tokens['c']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[':']).isdisjoint(map_terminal_tokens['c']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['(']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[')']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['/']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens[':']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"
    assert set(map_terminal_tokens['"']).isdisjoint(map_terminal_tokens['s']), "guarda map_terminal_tokens"


    print("Esempi di token per 'a':", map_terminal_tokens['a'][:10])
    print("Esempi di token per 's':", map_terminal_tokens['s'][:10])
    print("Esempi di token per 'c':", map_terminal_tokens['c'][:10])
    return map_terminal_tokens
