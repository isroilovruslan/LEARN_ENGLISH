from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

class VocabularyManager:
    def __init__(self, filename="vocabulary.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        return []

    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def add_word(self, word, translation, example, example_translation):
        entry = {
            "word": word,
            "translation": translation,
            "example": example,
            "example_translation": example_translation
        }
        self.data.append(entry)
        self.save_data()

manager = VocabularyManager()

@app.route('/')
def index():
    return render_template("index.html", words=manager.data)

@app.route('/add', methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        word = request.form.get('word').strip()
        translation = request.form.get('translation').strip()
        example = request.form.get('example').strip()
        example_translation = request.form.get('example_translation').strip()

        if word and translation and example and example_translation:
            manager.add_word(word, translation, example, example_translation)
            flash("Word added successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("All fields are required!", "danger")

    return render_template("add_word.html")

if __name__ == "__main__":
    app.run(debug=True)
