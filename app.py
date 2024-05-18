from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/error')
def error():
    response = jsonify({"error": "This is an error message"})
    response.status_code = 400
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
