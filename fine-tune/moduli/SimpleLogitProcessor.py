import logging
from transformers import LogitsProcessor
import torch

class MaskLogitsProcessor(LogitsProcessor):
    def __init__(self, tokenizer, pda):
        """
        mask_token_ids: Lista di liste di token ID da mascherare (assegnando -inf)
        tokenizer: Il tokenizer da usare per decodificare i token ID
        """
        #self.mask_token_ids = mask_token_ids #lo prendeva prima del pda, quado non cera get_valid tokens dentro __call__
        self.tokenizer = tokenizer
        self.pda = pda


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
        log_message = f"{prefix}:\nTop 10 Tokens\n"
        for token, prob in zip(top_token_labels, top_probs):
            log_message += f"Token: {token}, Probability: {prob:.6f}\n"

        # Stampa o salva il log
        #logging.debug(log_message)
        print(log_message)


    def __call__(self, input_ids, scores):
        print(f"Stack: {self.pda.stack[::-1]}") 

        valid_tokens = self.pda.get_tokens()
        valid_tokens_ids = self.tokenizer.convert_tokens_to_ids(valid_tokens)
        if valid_tokens_ids:
            print(f"tokens validi secondo il get tokens del PDA sono:{valid_tokens}")

            print("\n\nLogitsProcessor attivato!")  
            original_probabilities = torch.softmax(scores, dim=-1)
            self.log_top_10_scores(original_probabilities, prefix="Original")
            '''
            # Calcola la distribuzione di probabilità prima della modifica
            probs_before = torch.softmax(scores, dim=-1)
            top_k_before = torch.topk(probs_before, k=5, dim=-1)
            print(f"Probs prima della modifica:\n{top_k_before.values.tolist()}")
            '''

            filter_mask = torch.full_like(scores, -float('inf'))
            filter_mask[:, valid_tokens_ids] = 0
            filtered_scores = scores + filter_mask

            
            filtered_probabilities = torch.softmax(filtered_scores, dim=-1)
            self.log_top_10_scores(filtered_probabilities, prefix="Filtered")
        else:
            print(f"Valid tokens è vuoto!{valid_tokens}")

        return scores + filter_mask

        '''
        # Decodifica i top 5 ID token in stringhe di testo
        
        top_k_ids = top_k_before.indices.tolist()
        decoded_top_k = [self.tokenizer.decode(ids,skip_special_tokens=True) for ids in top_k_ids]
        print(f"Top 5 token ID prima della modifica:\n{top_k_ids}")
        print(f"Top 5 token (decodificati):\n{decoded_top_k}\n")

        # Applicazione del logits processor per mascherare i token
        for token_list in self.mask_token_ids:
            for token in token_list:
                scores[:, token] = -float("inf")
        

        # Calcola la distribuzione di probabilità dopo la modifica
        probs_after = torch.softmax(scores, dim=-1)
        top_k_after = torch.topk(probs_after, k=5, dim=-1)

        print(f"Probs dopo la modifica:\n{top_k_after.values.tolist()}")

        # Decodifica i top 5 ID token in stringhe di testo dopo la modifica
        top_k_ids_after = top_k_after.indices.tolist()
        decoded_top_k_after = [self.tokenizer.decode(ids,skip_special_tokens=True) for ids in top_k_ids_after]
        print(f"Top 5 token ID dopo la modifica:\n{top_k_ids_after}")
        print(f"Top 5 token (decodificati) dopo la modifica:\n{decoded_top_k_after}\n")
        

        return scores
        '''
        