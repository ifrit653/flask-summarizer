from flask import Flask, request, jsonify
from transformers import pipeline
import re

# Initialize Flask app
app = Flask(__name__)

# Load the summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Preprocessing functions
def clean_text(text):
    """Clean unwanted characters from text."""
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    return text.strip()

def truncate_text(text, max_tokens=1024):
    """Truncate text to fit within model's token limit."""
    tokens = text.split()
    if len(tokens) > max_tokens:
        return ' '.join(tokens[:max_tokens])
    return text

def preprocess_text(text, max_tokens=1024):
    """Combine cleaning and truncation."""
    cleaned_text = clean_text(text)
    return truncate_text(cleaned_text, max_tokens)

# API endpoint for summarization
@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        # Get input text from the request
        data = request.json
        if not data or 'text' not in data:
            return jsonify({"error": "Please provide text to summarize"}), 400

        input_text = data['text']
        # Preprocess the text
        preprocessed_text = preprocess_text(input_text)

        # Generate summary
        summary = summarizer(preprocessed_text, max_length=150, min_length=30, do_sample=False)

        # Return the summary
        return jsonify({"summary": summary[0]['summary_text']})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
