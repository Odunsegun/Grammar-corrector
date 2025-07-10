# app.py

from flask import Flask, request, jsonify, send_file, render_template
from Model import SpellCheckerModule, run_correction_pipeline
from file_reader import extract_text_from_pdf, extract_text_from_docx
from Model import generate_highlighted_diff
from summarizer import summarize_text
import os
import tempfile

app = Flask(__name__)
spell_checker_module = SpellCheckerModule()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spell', methods=['POST', 'GET'])
def spell():
    if request.method == 'POST':
        text = request.form['text']
        mode = request.form.get('mode')

        corrected_text = ""
        corrected_grammar_text = ""
        corrected_grammar_mistakes = []
        count = 0
        summary = ""

        if mode in ['correct', 'both']:
            corrected_text = spell_checker_module.correct_spell(text)
            corrected_grammar_text, corrected_grammar_mistakes, count = spell_checker_module.correct_grammar(text)

        if mode in ['summarize', 'both']:
            summary = summarize_text(text)

        return render_template('index.html',
                               corrected_text=corrected_text,
                               corrected_grammar=corrected_grammar_text,
                               grammar_mistakes=corrected_grammar_mistakes,
                               mistake_count=count,
                               summary=summary,
                               highlighted = generate_highlighted_diff(text, corrected_grammar_text)
        )
    return render_template('index.html')


@app.route('/grammar', methods=['POST', 'GET'])
def grammar():
    if request.method == 'POST':
        file = request.files['file']
        extension = file.filename.rsplit('.', 1)[-1].lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}', mode='w+', encoding='utf-8') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        # Your existing extract logic here...
        # Extract -> correct_spell -> correct_grammar
        if extension == 'pdf':
            from file_reader import extract_text_from_pdf
            readable_file = extract_text_from_pdf(tmp_path)
        elif extension == 'docx':
            from file_reader import extract_text_from_docx
            readable_file = extract_text_from_docx(tmp_path)
        else:
            readable_file = file.read().decode('utf-8', errors='ignore')

        corrected_file_text = spell_checker_module.correct_spell(readable_file)
        corrected_file_grammar, _, _ = spell_checker_module.correct_grammar(readable_file)

        # Save corrected grammar to temp file for download
        with open('static/corrected_output.txt', 'w', encoding='utf-8') as f:
            f.write(corrected_file_grammar)

        return render_template('index.html',
                               corrected_file_text=corrected_file_text,
                               corrected_file_grammar=corrected_file_grammar,
                               summary=summarize_text(readable_file))  # if using summarizer
    return render_template('index.html')

@app.route('/download')
def download():
    return send_file('static/corrected_output.txt', as_attachment=True)

@app.route('/api/correct', methods=['POST'])
def api_correct():
    data = request.get_json()
    text = data.get("text", "")

    corrected = spell_checker_module.correct_spell(text)
    grammar, mistakes, count = spell_checker_module.correct_grammar(corrected)

    return jsonify({
        "corrected": corrected,
        "grammar_corrected": grammar,
        "mistake_count": count,
        "mistakes": mistakes
    })

if __name__ == "__main__":
    app.run(debug=True)
