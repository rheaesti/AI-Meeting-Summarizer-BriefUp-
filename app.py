from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
from dotenv import load_dotenv
import os
import tempfile
import json
import re

load_dotenv()

app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


@app.route('/summarize', methods=['POST'])
def summarize():

    if 'file' not in request.files:
        return jsonify({
            "error": "No file uploaded"
        }), 400

    file = request.files['file']

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp:
        file.save(temp.name)
        temp_path = temp.name

    try:

        # =========================
        # STEP 1 — TRANSCRIBE AUDIO
        # =========================

        with open(temp_path, "rb") as audio_file:

            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3"
            )

        transcript = transcription.text

        # =========================
        # STEP 2 — SUMMARIZE
        # =========================

        prompt = f"""
You are an expert meeting analyst.

Analyze this meeting transcript and return ONLY valid raw JSON.

DO NOT use markdown.
DO NOT use triple backticks.

Transcript:
{transcript}

Return in EXACTLY this format:

{{
  "summary": "3-5 sentence summary",
  "keyPoints": [
    "point1",
    "point2"
  ],
  "actionItems": [
    "task1",
    "task2"
  ],
  "participants": [
    "person1"
  ],
  "estimatedWordCount": 500,
  "sentiment": "positive"
}}
"""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        response_text = completion.choices[0].message.content

        # =========================
        # CLEAN RESPONSE
        # =========================

        cleaned = re.sub(r"```json|```", "", response_text).strip()

        try:

            parsed_json = json.loads(cleaned)

            return jsonify(parsed_json)

        except Exception:

            print("\n===== INVALID JSON FROM MODEL =====\n")
            print(response_text)

            return jsonify({
                "error": "Model returned invalid JSON",
                "raw": response_text
            }), 500

    except Exception as e:

        print("\n===== SERVER ERROR =====\n")
        print(str(e))

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == '__main__':
    app.run(debug=True)