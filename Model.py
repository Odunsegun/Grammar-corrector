from textblob import TextBlob
import language_tool_python
from corrector import correct_text
import difflib

def generate_highlighted_diff(original, corrected):
    differ = difflib.ndiff(original.split(), corrected.split())
    result = []
    for token in differ:
        if token.startswith("- "):
            result.append(f"<span class='text-danger'>{token[2:]}</span>")
        elif token.startswith("+ "):
            result.append(f"<span class='text-success'>{token[2:]}</span>")
        elif token.startswith("  "):
            result.append(token[2:])
    return " ".join(result)


class SpellCheckerModule:
    def __init__(self):
        self.spell_check = TextBlob("")
        self.grammar_check = language_tool_python.LanguageTool('en-US')

    def correct_spell(self, text):
        words = text.split()
        corrected_words = []
        for word in words:
            corrected_word = str(TextBlob(word).correct())
            corrected_words.append(corrected_word)
        return " ".join(corrected_words)

    def correct_grammar(self, text):
        matches = self.grammar_check.check(text)
        foundmistakes = [match.message for match in matches]
        foundmistakes_count = len(foundmistakes)
        corrected_text = self.grammar_check.correct(text)
        return corrected_text, foundmistakes, foundmistakes_count

def run_correction_pipeline(user_input):
    return correct_text(user_input)

if __name__ == "__main__":
    obj = SpellCheckerModule()
    message = "Hello world. I like mashine learning. appple. bananana"

    print("🔤 Spell Check:")
    print(obj.correct_spell(message))

    print("\n📝 Grammar Check:")
    corrected_text, mistakes, count = obj.correct_grammar(message)
    print(f"Corrected Text: {corrected_text}")
    print(f"Found {count} grammar issues:")
    for i, msg in enumerate(mistakes, 1):
        print(f"{i}. {msg}")
