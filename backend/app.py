import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import run_model

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def nlp_model():
    try:
        data = request.get_json()
        input_string = data['input']
        result = run_model(input_string)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
