from flask import Flask, request, jsonify, render_template
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
def home():
    return render_template("index.html")
@app.route("/query", methods=["POST"])
def query():
    try:
        # Parse the user's input from the request
        user_input = request.json.get("message", "")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Run the LLaMA model via subprocess
        process = subprocess.Popen(
            ["ollama", "run", "llama3.2"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Decode output as UTF-8
            encoding="utf-8"  # Ensure proper encoding
        )

        # Send the user's input to the model
        stdout, stderr = process.communicate(input=user_input)

        # Check for errors in the subprocess
        if process.returncode != 0:
            return jsonify({"error": f"Model error: {stderr.strip()}"}), 500

        # Collect and combine all output lines
        response_lines = stdout.strip().splitlines()
        full_response = " ".join(response_lines)

        return jsonify({"response": full_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "LLaMA API is running. Use the /query endpoint to interact with the model."})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=4040)
