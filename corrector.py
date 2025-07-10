# corrector.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("prithivida/grammar_error_correcter_v1")
model = AutoModelForSeq2SeqLM.from_pretrained("prithivida/grammar_error_correcter_v1")

def correct_text(text):
    input_ids = tokenizer.encode("gec: " + text, return_tensors="pt", truncation=True)
    outputs = model.generate(input_ids, max_length=128, num_beams=5, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
