# UCSI University AI Chatbot Project

## Overview
A Flask-based AI Chatbot for university students, featuring **RAG (Retrieval Augmented Generation)** for accurate academic info and **Dual-Authentication** for secure grade access. Powered by **Google Gemini**.

## Key Features
- **AI Chat**: Natural language understanding using Gemini w/ Single-Call Optimization.
- **RAG System**: Context-aware answers based on university documents.
- **Security Check**: JWT + 2nd Password for accessing sensitive data (Grades, GPA).
- **Premium UI**: Glassmorphism design, Mobile-Responsive (Fullscreen), Smart Suggestions.

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Environment**:
   - Create valid `.env` file with `GOOGLE_API_KEY`, `MONGO_URI`, `SECRET_KEY`.

3. **Run Server**:
   ```bash
   python main.py
   ```
   Access at: `http://localhost:5000`

## Documentation
- For full details, see [HANDOVER.md](HANDOVER.md).
