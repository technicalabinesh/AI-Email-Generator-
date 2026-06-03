# AI Email Generator

A polished Streamlit application that generates professional emails using Google Gemini.
The app collects structured inputs (email type, tone, recipient, context), sends them to Gemini, and returns a ready-to-use email with subject + body.

## Table of Contents
- [Overview](#overview)
- [Core Features](#core-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How It Works (End-to-End)](#how-it-works-end-to-end)
- [Getting Started](#getting-started)
- [Usage Guide](#usage-guide)
- [Configuration Details](#configuration-details)
- [Error Handling](#error-handling)
- [Current Limitations](#current-limitations)
- [Customization Ideas](#customization-ideas)
- [License](#license)

## Overview
This project is a single-file Streamlit app (`ai_email_generator.py`) focused on fast, high-quality email drafting.
It provides:
- A premium UI with custom CSS
- Sidebar API configuration and model controls
- Form-driven prompt creation
- JSON-constrained LLM output parsing
- Download, copy, and regenerate actions
- In-session generation history

## Core Features
- **Structured generation**: Users provide email metadata and context before generation.
- **Tone + type controls**: Supports multiple email categories and tones.
- **JSON output enforcement**: Gemini is instructed to return strict JSON with `subject` and `body`.
- **Smart fallback cleaning**: If JSON parsing fails, markdown artifacts are stripped.
- **Session history**: Tracks recent generations inside Streamlit session state.
- **Export options**: Download as `.txt` or copy to clipboard.
- **Regeneration**: Regenerates using slightly higher temperature for variation.

## Tech Stack
- **Frontend/App runtime**: Streamlit
- **LLM provider**: Google Gemini via `google-genai`
- **Utilities**: `json`, `re`, `pyperclip`
- **Language**: Python

## Project Structure
```text
AI-Email-Generator-/
├── ai_email_generator.py   # Main Streamlit app (UI + generation logic)
├── README.md               # Project documentation
└── LICENSE                 # MIT license
```

## How It Works (End-to-End)
1. **App bootstraps** with page config, custom CSS, and session state defaults.
2. **User enters Gemini API key** in the sidebar.
3. **Sidebar validates API key** by creating a temporary `genai.Client`.
4. **User selects model settings** (`model`, `temperature`, `max_tokens`).
5. **User fills email form** (type, tone, recipient, sender, subject hint, key points, extras).
6. On **Generate**, app validates:
   - API key is configured
   - Key points are not empty
7. App builds a prompt from user fields (`build_prompt()`).
8. App calls Gemini (`run_generation()`) with:
   - System instruction forcing strict JSON output
   - User prompt content
   - Generation parameters from UI
9. App parses `response.text` as JSON and formats:
   - `Subject: ...`
   - blank line
   - body text
10. If parsing fails, app strips markdown artifacts and still returns usable text.
11. Output is shown in a styled panel, then user can:
   - Download as text
   - Copy to clipboard
   - Regenerate variant
12. Generation metadata is stored in session history and shown in sidebar.

## Getting Started

### Prerequisites
- Python 3.9+
- A Google AI Studio API key (Gemini)

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install streamlit google-genai pyperclip
   ```

### Run the App
```bash
streamlit run ai_email_generator.py
```

Then open the local URL shown by Streamlit (typically `http://localhost:8501`).

## Usage Guide
1. Enter your Gemini API key in the sidebar.
2. Pick email type and tone.
3. Fill recipient/sender/subject/context.
4. Click **Generate Email**.
5. Review the generated email on the right panel.
6. Use Download / Copy / Regenerate actions as needed.

## Configuration Details
- **Model**: currently fixed to `models/gemma-4-31b-it` in the dropdown list.
- **Creativity**: mapped to `temperature`.
- **Max Length (tokens)**: mapped to `max_output_tokens`.
- **Regenerate behavior**: re-runs generation with `temperature + 0.15` (capped at `1.0`).

## Error Handling
The app handles common failure cases:
- Missing API key → prompts user to configure it.
- Invalid API key / client failure → shows API connection failure status.
- Empty key points → warns user before generation.
- LLM/transport exceptions → displays generation error message.
- JSON parse errors → fallback cleanup returns plain text output when possible.

## Current Limitations
- Single-file architecture (UI + logic in one module).
- No persistent storage beyond Streamlit session state.
- No automated tests or dependency lock file included.
- Model list is currently hardcoded to one option.

## Customization Ideas
- Add multiple Gemini model options.
- Add prompt templates per email category.
- Add local file/database persistence for history.
- Add unit tests for prompt builder and response parser.
- Split UI, prompt logic, and model client into separate modules.

## License
This project is licensed under the MIT License. See [`LICENSE`](./LICENSE).
