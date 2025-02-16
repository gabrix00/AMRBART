import logging
class BaseStreamer:
    """
    Base class from which `.generate()` streamers should inherit.
    """
    def __init__(self, tokenizer, pda):
        self.tokenizer = tokenizer
        self.pda = pda
        self.is_first_call = True  # Variabile per evitare la chiamata iniziale con un tensore di più elementi.

    def put(self, value):

        if self.pda.eos():
            print("STACK vuoto, eos AMR generato! Interrompendo la generazione.")
            return  # Esce dalla funzione, interrompendo l'elaborazione
    
        """Function that is called by `.generate()` to push new tokens"""
        generated_token_id = value[0]
        print(f"Valore ricevuto in put: {generated_token_id}")
        logging.info(f"Valore ricevuto in put:{generated_token_id}")

        if not self.is_first_call:
            #token = self.tokenizer.decode(generated_token_id, skip_special_tokens=True, add_prefix_space=True)
            #print(f"token decodificato con prefix_space: {token}")
            # Decodifica il token senza aggiungere il prefisso (quindi senza `Ġ`)
                
            token = self.tokenizer.decode(generated_token_id, skip_special_tokens=True)
            print(f"Token decodificato: {token} (ID: {generated_token_id})")

            #if token == 'âĢĵ':
            #    print("Token decodificato come 'âĢĵ', correggi la decodifica.")
                # Esegui la gestione specifica per 'âĢĵ'
            #    token = '–'  # Imposta il token corretto, se necessario (trattino lungo)

            #if generated_token_id == 2383:
            #    token = "-"

            # Se il token ha uno spazio come primo carattere (es. ' and'), aggiungi 'Ġ'
            if token.startswith(' '):
                token = 'Ġ' + token.lstrip()  # Aggiungi Ġ e rimuovi lo spazio iniziale
                # Stampa il risultato
                print(f"Token decodificato con Ġ aggiunto: {token}")

            print(f"Token decodificato: {token}")

            
            self.pda.next_state(token)  # Esegui il next_state del PDA
            
        self.is_first_call = False
        

    def end(self):
        """Function that is called by `.generate()` to signal the end of generation"""
        logging.info("end generation")
        