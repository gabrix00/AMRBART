'''
from transformers import BartForConditionalGeneration, AutoTokenizer
#from model_interface.tokenization_bart import AMRBartTokenizer      # We use our own tokenizer to process AMRs

#model = BartForConditionalGeneration.from_pretrained("xfbai/AMRBART-large-finetuned-AMR3.0-AMRParsing-v2")
#tokenizer = AMRBartTokenizer.from_pretrained("xfbai/AMRBART-large-finetuned-AMR3.0-AMRParsing-v2")

model = BartForConditionalGeneration.from_pretrained("xfbai/AMRBART-large-finetuned-AMR3.0-AMRParsing-v2")
tokenizer = AutoTokenizer.from_pretrained("xfbai/AMRBART-large-finetuned-AMR3.0-AMRParsing-v2")

print(tokenizer)

from transformers import BartForConditionalGeneration
from model_interface.tokenization_bart import AMRBartTokenizer
model = BartForConditionalGeneration.from_pretrained("xfbai/AMRBART-large-v2")
tokenizer = AMRBartTokenizer.from_pretrained("xfbai/AMRBART-large-v2")

# my improvisation:
inputs = tokenizer(["the cat sat on the mat"])
amr = model.generate(inputs)

print(amr)

from transformers import BartForConditionalGeneration, AMRBartTokenizer
import os

# Imposta il percorso della cache in cui sono stati scaricati i file
cache_dir = "/home/gtuccio/AMRBART/cache/.cache/"

# Carica il modello e il tokenizer da percorso locale
model_name = "xfbai/AMRBART-large-finetuned-AMR3.0-AMRParsing-v2"
tokenizer = AMRBartTokenizer.from_pretrained(cache_dir)
model = BartForConditionalGeneration.from_pretrained(cache_dir)

# Frase di input per test
sentence = "John bought a book."

# Tokenizza la frase
inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
print(inputs)

# Ottieni la rappresentazione AMR
output = model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])
'''

from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast

# Specifica il percorso dei file del tokenizer (es. vocab.json e merges.txt)
tokenizer_path = "/home/gtuccio/AMRBART/cache/.cache/"
tokenizer = PreTrainedTokenizerFast.from_pretrained(tokenizer_path)

model_name = "xfbai/AMRBART-large-finetuned-AMR3.0-AMRParsing-v2"
# Carica il modello
model = BartForConditionalGeneration.from_pretrained(model_name)

sentence = "John bought a book."

# Tokenizza la frase
inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
print(inputs)

# Ottieni la rappresentazione AMR
output = model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])
