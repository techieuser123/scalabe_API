""" from PIL import Image
import pytesseract
import cv2
from flask import Flask, request

pytesseract.pytesseract.tesseract_cmd = r"C://Program Files//Tesseract-OCR//tesseract.exe"



image_path = 'img1.png'  
image = cv2.imread(image_path)

rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

pil_image = Image.fromarray(rgb_image)

text = pytesseract.image_to_string(pil_image)


print("Extracted Text:")
print(text)

 """




from flask import Flask, request, send_file
from gtts import gTTS
import os
from PIL import Image
import pytesseract
import cv2
import numpy as np
from flask import Flask, request, jsonify


#pytesseract.pytesseract.tesseract_cmd = r"C://Program Files//Tesseract-OCR//tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def img_to_text():
    try:

        image_file = request.files['file']
        
        file_bytes = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        text = pytesseract.image_to_string(pil_image)

        return jsonify({"Extracted Text": text}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/text-to-speech', methods=['GET'])
def text_to_speech():
    
    data = request.json
    if not data or 'text' not in data:
        return {'error': 'No text provided'}, 400

    mytext = data['text']
    language = 'en'
    tts = gTTS(text=mytext, lang=language, slow=False)
    file_name = "output.mp3"
    tts.save(file_name)
    os.system(f"start {file_name}")
    
    return send_file(file_name, as_attachment=True)





if __name__ == '__main__':
    app.run(debug=True,port=4040)
