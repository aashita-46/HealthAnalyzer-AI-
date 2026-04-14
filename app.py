from flask import Flask, request, render_template, jsonify
import os
from detector import ShelfDetector
from ocr_reader import OCRReader

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

detector = ShelfDetector()
ocr = OCRReader()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        file = request.files.get('image')
        if not file: return "No image provided", 400
        
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        
        items = detector.detect(path)
        final_data = []
        
        # Health Analysis Logic
        bad_keywords = ['sugar', 'sweet', 'crisp', 'toffee', 'bubbles', 'soda', 'syrup', 'choco', 'fat', 'ogar', 'bites', 'candy']

        for item in items:
            text = ocr.read_text(item['crop'])
            text_low = text.lower()
            
            if any(word in text_low for word in bad_keywords):
                verdict, reason, color = "Avoid", "High sugar/processed content.", "danger"
            elif text == "Generic Product":
                verdict, reason, color = "Neutral", "Label unclear. Check manually.", "warning"
            else:
                verdict, reason, color = "Buy", "No immediate harmful additives detected.", "success"

            final_data.append({
                "label": text,
                "verdict": verdict,
                "reason": reason,
                "color": color
            })
            
        return render_template('results.html', items=final_data, image=file.filename)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)