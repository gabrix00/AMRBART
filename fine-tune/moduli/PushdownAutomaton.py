
# get_tokens(TOP)
#    - se TOP è terminale ritorna TOP
#    - altrimenti (se TOP è Non Terminale) procede ricorsivamente:
#    - cerca la riga(REGOLA) corrispondente a TOP e considera tutti i terminali iniziali di regole che iniziano per terminale e aggiunge eventualmente i seguenti:
#            - get_tokens(NT) dove NT è il primo Non terminale dell'unica regola TOP -> NT .... rimanente (se c'è)
#            - se produce_null(NT) ritorna true allora chiama get_tokens ricorsivamente col prossimo simbolo della regola TOP -> NT ....
#            - se c'è la regola TOP -> null chiama get_tokens ricorsivamente sul prossimo simbolo dello stack
# next_state()
#    Pop del simbolo dallo stack, cerca la riga corrispondente e vede se il token generato appare come simbolo terminale 
#    all'inizio di una regola della riga, altrimenti se c'è null procede ricorsivamente sul prossimo simbolo dello stack, 
#    altrimenti ci dovrà essere una regola che inizia per non-terminale. Metti tutti i simboli di quella regola sullo stack 
#    (push in ordine inverso) e procedi ricorsivamente. 

class PushdownAutomaton:
    def __init__(self,grammar,startSymbol,map):
        self.stack = [('NT',startSymbol)]
        self.grammar = grammar
        self.map_terminals_tokens = map
        """
        self.map_tokens_terminals = defaultdict(list)
        for terminal, tokens in map.items():
            for token in tokens:
                self.map_tokens_terminals[token].append(terminal)
        
        self.map_tokens_terminals = dict(self.map_tokens_terminals)
        """
        self.map_tokens_terminals = {}
        for terminal, tokens in map.items():
            for token in tokens:
                if token not in self.map_tokens_terminals:
                    self.map_tokens_terminals[token] = []
                self.map_tokens_terminals[token].append(terminal)
        
        #print(self.map_tokens_terminals)

    
    def recursive_get_tokens(self,stack):
        if not stack:
            return []
        
        TOP = stack.pop()  

        if TOP[0]=='T':
            return [TOP[1]] 
        
        TOP = TOP[1] 
        if TOP not in self.grammar:
            assert False, "Non terminale sullo stack non trovato come parte sinistra nella grammatica"
            return []
        
        tokens = []
        if 'T' in self.grammar[TOP]:  
            tokens = [k for k in self.grammar[TOP]['T']]
    

        if 'NT' in self.grammar[TOP]: 
            for symbol in self.grammar[TOP]['NT'][::-1]:
                stack.append(symbol)
            tokens += self.recursive_get_tokens(stack) 
      
        return tokens

    def get_tokens(self):
        terminals = self.recursive_get_tokens(self.stack.copy())
        tokens = set()
        for terminal in terminals:
            print(terminal)
            assert set(self.map_terminals_tokens[terminal]).isdisjoint(tokens), "Gli insiemi dei token associati ai terminali ammissibili non sono disgiunti"
            tokens.update(self.map_terminals_tokens[terminal])

        self.current_terminals = terminals

        #print(f"\n\nTerminals: {terminals}") #debug
        #print(f"Tokens: {tokens}\n\n") #debug
        return list(tokens)
        
    def next_state(self,token_gen):  #next state viene chiamato sul token generato!
        #print(f"token_gen:{token_gen}\n") #debug
        #qui token dovrebbe essere sostituito con terminal, perchè significa quello in realtà
        #print(f"\ncurrent terminals: {self.current_terminals}, mapped_token2terminal{self.map_tokens_terminals[token_gen]}")
        #if self.eos:
        #    return "eos raggiunto tramite stack vuoto"
        print(f"current terminals is:{self.current_terminals}")
        check_terminals = set(self.map_tokens_terminals[token_gen]).intersection(set(self.current_terminals))
        print(f"check_terminals is: {check_terminals}")
        assert len(check_terminals) == 1, "Scelto un token ambiguo, in quanto corrispondente a più possibili terminali per questo stato"
        terminal = list(check_terminals)[0]
        self.next_state_terminal(terminal)

        
    def next_state_terminal(self,terminal):
        token = terminal
        stack = self.stack
        TOP = stack.pop()
        if TOP[0]=='T':
            #print(TOP[1],token) #debug
            assert TOP[1]==token, "Token sullo stack diverso da quello atteso" 
            return 
        TOP = TOP[1] 
        if TOP not in self.grammar:
            assert False, "Non terminale sullo stack non trovato come parte sinistra nella grammatica"
            return
        
        if 'T' in self.grammar[TOP]: 
            if token in self.grammar[TOP]['T']:
                for symbol in self.grammar[TOP]['T'][token][::-1]:
                    stack.append(symbol)
                return
        
        if 'NT' in self.grammar[TOP]:
            for symbol in self.grammar[TOP]['NT'][::-1]: 
                stack.append(symbol)
            self.next_state_terminal(token)
            return

        
        assert False, "Token non trovato nella grammatica!"

    def eos(self):
        return True if not self.stack else False