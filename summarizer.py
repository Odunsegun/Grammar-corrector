from transformers import pipeline

# Load the model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_len=130, min_len=30):
    text = text.strip().replace("\n", " ")
    if len(text) > 1024:
        text = text[:1024]
    summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
    return summary[0]['summary_text']
