# app.py

from flask import Flask, request, jsonify
from inference import run_login

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.get_json()
        result = run_login(input_data)

        # Convert float32/NumPy types to regular Python floats
        if isinstance(result, list):
            result = [float(x) for x in result]
        elif isinstance(result, dict) and "prediction" in result:
            result["prediction"] = float(result["prediction"])
        elif isinstance(result, (np.float32, np.float64)):
            result = float(result)

        return jsonify({
            "status": "success",
            "prediction": result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
