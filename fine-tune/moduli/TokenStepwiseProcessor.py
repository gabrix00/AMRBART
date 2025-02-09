import logging
import torch
import matplotlib.pyplot as plt
from transformers import LogitsProcessor

class TokenStepwiseProcessor(LogitsProcessor):
    def __init__(self, state_sequence, tokenizer):
        """
        Inizializza il filtro dei token.

        Args:
            state_sequence: Lista di dizionari che rappresentano gli stati e i token associati.
            tokenizer: Oggetto tokenizer per convertire token in ID.
        """
        self.state_sequence = state_sequence
        self.tokenizer = tokenizer
        self.current_state_index = 0
        self.current_step_index = 0
        self.generated_tokens = []
        self.eos_token_id = tokenizer.eos_token_id  # ID del token di fine sequenza
        #print(self.eos_token_id)
        #print(tokenizer.convert_ids_to_tokens(13))

    def log_top_10_scores(self, scores, prefix):
        # Calcolare le probabilità usando softmax
        probabilities = torch.softmax(scores, dim=1)

        # Ordina le probabilità in ordine decrescente e prendi i top 10
        top_probs, top_indices = torch.topk(probabilities, 10, dim=1)
        top_token_ids = top_indices[0].tolist()  # ID dei token con le top 10 probabilità
        top_probs = top_probs[0].tolist()  # Probabilità dei top 10 token

        # Convertire gli ID dei token in stringhe leggibili
        top_token_labels = self.tokenizer.convert_ids_to_tokens(top_token_ids)

        # Registrare i token e le probabilità corrispondenti
        log_message = f"{prefix}:\nTop 10 Tokens - Step {self.current_step_index}:\n"
        for token, prob in zip(top_token_labels, top_probs):
            log_message += f"Token: {token}, Probability: {prob:.6f}\n"

        # Stampa o salva il log
        logging.debug(log_message)  # Puoi sostituirlo con un salvataggio su file se preferisci


    def visualize_top_10_scores(self, scores):
        # Creare un grafico degli score
        plt.figure(figsize=(10, 6))

        # Ordina gli score in ordine decrescente e prendi i top 10
        top_scores, top_indices = torch.topk(scores, 10, dim=1)
        top_token_ids = top_indices[0].tolist()  # ID dei token con i top 10 score
        top_scores = top_scores[0].tolist()  # Punteggi dei top 10 token

        # Convertire gli ID dei token in stringhe leggibili
        top_token_labels = self.tokenizer.convert_ids_to_tokens(top_token_ids)

        # Visualizzare i top 10 score
        plt.bar(top_token_labels, top_scores, color='blue')
        plt.title(f"Top 10 Scores - Step {self.current_step_index}")
        plt.xticks(rotation=90)
        plt.xlabel("Token")
        plt.ylabel("Score")

        # Mostrare il grafico
        plt.tight_layout()
        plt.show()

    def get_valid_tokens(self):
        """Ottieni i token validi per lo stato e passo attuali."""
        if self.current_step_index >= len(self.state_sequence):
            raise IndexError(f"Passo corrente {self.current_step_index} supera i limiti della sequenza di stati.")
        
        current_states = (self.current_state_index if isinstance(self.current_state_index, list) else [self.current_state_index])

        state_dict = self.state_sequence[self.current_step_index]
        
        if self.current_state_index == 0:
            valid_tokens = self.state_sequence[self.current_step_index].keys()
        else:

            valid_tokens = [
                token for token, states in state_dict.items()
                if any(state + 1 in states for state in current_states)]  # Controlla consecutività per ogni stato
            #dovrei aggiungere un vincolo che al passo successivo di generazione deve tenere conto del contesto della gerarchia,
            #es dopo "-" è chiaro che lui può generare potenzialmente uqaluneu altro tok della sua classe , ma gli devo mettere il voncolo che deve seguire la gereracgia 
        logging.info(f"Valid Tokens: {valid_tokens}")
        #logging.info(f"Step: {self.current_step_index}, Current State: {self.current_state_index}, Valid Tokens: {valid_tokens}")

        if not valid_tokens:
            raise ValueError(f"Nessun token valido trovato per lo stato {self.current_state_index} al passo {self.current_step_index}.")

        return valid_tokens
    
    def reset(self):
        """Reset degli stati alla condizione iniziale."""
        self.current_state_index = 0
        self.current_step_index = 0
        self.generated_tokens = []
        logging.info("Stati resettati.")

    
    def __call__(self, input_ids, scores):

        #self.visualize_top_10_scores(scores)
        '''
        """Applica il filtro durante l'inferenza del modello."""
        #print(input_ids[0, -1].item())
        if input_ids[0, -1].item() == self.eos_token_id:
            logging.info(f"Raggiunto token di fine frase <eos>. Resetto gli stati...")
            self.reset()
            return 1
        '''
        original_probabilities = torch.softmax(scores, dim=-1)
        self.log_top_10_scores(original_probabilities, prefix="Original")


        valid_tokens = self.get_valid_tokens()
        valid_token_ids = self.tokenizer.convert_tokens_to_ids(valid_tokens)

        # Maschera con -inf per i token non validi
        filter_mask = torch.full_like(scores, -float('inf'))
        filter_mask[:, valid_token_ids] = 0

        # Chiamare la funzione di visualizzazione per i top 10 score
        #self.visualize_top_10_scores(scores + filter_mask)
        filtered_scores = scores + filter_mask
        filtered_probabilities = torch.softmax(filtered_scores, dim=-1)
        self.log_top_10_scores(filtered_probabilities, prefix="Filtered")

        # Aggiorna l'indice del passo corrente
        self.current_step_index += 1

        return scores + filter_mask
    


    def update_state(self, generated_token_id):
        """Aggiorna lo stato corrente in base al token generato."""
        generated_token = self.tokenizer.convert_ids_to_tokens([generated_token_id])[0]

        if self.current_step_index >= len(self.state_sequence):
            raise IndexError("Passo corrente supera i limiti della sequenza di stati.")

        state_dict = self.state_sequence[self.current_step_index -1] #devo recuperare lo stato del token allo step index precedente

        if generated_token in state_dict:
            possible_states = state_dict[generated_token]
            #logging.info(f"poss state:  {possible_states}")

            if not isinstance(self.current_state_index, list):
                self.current_state_index = [self.current_state_index]

            #possibile state contine gli stati nuovi!!
            if self.current_state_index != [0]:
                filtered_states = [state for state in possible_states if state-1 in self.current_state_index]
            else:
                filtered_states = possible_states

            #logging.info(f"poss state filtered:{filtered_states}")
            
            logging.info(f"Stato corrente: {self.current_state_index}, Token generato: {generated_token}")# Step index: {self.current_step_index}")

            if not filtered_states:
                logging.debug(f"Attenzione: nessuno stato successivo per il token '{generated_token}'. Assegnando None.")
                self.current_state_index = None
            else:
                self.current_state_index = filtered_states #possible_states
        else:
                raise KeyError(
                    f"Token '{generated_token}' non valido nello stato attuale. "
                    f"Stato corrente: {self.current_state_index}, Step: {self.current_step_index}, "
                    f"Token validi: {list(state_dict.keys())}"
                )


        # Aggiungi il token generato alla lista dei token generati
        self.generated_tokens.append(generated_token)


        return self.current_state_index