import json

def extract_sentences_to_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if line.startswith('# ::snt '):  # Cerca le righe che iniziano con "# ::snt "
                sentence = line[len('# ::snt '):].strip()  # Rimuove il prefisso e spazi bianchi
                json.dump({"sent": sentence,"amr":""}, outfile)
                outfile.write('\n')  # Aggiunge una nuova riga per il formato JSONL


def clean_dataset(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if line.startswith('# '):
                continue
            else:
                outfile.write(line)
'''
# Esempio di utilizzo
input_filename = "test.txt"  # Sostituisci con il tuo file di input
output_filename = "lp_test.jsonl"
extract_sentences_to_jsonl(input_filename, output_filename)
print(f"Frasi estratte e salvate in {output_filename}")
'''
# Esempio di utilizzo
input_filename = "ldc_data/pred_base_little_test.txt"  # Sostituisci con il tuo file di input
output_filename = "ldc_data/pred_base_little_test_clean.txt"
clean_dataset(input_filename, output_filename)
print(f"Frasi estratte e salvate in {output_filename}")