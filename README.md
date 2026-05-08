# AI Meeting Summarizer - Brief Up
# Brief Up - AI Meeting Summarizer

`Brief Up` is a Flask web app that turns meeting recordings into structured summaries using Groq models.

Upload a video file, and the app will:
- transcribe the recording with `whisper-large-v3`
- summarize the transcript with `llama-3.3-70b-versatile`
- return:
  - summary
  - key points
  - action items
  - participants mentioned
  - estimated word count

## App Preview
### Home Page
<img src="https://raw.githubusercontent.com/rheaesti/AI-Meeting-Summarizer-BriefUp-/main/image1.png" width="700">

### Summary Output
<img src="https://raw.githubusercontent.com/rheaesti/AI-Meeting-Summarizer-BriefUp-/main/image2.png" width="700">

### Upload Page
<img src="https://raw.githubusercontent.com/rheaesti/AI-Meeting-Summarizer-BriefUp-/main/image3.png" width="700">

### Final Result
<img src="https://raw.githubusercontent.com/rheaesti/AI-Meeting-Summarizer-BriefUp-/main/image4.png" width="700">

## Features

- Drag-and-drop UI for meeting files
- Supports only `MP4`
- 25 MB max file size guard (Groq Whisper limit)
- Structured JSON output from the backend
- Copy buttons for summary and key points

## Tech Stack

- Python
- Flask
- Groq Python SDK
- python-dotenv
- Vanilla HTML/CSS/JS frontend

## Project Structure

- `app.py` - Flask backend, transcription + summarization API
- `index.html` - Single-page frontend interface
- `.env` - Local environment variables (not committed)

## Requirements

- Python 3.9+ recommended
- A Groq API key

## Setup

1. Clone or open this project folder.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install flask groq python-dotenv
```

4. Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Run the App

From the project root:

```bash
python app.py
```

Open your browser at:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

## How It Works

1. Frontend uploads a media file to `POST /summarize`
2. Backend saves file temporarily
3. Backend transcribes audio via Groq Whisper (`whisper-large-v3`)
4. Backend sends transcript to Groq chat model (`llama-3.3-70b-versatile`)
5. Backend returns parsed JSON to frontend for display
6. Temporary file is deleted in `finally`

## API

### `POST /summarize`

Form-data:
- `file` (required): audio/video meeting recording

Success response (example):

```json
{
  "summary": "3-5 sentence summary...",
  "keyPoints": ["point1", "point2"],
  "actionItems": ["task1", "task2"],
  "participants": ["person1"],
  "estimatedWordCount": 500,
  "sentiment": "positive"
}
```

Error response:

```json
{
  "error": "No file uploaded"
}
```

## Troubleshooting

- **`No file uploaded`**  
  Make sure the request includes a `file` form field.

- **`Model returned invalid JSON`**  
  The LLM response was not parseable JSON. Retry the request.

- **Empty server response in UI**  
  Check the backend terminal for a Python traceback and confirm `GROQ_API_KEY` is set.

- **File too large**  
  Keep uploads at or below 25 MB.

## Notes

- `app.py` currently runs with `debug=True` for local development.
- Do not commit your `.env` file or API keys.
