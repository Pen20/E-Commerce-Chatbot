from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from bot.retrieval_generation import generation
from bot.ingest import ingestdata

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Initialize the vector store and retrieval-generation chain once at startup
vstore, _ = ingestdata("done")  # 
chain = generation(vstore)

@app.route("/")
def index():
    """Render the chat UI."""
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    """Handle chat messages sent from the frontend."""
    msg = request.form.get("msg")

    # Check if a message was provided
    if not msg:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Process the message through the retrieval-generation chain
        result = chain.invoke(msg)
        print("Response:", result)

        # Return the result as plain text (compatible with your frontend)
        return result

        # Alternatively, return JSON if you plan to extend:
        # return jsonify({"response": result})

    except Exception as e:
        print(f"Error processing message: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

if __name__ == '__main__':
    # Run the Flask app (debug=True for development only)
    app.run(host="0.0.0.0")
