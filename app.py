from flask import Flask, request, jsonify
from googletrans import Translator
import random

app = Flask(__name__)
translator = Translator()

languages = [
    "af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "ny", "zh-CN",
    "zh-TW", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "fy", "gl", "ka",
    "de", "el", "gu", "ht", "ha", "haw", "he", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it",
    "ja", "jv", "kn", "kk", "km", "rw", "ko", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk",
    "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "or", "ps", "fa", "pl", "pt",
    "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su",
    "sw", "sv", "tg", "ta", "tt", "te", "th", "tr", "uk", "ur", "ug", "uz", "vi", "cy",
    "xh", "yi", "yo", "zu"
]

@app.route('/')
def home():
    return """
    Language Quiz! Enter a word in the URL bar, and we'll choose a\n random language to guess that word from!\n Example: /translate?word=hello  
"""

@app.route('/translate', methods=['GET', "POST"])
def translate_word():


    if request.method == "POST":    
        data = request.get_json()
        text = data.get('text')
        dest_language = data.get('dest_language', 'en') 

        if not text:
            return jsonify({'error': 'Text to translate is missing'}), 400

        try:
            translated = translator.translate(text, dest=dest_language)
            return jsonify({
                'original_text': text,
                'translated_text': translated.text,
                'src_language': translated.src,
                'dest_language': dest_language
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500



    elif request.method == "GET":
        word = request.args.get('word')

        if not word:
            return jsonify({'error': 'Word is missing in the URL'}), 400

        chosen_language = random.choice(languages)

        try:
            translated = translator.translate(word, dest=chosen_language)
            return jsonify({
                'word': word,
                'translated_word': translated.text,
                'chosen_language': translated.src
            })
        except Exception as e:
            print(chosen_language)
            return jsonify({'error': str(e)}), 500
    


if __name__ == '__main__':
    app.run(debug=True)
