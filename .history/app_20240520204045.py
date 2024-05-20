from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/error')
def error():
    response = jsonify({"error": "This is an error message"})
    response.status_code = 400
    return response

@app.route('/run-generate-commit')
def run_generate_commit():
    try:
        result = subprocess.run(['python', 'tools/generate_commit/generate_commit.py'], capture_output=True, text=True)
        return jsonify({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':  # pragma: no cover
    app.run(host='0.0.0.0', port=80)
